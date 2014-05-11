from census import Census
import csv
import time
import os

def main():
    c = Census("5e9aade56a78e9f799fafdd313b7c258d8b40ccd")
    fields = ['B01001_007E','B01001_023E', 'B06011_001E']
    out_file_path = initialize_output('test')

    with open('zip_code_database.csv', 'r') as in_file, \
         open(out_file_path, 'w') as out_file:
        reader = csv.DictReader(in_file)
        header = get_header(fields, reader, c)
        writer = csv.DictWriter(out_file, header, delimiter='\t')
        writer.writeheader()
        for counter,row in enumerate(reader):
            print counter
            results = c.acs5.zipcode(','.join(fields), row['zip'])
            if results != []:
                results = results[0]
            if isinstance(results, dict):
                writer.writerow(dict(row.items() + results.items()))
            else:
                writer.writerow(row)

def initialize_output(file_name):
    """ Boilerplate for making the output file. """
    output_dir = os.path.abspath('output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    datetime = time.strftime("%Y%m%d%H%M%s")
    out_file_path = os.path.normpath(os.path.join(output_dir, datetime+"_"+
                                                     file_name+".tsv"))
    return out_file_path

def get_header(fields, reader, c):
    """ Combines dictionary keys from an api request as well as the original
    zip_database file to make a consistent header for output file
    """

    query_result = c.acs5.zipcode(fields, '02035')
    header = query_result[0].keys() + reader.fieldnames
    return header

if __name__ == "__main__":
    main()
