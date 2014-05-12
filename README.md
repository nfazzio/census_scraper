A tool for collecting census fields for the US on a zipcode bases.

Before running:

1) Install Sunlight Lab's Census package
``` pip install git+https://github.com/sunlightlabs/census.git ```

2) Obtain a Census API key http://www.census.gov/developers/tos/key_request.html and store it in a file. The program defaults to reading from api_key.txt, but you can designate a different file with the -k option.

3) Obtain a csv of US zipcodes. The script is tailored to interpret the list provided here http://www.unitedstateszipcodes.org/zip-code-database/. The script defaults to read from zip_code_database.csv, but you can specify a different file with the -i option.

4) ```python census_scraper.py```

```
python census_scraper.py -h
usage: census_scraper.py [-h] [-i INFILE] [-o OUTFILE] [-f FIELDS]
                                   [-k KEY]

optional arguments:
  -h, --help            show this help message and exit
  -i INFILE, --infile INFILE
                        provide the path of the infile csv
  -o OUTFILE, --outfile OUTFILE
                        provide a name for the outfile tsv
  -f FIELDS, --fields FIELDS
                        provide the path of the fields to retrieve
  -k KEY, --key KEY     path for .txt with api key
  
```
