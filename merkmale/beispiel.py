from read_gipfel_koordinaten import read_gipfel_koordinaten

def get_beispiel_merkmal(data):
    liste = []
    for row in data.itertuples():
        name = row.Name
        easting = row.geometry.x
        northing = row.geometry.y
        # spezifischer Code
        liste.append({
            # z.B. Gebietsname, Profilkoordinaten, ...
            "property1": 1,
            "property2": 2,
        })
    return liste

if __name__ == "__main__":
    data = read_gipfel_koordinaten()
    liste = get_beispiel_merkmal(data)
    print(liste)
