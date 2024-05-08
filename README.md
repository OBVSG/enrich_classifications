# Enrich Classifications

Marc XML Bibliographic Records of E-Books often come Dewey Classification. Based on concordances

https://coli-conc.gbv.de/api/concordances/ddc-obv
https://coli-conc.gbv.de/api/concordances/ddc-bk-1000-ubg

one can enrich BK and OBV Classifcation for a given Marc XML <record/> Element.

# Usage `script_alma_js.py`

There is a `-h` switch to print a how-to-use message:

`python script_alma_js.py -h`

## Execution
`python script_alma_js.py input_folder/ output_folder/`

The input_folder should contain XML Files of [Alma APIs Rest Bib Objects](https://developers.exlibrisgroup.com/alma/apis/docs/xsd/rest_bib.xsd/?tags=GET)

The output_folder is used to write the enriched Bib Objects into it for API updates.
