from census import Census
import csv
import time
import os
import argparse

def main():
    args = get_args()
    api_key = open(args.key).read().rstrip()
    print args
    c = Census(api_key)
    fields = open(args.fields).read().rstrip().strip().split(',')
    print fields
    #['B01001_007E','B01001_023E', 'B06011_001E']
    out_file_path = initialize_output(args.outfile)

    with open(args.infile, 'r') as in_file, \
         open(out_file_path, 'w') as out_file:
        reader = csv.DictReader(in_file)
        print str(fields) + '\n' + str(reader) +'\n' + str(c)
        header = get_header(fields, reader, c)
        writer = csv.DictWriter(out_file, header, delimiter='\t')
        writer.writeheader()
        for counter,row in enumerate(reader):
            print counter
            results = c.acs5.zipcode(','.join(fields), row['zip'])
            # For successful api call, set results to content of returned list.
            # Write the ombined results of the api call and the reference csv.
            if results != []:
                results = results[0]
                writer.writerow(dict(row.items() + results.items()))
            # Else, just rewrite the row from reference csv.
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

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', default = 'zip_code_database.csv',
                        help="provide the path of the infile csv")
    parser.add_argument('-o', '--outfile', default = 'test',
                        help="provide a name for the outfile tsv")
    parser.add_argument('-f', '--fields', default = "fields.csv",
                        help = "provide the path of the fields to retrieve")
    parser.add_argument('-k', '--key', default = "api_key.txt",
                        help = "path for .txt with api key")
    args = parser.parse_args()
    return args
if __name__ == "__main__":
    main()
