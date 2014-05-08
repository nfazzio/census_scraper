import requests
from census import Census

api_key = open('api_key.txt').read().rstrip()

def main():
    
    c = Census("5e9aade56a78e9f799fafdd313b7c258d8b40ccd")
    c.acs.get(('NAME', 'B25034_010E'), {'for': 'state:%s' % states.MD.fips})
    #api_url = "http://api.census.gov/data/2010/sf1"
    #payload = {'key': api_key,
    #           'get': 'P0010001,NAME',
    #           'for': 'county:*',
    #           'in': 'state:*'}
    #r = requests.get(api_url, params=payload)
    #print r.url
    #print r.text



if __name__ == "__main__":
    main()
