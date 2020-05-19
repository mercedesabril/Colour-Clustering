######################################################
##													##
##	To perform color analysis on multiple images	##
##													##
######################################################

from color_analysis import *

from os import walk

folder = "Imgs"

f = []
for (dirpath, dirnames, filenames) in walk(folder):
    f.extend(filenames)
    break 

for i in filenames:
    print(i)
    fullpath = os.path.join(dirpath, i)
    Imagen = ImageAnalizer(fullpath)
    Imagen.RGB_composite()
    Imagen.RGB_graph()
    maxclusters = 30
    clusters = ElbowCurve(maxclusters, Imagen.pixel_values)
    Imagen.Color_palette(clusters)
    SaveClustersInfo(Imagen.name, Imagen.colors, Imagen.pixel_label, Imagen.total_pixels)

