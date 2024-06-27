from argparse import ArgumentParser
from pathlib import Path
import requests
import xml.etree.ElementTree as ET
from enrich_cls import create_notation_map, download_concordance, enrich_bib


def main():
    parser = ArgumentParser(
        description="Enrich BK and OBV Fachgruppe for Marc Records in a Marc XML File including the Namespace URI http://www.loc.gov/MARC21/slim"
    )
    parser.add_argument(
        "input_marc_xml_file",
        type=Path,
        help="Input Marc XML File containing Marc record elements under one root element",
    )
    parser.add_argument(
        "output_marc_xml_file",
        type=Path,
        help="Output file to write enriched Marc XML data to",
    )

    args = parser.parse_args()

    DDC_BK_ID = "ddc-bk-1000-ubg"
    DDC_OBV_ID = "ddc-obv"

    with requests.Session() as s:
        ddc_bk_concordance = download_concordance(s, DDC_BK_ID)
        ddc_obv_concordance = download_concordance(s, DDC_OBV_ID)

    ddc_bk_map = create_notation_map(ddc_bk_concordance)
    ddc_obv_map = create_notation_map(ddc_obv_concordance)

    print(
        f"Downloaded {len(ddc_bk_map)} mappings for BK and {len(ddc_obv_map)} mappings for OBV"
    )

    counter = 0
    tree = ET.parse(args.input_marc_xml_file)
    root = tree.getroot()
    ET.register_namespace("marc", "http://www.loc.gov/MARC21/slim")

    for marcrecord in root:
        new_marcrecord = enrich_bib(
            marcrecord, ddc_to_bk=ddc_bk_map, ddc_to_obv=ddc_obv_map
        )
        if new_marcrecord:
            marcrecord = new_marcrecord
            counter += 1
    
    tree.write(
        f"{args.output_marc_xml_file}",
        encoding="utf-8",
        xml_declaration=True,
    )

    print(f"Enriched {counter} records")


if __name__ == "__main__":
    main()
