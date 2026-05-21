from read_gipfel_koordinaten import read_gipfel_koordinaten

def get_hoehen_koordinaten(data):
    liste = []
    for row in data.itertuples():
        easting = int(round(row.geometry.x, 0))
        northing = int(round(row.geometry.y, 0))
        elevation = int(round(row.Hoehe, 0))
        liste.append({
            "koordinate_x": easting,
            "koordinate_y": northing,
            "hoehe": elevation,
        })
    return liste

if __name__ == "__main__":
    data = read_gipfel_koordinaten()
    liste = get_hoehen_koordinaten(data)
    print(liste)
