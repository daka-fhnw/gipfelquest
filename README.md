# gipfelquest

## Kurzbeschreibung

Im Spiel "gipfelquest" besteht die Möglicheit ihr Bergwissen zu testen. Ziel ist aus unzähligen Bergen mit Höhenprofilen, Koordinaten, Kanton, Karte und Orthophoto unter Zeitdruck und Punktabzug pro benötigter Hilfe die höchst mögliche Punktzahl zu erreichen.

## Preview

hier ein Bild der Oberfläche einfügen

## Conda

`conda create -n hackathon python=3.14 streamlit requests numpy matplotlib geopandas rasterio fiona owslib -c conda-forge`

`conda activate hackathon`

## Dokumentationen

- https://docs.streamlit.io/
- https://geopandas.org/en/stable/docs.html
- https://pandas.pydata.org/docs/
- https://shapely.readthedocs.io/en/stable/
- https://owslib.readthedocs.io/en/latest/
- https://numpy.org/doc/2.4/

## Datenquellen

### WMS swisstopo

- https://wms.geo.admin.ch
- https://wms.geo.admin.ch/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities

### API GeoAdmin Profile

- https://docs.geo.admin.ch/access-data/get-elevation-profile.html

### swissBOUNDARIES3D:

- https://www.swisstopo.admin.ch/de/landschaftsmodell-swissboundaries3d

### swissNAMES3D:

- https://www.swisstopo.admin.ch/de/landschaftsmodell-swissnames3d

### Liste Berggipfel:

- http://zirbitzkogel.at/blog/wp-content/uploads/2019/08/kmz/mountain_peaks_ALPS.kmz
