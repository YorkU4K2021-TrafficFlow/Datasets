import pandas as pd
import osmapi as osm


# url = 'https://www.openstreetmap.org/api/0.6/way/'+str(way_id)+'/full'
csv_file_name = 'movement-speeds-hourly-new-york-2020-1.csv'

def check_num_eligible():
    global csv_file_name

    api = osm.OsmApi()
    counter = 0

    file = pd.read_csv(csv_file_name)
    g = file['osm_way_id'].values
    print(len(g))
    g = set(g)
    print(len(g))

    for node_id in g:
        try:
            node = api.NodeGet(node_id)
        except Exception as e:
            # in history - deleted
            try:
                node = api.NodeHistory(node_id)

            except Exception as ee:
                print(node_id)
                counter += 1

    api.close()

    print(counter)




lat1 = []
long1 = []
lat2 = []
long2 = []

file = pd.read_csv(csv_file_name)
g = file['osm_way_id'].values
print(len(g))
g = list(set(g))
print(len(g))

api = osm.OsmApi()
couter = 1

for way_id in g:
    print(couter)
    couter += 1
    try:
        node = api.WayFull(way_id)
        lat1.append(node[0]['data']['lat'])
        long1.append(node[0]['data']['lon'])

        lat2.append(node[1]['data']['lat'])
        long2.append(node[1]['data']['lon'])

    except Exception as e:
        lat1.append(None)
        long1.append(None)

        lat2.append(None)
        long2.append(None)

api.close()

X = pd.DataFrame({'osm_way_id': g, 'latitude1':lat1, 'longitude1': long1, 'latitude2':lat2, 'longitude2': long2})

Y = pd.merge(file, X, on='osm_way_id')
Y.to_csv(csv_file_name, index=False)
