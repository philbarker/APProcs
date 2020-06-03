Testing the viability of the [DCMI AP](https://github.com/dcmi/dcap) CSV format.

Will read *a* csv file that specifies an application profile and store as a complex python dictionary, and optionally print a representation of the python dict, or (partially) convert the dict to [YAMA](https://nishad.github.io/yama/spec/latest/) or [ShExJ](https://shex.io/) and print that.

When I say "*a* csv file...", I mean the one in [/input/ap_bookclub.csv](https://github.com/philbarker/APProcs/blob/master/input/ap_bookclub.csv). Trying with any other will likely find a bug.

Example output: [raw](https://github.com/philbarker/APProcs/blob/master/output/raw_bookclub.txt), [shexj](https://github.com/philbarker/APProcs/blob/master/output/shexj_bookclub.txt), [yama](https://github.com/philbarker/APProcs/blob/master/output/yama_bookclub.txt)

Also, [shexc](https://github.com/philbarker/APProcs/blob/master/output/shexj_bookclub.txt) generated from the schexj using the [shexSpec webap](https://rawgit.com/shexSpec/shex.js/extends/packages/shex-webapp/doc/shex-simple.html)

# Usage
main.py [-h] [-d DUMP] [-y YAMA] [-s SHEX] infile

Read an application profile from simple csv file and output some RDFS for the profile.

positional arguments:
  infile                input file name of Application Profile csv

optional arguments:
  -h, --help            show this help message and exit
  -d DUMP, --dump DUMP  Dump (print) the AP once loaded
  -y YAMA, --yama YAMA  Convert and dump (print) the AP as YAMA
  -s SHEX, --shex SHEX  Convert and dump (print) the AP as YAMA
