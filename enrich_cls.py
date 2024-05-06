import csv
import requests
import xml.etree.ElementTree as ET


def create_notation_map_via_download(url):
    notation_map = dict()
    r = requests.get(url)
    csv_data = r.text.splitlines()
    reader = csv.reader(csv_data)
    header = next(reader)
    from_index = header.index("fromNotation")
    to_indices = [header.index(col) for col in header if "toNotation" in col]
    for line in reader:
        to_notations = notation_map.get(line[from_index], [])
        to_notations += [line[i] for i in to_indices if line[i]]
        notation_map[line[from_index]] = to_notations
    return notation_map


def gen_datafield(tag, ind1, ind2, subfields):
    """
    Generate a datafield
    Subfields: list of tuples with (code, value) pairs
    """
    df = ET.Element("datafield", {"tag": tag, "ind1": ind1, "ind2": ind2})
    for code, value in subfields:
        sf = ET.SubElement(df, "subfield", {"code": code})
        sf.text = value
    return df


def enrich_bib(bib_element, ddc_to_bk, ddc_to_obv):
    update_flag = False
    df084_is_here = False
    df970_is_here = False
    df084__ = bib_element.find("./datafield[@tag='084'][@ind1=' '][@ind2=' ']")
    df9701_ = bib_element.find("./datafield[@tag='970'][@ind1='1'][@ind2=' ']")
    df08204a = bib_element.find(
        "./datafield[@tag='082'][@ind1='0'][@ind2='4']/subfield[@code='a']"
    )
    if (
        df084__ is not None
        and (sf2 := df084__.find("./subfield[@code='2']")) is not None
        and sf2.text == "bkl"
    ):
        df084_is_here = True
    if (
        df9701_ is not None
        and df9701_.find("./subfield[@code='c']") is not None
    ):
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
                            ("9", "O: Automatisch generiert aus Konkordanz DDC-BK (UBG)"),
                            ("2", "bkl"),
                        ],
                    )
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
                    )
                )
    if update_flag:
        return bib_element
    return
