import json

f = open('mpo_boundaries.json')
data = json.load(f)
states = {}
  
# Iterating through the json list
for mpo in data['features']:
    print(mpo["properties"]["MPO_NAME"], "--", mpo["properties"]["STATE"])
    # print(mpo["properties"])

    # if mpo["properties"]["STATE"] in states:
    #     states[mpo["properties"]["STATE"]].append(mpo)
    # else:
    #     states[mpo["properties"]["STATE"]] = [mpo]

    dump = json.dumps(mpo)
    # print(dump[0:100])
    if mpo["properties"]["STATE"] in states:
        states[mpo["properties"]["STATE"]].append(dump)
    else:
        states[mpo["properties"]["STATE"]] = [dump]

f.close()

print(states.keys())

# states = {"testState" : states["AK"]}

for k,v in states.items():
    text_file = open("mpo_boundaries_by_state/mpo_" + k + ".geojson", "w")

    file_text = "{\"type\":\"FeatureCollection\",\"name\":\"MPO_Boundary_01072022" + k + "\",\"crs\":{\"type\":\"name\",\"properties\":{\"name\":\"urn:ogc:def:crs:EPSG::4269\"}},\"features\":"
    file_text += "["
    for i in v:
        file_text += i + ","
    file_text = file_text[:-1] + "]}"

    n = text_file.write(file_text)
    text_file.close()
