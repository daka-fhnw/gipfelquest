import json
from read_gipfel_koordinaten import read_gipfel_koordinaten
from gemeinde import get_gemeinden
from kanton import get_kantone
from hoehen import get_hoehen
from orthophoto import get_ortho_url
from profil import get_profil

data = read_gipfel_koordinaten()
data_count = data.shape[0]

gemeinden = get_gemeinden(data)
kantone = get_kantone(data)
hoehen = get_hoehen(data)
orthophoto = get_ortho_url(data)
profil = get_profil(data)

liste = []
for i in range(data_count):
    alle = gemeinden[i] | kantone[i] | hoehen[i] | orthophoto[i] | profil[i]
    alle["name"] = data["Name"].iloc[i]
    liste.append(alle)

with open('./data/gipfel-daten.json', 'w') as fp:
    json.dump(liste, fp, indent=2)
