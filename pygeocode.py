# These functions use the postcodes.io api to lookup single and bulk postcodes and
# return their geocode (latitude and longitude)

import requests
import json
import configparser

#Parse Config File
config = configparser.ConfigParser()
config.read('config.ini')

api_url_base = config['postcodes.io']['api_url_base']
postcode_lookup_endpoint = config['postcodes.io']['postcode_lookup_endpoint']

# build and format endpoint URL
postcode_lookup_url = '{0}/{1}'.format(api_url_base, postcode_lookup_endpoint)

# Define request headers
headers = {'Content-Type': 'application/json'}


# lookup and return geocode for single postcode.
# args: str postcode
# returns: tuple (longitude, latitude)
def geocode_by_postcode(postcode):
    # Make API call using endpoint URL for postcodes lookup
    response = requests.get(postcode_lookup_url + postcode)

    # If successful request then parse response, extract longitude and latitude from response
    # else return None
    if response.status_code == 200:
        parsed_response = json.loads(response.content.decode('utf-8'))
        longitude = parsed_response['result']['longitude']
        latitude = parsed_response['result']['latitude']
        return (longitude, latitude)
    else:
        return None

# lookup and return geocodes for array of postcodes.
# args: [str] postcodes
# returns: [dict] [{"query": postcode, "geocode": (longitude, latitude)}]
def bulk_geocode_by_postcode(postcodes):
    # build request body, add array of postcodes
    body = json.dumps({"postcodes": postcodes})

    # Make API call using endpoint URL for postcodes lookup. Provides headers and request body
    response = requests.post(postcode_lookup_url,headers=headers, data=body)

    # If successful request then parse response then for each postcode extract longitude and latitude from response
    # else return None
    if response.status_code == 200:
        parsed_response = json.loads(response.content.decode('utf-8'))
        results = parsed_response['result']
        geocodes = []
        for result in results:
            query = result['query']
            longitude = result['result']['longitude']
            latitude = result['result']['latitude']
            geocodes.append({"query": query, "geocode": '{0},{1}'.format(longitude, latitude)})
        return geocodes
    else:
        return None

# Test Code

in_postcode = "BD89PN"

bulk_in_postcodes = ["BD89PN", "BD88DJ"]

print(geocode_by_postcode(in_postcode))

print(bulk_geocode_by_postcode(bulk_in_postcodes))