from owslib.wms import WebMapService
from owslib.util import ResponseWrapper
import geopandas as gpd
import pandas as pd
import warnings

warnings.filterwarnings("ignore")
warnings.simplefilter("ignore")

data = pd.read_csv('data/gipfel-koordinaten.csv')
data = gpd.GeoDataFrame(data, 
    geometry=gpd.points_from_xy(data['easting'], data['northing']),
    crs='EPSG:2056'
)

liste = []

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

wms = WebMapService(GEOADMIN_WMS_URL)


for row in data.itertuples():
    name = row.name
    easting = row.easting
    northing = row.northing
   
    coord = easting, northing
    response = get_image_from_center(wms, coord)
    url = response.geturl()

    liste.append({
        #WMS Link
        "WMS URL": url,
    })

print(liste)
