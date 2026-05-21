import json
from read_gipfel_koordinaten import read_gipfel_koordinaten
from gemeinde import get_gemeinden
from kanton import get_kantone
from hoehen_koordinaten import get_hoehen_koordinaten
from orthophoto import get_ortho_url
from profil import get_profil
from gebietsname import get_gebietsname

data = read_gipfel_koordinaten()
data_count = data.shape[0]

gemeinden = get_gemeinden(data)
kantone = get_kantone(data)
hoehen_koordinaten = get_hoehen_koordinaten(data)
orthophoto = get_ortho_url(data)
profil = get_profil(data)
gebietsname = get_gebietsname(data)

liste = []
for i in range(data_count):
    row = data.iloc[i]
    alle = {"name": row["Name"]}
    alle = alle | hoehen_koordinaten[i] | kantone[i] | gemeinden[i] | gebietsname[i] | orthophoto[i] | profil[i]
    liste.append(alle)

with open('./data/gipfel-daten.json', 'w', encoding='utf8') as fp:
    json.dump(liste, fp, indent=2, ensure_ascii=False)
