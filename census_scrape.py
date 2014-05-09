import requests
from census import Census
from us import states
import csv
import os
import json
import pprint
import time

api_key = open('api_key.txt').read().rstrip()

def main():
    
    c = Census("5e9aade56a78e9f799fafdd313b7c258d8b40ccd")    
    conversions = load_tract_conversions()
    
    fields = ['B01001_007E','B01001_023E', 'B06011_001E']
    # Do it on all the states
    results = []
    for state in states.STATES_AND_TERRITORIES:
        print state.fips
        query_results = retrieve_fields(fields, state.fips, c)
        print query_results
        for result in query_results:
            results.append(result)
    for i in range(1,5):
        print results[i]
    results = add_zip(results, conversions)
    results = add_readable_state(results)

    # Test for one state
    '''
    results = retrieve_fields(fields, '51', c)
    results = add_zip(results, conversions)
    results = add_readable_state(results)
    print results[0]
    '''
    write_tsv(results, 'test')


def retrieve_fields(fields, state, c, level='tract'):
    """ Returns list of dicts value of field values at the tract level for the
    state provided.

    fields -- list of fields to retrieve (up to 50).
    state -- name of state to retrieve fields from.
    c -- census object
    level -- resolution of area to retrieve fields.
    """
    fields = ",".join(fields)
    return c.acs5.get(('NAME', fields),
                      {'for': level+":*",
                       'in': 'state:%s' % state})

def add_zip(dicts, conversions):
    """ Inserts the zip5 value to the dictionaries provided. The value is found
    in the provided conversions dict.
    """
    for d in dicts:
        try:
            tract11 = d['state']+d['county']+d['tract']
            d['zip5'] = conversions[tract11]
        except(KeyError):
            print "Tract not found in conversions reference: " + tract11
    return dicts

def add_readable_state(dicts):
    """ Inserts the two letter state abbreviation to the provided dicts """
    for d in dicts:
        d['state_readable'] = str(states.lookup(d['state']))
    return dicts

def load_tract_conversions():
    """ Returns a dict with key=tract, value=zip5. Note that tract->zip5 is
    many-to-many, but the geographic areas are very proximate. Since this is
    a hash, the zip5 of the last tract inserted will be used.
    """
    tract_to_zip = {}
    with open('ZIP_TRACT_092013.csv', 'r') as f:
        c = csv.reader(f, delimiter=',')
        for row in c:
            tract_to_zip[row[1]] = row[0]
    return tract_to_zip

def write_tsv(dicts, file_name):
    """TODO
    Creates a DictWriter that writes output tsv"""
    output_dir = os.path.abspath('output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    date = time.strftime("%Y%m%d")
    fieldnames = dicts[0].keys()
    tsv_out = open(os.path.normpath(os.path.join(output_dir, date+"_"+
                                                     file_name+".tsv")), 'wb')
    tsv_writer = csv.DictWriter(tsv_out, fieldnames, delimiter='\t')
    tsv_writer.writeheader()
    for dictionary in dicts:
        print dictionary
        tsv_writer.writerow({k:(v.encode('utf8') if v is not None else v)
            for k,v in dictionary.items()})


if __name__ == "__main__":
    main()
