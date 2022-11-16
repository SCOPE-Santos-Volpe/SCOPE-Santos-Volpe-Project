import json
  
# Opening JSON file
f = open('county.json')
  
# returns JSON object as dictionary
data = json.load(f)

state_codes = {
    'AL': '01', 'AK': '02', 'AZ': '04', 'AR': '05', 'CA': '06', 'CO': '08',
    'CT': '09', 'DE': '10', 'DC': '11', 'FL': '12', 'GA': '13', 'HI': '15',
    'ID': '16', 'IL': '17', 'IN': '18', 'IA': '19', 'KS': '20', 'KY': '21',
    'LA': '22', 'ME': '23', 'MD': '24', 'MA': '25', 'MI': '26', 'MN': '27',
    'MS': '28', 'MO': '29', 'MT': '30', 'NE': '31', 'NV': '32', 'NH': '33', 
    'NJ': '34', 'NM': '35', 'NY': '36', 'NC': '37', 'ND': '38', 'OH': '39',
    'OK': '40', 'OR': '41', 'PA': '42', 'RI': '44', 'SC': '45', 'SD': '46',
    'TN': '47', 'TX': '48', 'UT': '49', 'VT': '50', 'VA': '51', 'WA': '53', 
    'WV': '54', 'WI': '55', 'WY': '56', 'AS': '60', 'GU': '66', 'MP': '69',
    'PR': '72', 'VI': '78'
}

for key in state_codes.keys():
    int_code = int(state_codes[key])
    state_codes[key]= int_code

res = dict((v,k) for k,v in state_codes.items())

state_dict = {}
# print(data["features"])
  
# Iterating through the json list
for i, county in enumerate(data['features']):
    statefp = int(county["properties"]["STATEFP"])
    #json_object = json.dumps(data['features'][i])
    if(statefp not in state_dict):
        state_dict[statefp] = []
    state_dict[statefp].append(data['features'][i])

for key in state_dict.keys():
    string = "{\"type\":\"FeatureCollection\",\"name\":\"cb_2018_us_county_5m\",\"features\":" + json.dumps(state_dict[key]) + "}"

    code_to_state = res[key]
    with open(f"county_{code_to_state}.geojson", "w") as outfile:
        outfile.write(string)

# Closing file
f.close()