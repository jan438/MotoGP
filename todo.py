import svgutils.transform as sg
from svgpathtools import parse_path

fig = sg.fromfile('smile.svg')
mouth = fig.find_id('path1069')

# scaling
factor = 1.25
mouth.scale(factor)

# dirty-ish capture of path data
path = mouth.tostr().decode().lower().split(' d="')[1].split('" ')[0]

# cleaner capture of path data https://stackoverflow.com/a/41187226
import lxml.etree as ET
svg = ET.parse('smile.svg')
# using * because can't figure out namespaces https://stackoverflow.com/a/56936158/188159
path = svg.xpath('//*[@id = "path1069"]')[0].attrib['d']

# coordinates of the path's bounding box https://stackoverflow.com/a/38297053
xmin, xmax, ymin, ymax = parse_path(path).bbox()

# width/height calc
w = xmax - xmin
h = ymax - ymin

# center point calc
cx = xmin + w/2
cy = ymin + h/2

# diff between original/new center points
x = cx - cx * factor
y = cy - cy * factor

#correctional movement
mouth.moveto(x,y)

fig.save('smile-scale_and_move.svg')
