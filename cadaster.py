# http://www.catastro.meh.es/servicios/wms/wms.htm

from owslib.wms import WebMapService  # https://geopython.github.io/OWSLib/
import json
import math

endpoint = "http://ovc.catastro.meh.es/Cartografia/WMS/ServidorWMS.aspx"

extent = [-math.pi * 6378137, math.pi * 6378137]

def xyzToBounds(x, y, z):
    tileSize = (extent[1] * 2) / math.pow(2, z)
    minx = extent[0] + x * tileSize
    maxx = extent[0] + (x + 1) * tileSize
    # remember y origin starts at top
    miny = extent[1] - (y + 1) * tileSize
    maxy = extent[1] - y * tileSize
    return (minx, miny, maxx, maxy)


# http://www.catastro.meh.es/servicios/wms/wms.htm
wms = WebMapService(endpoint, version='1.1.1')
print(wms.identification.abstract)

print("LAYERS:")
jlayers = json.dumps(list(wms.contents), indent=2)
with open('layers.json', 'w') as layers:
    layers.write(jlayers)

print(jlayers)
operations = [op.name for op in wms.operations]
for op in operations:
    print(op+":")
    print("-", wms.getOperationByName(op).methods)
    print("-", wms.getOperationByName(op).formatOptions)

# box = xyzToBounds(42.034232, 2.804443, 18)
box = xyzToBounds(133111, 97277, 18)
print(box)

srs = 'EPSG:3857'
format = 'png'
size = (500, 500)

info = wms.getfeatureinfo(
    layers=['Catastro'],
    srs=srs,
    bbox=box,
    size=size,
    format='image/jpeg',
    query_layers=['Catastro'],
    info_format="text/html",
    xy=(int(size[0]/2), int(size[1]/2)))

out = open('info.html', 'wb')
out.write(info.read())
out.close()

img = wms.getmap(layers=['Catastro'],
                 styles=['Default'],
                 bbox=box,
                 srs=srs,
                 size=size,
                 format='image/'+format,
                 transparent=True)
out = open('test.'+format, 'wb')
out.write(img.read())
out.close()

