from argparse import ArgumentParser
from pathlib import Path
from os.path import basename
import glob
import xml.etree.ElementTree as ET
import enrich_cls

parser = ArgumentParser(
    description="Enrich BK and OBV Fachgruppe for Marc Records on Basis of DDC"
)
parser.add_argument(
    "input_xml_dir", type=str, help="Input directory containing xmls of alma bib api objects"
)
parser.add_argument(
    "output_xml_dir", type=str, help="Output directory to write files to"
)
parser.add_argument(
    "ddc_bk_csv", type=Path, help="File to with csv mappping table ddc bk"
)
parser.add_argument(
    "ddc_obv_csv", type=Path, help="File to with csv mapping table ddc obv"
)

args = parser.parse_args()

ddc_bk_map = enrich_cls.create_notation_map(args.ddc_bk_csv)
ddc_obv_map = enrich_cls.create_notation_map(args.ddc_obv_csv)

for xml_file in glob.glob(f"{args.input_xml_dir}*.xml"):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    marcrecord = root.find("./record")
    new_marcrecord = enrich_cls.enrich_bib(marcrecord, ddc_to_bk=ddc_bk_map, ddc_to_obv=ddc_obv_map)
    if new_marcrecord:
        marcrecord = new_marcrecord
        ET.indent(tree)
        tree.write(f"{args.output_xml_dir}{basename(xml_file)}", encoding="utf-8", xml_declaration=True)