# Enrich Classifications

Marc XML Bibliographic Records of E-Books often come with a Dewey Classification. Based on concordances

https://coli-conc.gbv.de/api/concordances/ddc-obv

https://coli-conc.gbv.de/api/concordances/ddc-bk-1000-ubg

one can enrich BK and OBV Classification for a given Marc XML `<record/>` Element.

# Installation

* You can use [pipx](https://pipx.pypa.io/stable/installation/) to make this available from a local clone:

* From the repo root directory execute `pipx install .`


# Usage 

There is a `-h` switch for `alma_rest_bib_enricher` to print a how-to-use message:

`alma_rest_bib_enricher -h`

## Execution
`alma_rest_bib_enricher input_folder/ output_folder/`

The input_folder should contain XML Files of [Alma APIs Rest Bib Objects](https://developers.exlibrisgroup.com/alma/apis/docs/xsd/rest_bib.xsd/?tags=GET)

The output_folder is used to write the enriched Bib Objects into it for API updates.
