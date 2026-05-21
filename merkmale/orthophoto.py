import warnings
from owslib.wms import WebMapService
from owslib.util import ResponseWrapper
from read_gipfel_koordinaten import read_gipfel_koordinaten

warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

GEOADMIN_WMS_URL = "https://wms.geo.admin.ch"
SWISSIMAGE_LAYER = "ch.swisstopo.swissimage"

def get_image_from_center(wms: WebMapService, 
                          xy_lv95: tuple[float, float], 
                          radius_m: int = 2000, 
                          size_px: int = 512) -> ResponseWrapper:
    minx = xy_lv95[0] - radius_m
    maxx = xy_lv95[0] + radius_m
    miny = xy_lv95[1] - radius_m
    maxy = xy_lv95[1] + radius_m
    response = wms.getmap(
        layers=[SWISSIMAGE_LAYER],
        styles=["default"],
        srs="EPSG:2056",
        bbox=(minx, miny, maxx, maxy),
        size=(size_px, size_px),
        format="image/png",
        transparent=False,
    )
    return response

def get_ortho_url(data):
    liste = []
    wms = WebMapService(GEOADMIN_WMS_URL)
    for row in data.itertuples():
        easting = row.geometry.x
        northing = row.geometry.y

        coord = (easting, northing)
        response = get_image_from_center(wms, coord)
        url = response.geturl()

        liste.append({
            "ortho_url": url,
        })
    return liste

if __name__ == "__main__":
    data = read_gipfel_koordinaten()
    liste = get_ortho_url(data)
    print(liste)
