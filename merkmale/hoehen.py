from read_gipfel_koordinaten import read_gipfel_koordinaten

def get_koordinaten_hoehe_merkmal(data):
    liste = []
    for row in data.itertuples():
        easting = int(round(row.geometry.x, 0))
        northing = int(round(row.geometry.y, 0))
        elevation = int(round(row.Hoehe, 0))
        # spezifischer Code
        liste.append({
            # z.B. Gebietsname, Profilkoordinaten, ...
            "easting": easting,
            "northing": northing,
            "elevation": elevation
        })
    return liste
    


if __name__ == "__main__":
    data = read_gipfel_koordinaten()
    liste = get_koordinaten_hoehe_merkmal(data)
    print(liste)