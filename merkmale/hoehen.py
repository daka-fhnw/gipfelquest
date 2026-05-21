from read_gipfel_koordinaten import read_gipfel_koordinaten

def get_koordinaten_hoehe_merkmal(data):
    liste = []
    for row in data.itertuples():
        elevation = int(round(row.Hoehe, 0))
        liste.append({
            "hoehe": elevation
        })
    return liste

if __name__ == "__main__":
    data = read_gipfel_koordinaten()
    liste = get_koordinaten_hoehe_merkmal(data)
    print(liste)
