import csv
import xml.etree.ElementTree as ET


def create_notation_map(csv_file):
    notation_map = dict()
    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
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
    mms = bib_element.find("./controlfield[@tag='001']").text
    df084 = bib_element.find("./datafield[@tag='084']")
    df970 = bib_element.find("./datafield[@tag='970']")
    for df082a in bib_element.findall("./datafield[@tag='082']/subfield[@code='a']"):
        dewey = df082a.text[:3]
        if (bk_list := ddc_to_bk.get(dewey)) and df084 is None:
            update_flag = True
            for bk in bk_list:
                bib_element.append(
                    gen_datafield(
                        "084",
                        " ",
                        " ",
                        [
                            ("a", bk),
                            ("9", "Automatisch generiert aus Konkordanz DDC-BK (UBG)"),
                            ("2", "bkl"),
                        ],
                    )
                )
        if (obv_list := ddc_to_obv.get(dewey)) and df970 is None:
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
