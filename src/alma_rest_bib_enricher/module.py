from argparse import ArgumentParser
from os.path import basename
import glob
import requests
import xml.etree.ElementTree as ET
from enrich_cls import create_notation_map, download_concordance, enrich_bib


def main():
    parser = ArgumentParser(
        description="Enrich BK and OBV Fachgruppe for Marc Records on Basis of DDC"
    )
    parser.add_argument(
        "input_xml_dir",
        type=str,
        help="Input directory containing xmls of alma bib api objects",
    )
    parser.add_argument(
        "output_xml_dir",
        type=str,
        help="Output directory to write enriched marc xml files to",
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

    for xml_file in glob.glob(f"{args.input_xml_dir}*.xml"):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        marcrecord = root.find("./record")
        new_marcrecord = enrich_bib(
            marcrecord, ddc_to_bk=ddc_bk_map, ddc_to_obv=ddc_obv_map, namespace_uri = None
        )
        if new_marcrecord:
            marcrecord = new_marcrecord
            ET.indent(tree)
            tree.write(
                f"{args.output_xml_dir}{basename(xml_file)}",
                encoding="utf-8",
                xml_declaration=True,
            )
            counter += 1

    print(f"Enriched {counter} records")


if __name__ == "__main__":
    main()
