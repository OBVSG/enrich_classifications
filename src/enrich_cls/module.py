import json
import xml.etree.ElementTree as ET

import requests

COLI_CONC_BASE_URL = "https://coli-conc.gbv.de/api/"


def get_concordance(session: requests.Session, id: str) -> requests.Response:
    return session.get(f"{COLI_CONC_BASE_URL}concordances/{id}")


def download_concordance(
    session: requests.Session,
    id: str,
    mimetype="application/x-ndjson; charset=utf-8",
) -> str | None:
    concordance = get_concordance(session, id)
    concordance = concordance.json()
    for dist in concordance.get("distributions"):
        if dist.get("mimetype") == mimetype:
            mappings = session.get(dist.get("download"))
            return mappings.text
    return None


def create_notation_map(concordance: str) -> dict[str, list]:
    notation_map = {}
    for line in concordance.splitlines():
        mapping = json.loads(line.strip())
        from_notation = mapping.get("from").get("memberSet")[0].get("notation")[0]
        to_notation = mapping.get("to").get("memberSet")[0].get("notation")
        to_notations = notation_map.get(from_notation, [])
        to_notations += to_notation
        notation_map[from_notation] = to_notations
    return notation_map


def gen_datafield(tag: str, ind1: str, ind2: str, subfields: list) -> ET.Element:
    """Generate a datafield
    Subfields: list of tuples with (code, value) pairs
    """
    df = ET.Element("datafield", {"tag": tag, "ind1": ind1, "ind2": ind2})
    for code, value in subfields:
        sf = ET.SubElement(df, "subfield", {"code": code})
        sf.text = value
    return df


def enrich_bib(
    bib_element: ET.Element,
    ddc_to_bk: dict,
    ddc_to_obv: dict,
) -> ET.Element | None:
    update_flag = False
    df084_is_here = False
    df970_is_here = False
    df084__fields = bib_element.findall("./datafield[@tag='084'][@ind1=' '][@ind2=' ']")
    df9701_ = bib_element.find("./datafield[@tag='970'][@ind1='1'][@ind2=' ']")
    df08204a = bib_element.find(
        "./datafield[@tag='082'][@ind1='0'][@ind2='4']/subfield[@code='a']",
    )
    for df084__ in df084__fields:
        if (
            sf2 := df084__.find("./subfield[@code='2']")
        ) is not None and sf2.text == "bkl":
            df084_is_here = True
    if df9701_ is not None and df9701_.find("./subfield[@code='c']") is not None:
        df970_is_here = True
    if df08204a is not None:
        dewey = df08204a.text[:3]
        if (bk_list := ddc_to_bk.get(dewey)) and not df084_is_here:
            update_flag = True
            for bk in bk_list:
                bib_element.append(
                    gen_datafield(
                        "084",
                        " ",
                        " ",
                        [
                            ("a", bk),
                            ("2", "bkl"),
                            (
                                "9",
                                "O: Automatisch generiert aus Konkordanz DDC-BK (UBG)",
                            ),
                        ],
                    ),
                )
        if (obv_list := ddc_to_obv.get(dewey)) and not df970_is_here:
            update_flag = True
            for fg in obv_list:
                bib_element.append(
                    gen_datafield(
                        "970",
                        "1",
                        " ",
                        [("c", fg)],
                    ),
                )
    if update_flag:
        return bib_element
    return None
