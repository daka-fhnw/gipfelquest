from read_gipfel_koordinaten import read_gipfel_koordinaten

def get_region(data):
    liste = []
    for row in data.itertuples():
        region = row.Region
        liste.append({
            "region": region
        })
    return liste

if __name__ == "__main__":
    data = read_gipfel_koordinaten()
    liste = get_region(data)
    print(liste)