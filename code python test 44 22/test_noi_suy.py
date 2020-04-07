import json
import urllib
import requests
import math
import test_data_44_22
import all_even_housenumbers

def distance(lat1, lon1, lat2, lon2):
    if (lat1 == lat2) and (lon1 == lon2):
        return 0
    else:
        radlat1 = math.pi * lat1 / 180
        radlat2 = math.pi * lat2 / 180
        theta = lon1 - lon2
        radtheta = math.pi * theta / 180
        dist = math.sin(radlat1) * math.sin(radlat2) + math.cos(radlat1) * math.cos(radlat2) * math.cos(radtheta)
        if dist > 1:
            dist = 1
        dist = math.acos(dist)
        dist = dist * 180 / math.pi
        dist = dist * 60 * 1.1515
        return dist * 1.609344 * 1000
        
pass_count = 0
total = 0

# write distance into result file 
with open("interpolation_result.js", "a") as result_file:
    result_file.write('const interpolation_data = {"type":"FeatureInterpolation","features": [')
    for each_test in test_data_44_22.test_datas:
        total += 1
        housenumber = each_test["housenumber"]
        results = requests.get(f'http://localhost:3000/search/geojson?lat=21.036&lon=105.785&number={housenumber}&street=Xuan%20Thuy').json()
        result = results['features'][0]
        lat1 = result['properties']['lat']
        lon1 = result['properties']['lon']
        lat2 = float(each_test['real_lat'])
        lon2 = float(each_test['real_lon'])
        result_file.write(str(result)+", ")
        #check pass test
        devia = math.inf
        if devia > distance(lat1, lon1, lat2, lon2):
            devia = round(distance(lat1, lon1, lat2, lon2) * 100) / 100
            if devia <= 20.0:
                print("PASS")
                pass_count += 1
            else:
                print("FAIL")
    result_file.write(']}')
    result_file.close()
    
print(pass_count)
print(total)                
