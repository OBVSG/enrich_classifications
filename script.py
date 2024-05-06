from argparse import ArgumentParser
from pathlib import Path
import xml.etree.ElementTree as ET
import enrich_cls

parser = ArgumentParser(
    description="Enrich BK and OBV Fachgruppe for Marc Records on Basis of DDC"
)
parser.add_argument(
    "input_xml", type=Path, help="File containing the MARCXML Data. No namespaces!"
)
parser.add_argument("output_xml", type=Path, help="File to write the output.")
parser.add_argument(
    "ddc_bk_csv", type=Path, help="File to with csv mappping table ddc bk"
)
parser.add_argument(
    "ddc_obv_csv", type=Path, help="File to with csv mappping table ddc obv"
)

args = parser.parse_args()
tree = ET.parse(args.input_xml)

ddc_bk_map = enrich_cls.create_notation_map(args.ddc_bk_csv)
ddc_obv_map = enrich_cls.create_notation_map(args.ddc_obv_csv)
result_collection = ET.Element("collection")

for record in tree.getroot():
    new_bib = enrich_cls.enrich_bib(
        record, ddc_to_bk=ddc_bk_map, ddc_to_obv=ddc_obv_map
    )
    if new_bib:
        result_collection.append(new_bib)

result_tree = ET.ElementTree(result_collection)
result_tree.write(args.output_xml, encoding="utf-8", xml_declaration=True)
