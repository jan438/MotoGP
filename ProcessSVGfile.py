import sys
from svgpathtools import svg2paths, wsvg
from svgpathtools import parse_path, Path, Line, CubicBezier
from reportlab.lib.units import inch, mm
import lxml.etree as ET
import warnings

def flip_svg_path_vertically(input_svg, output_svg, pathid):
    try:
        circuit = ET.parse(input_svg)
        root = circuit.getroot()
        for tag in root.iter():
            if not len(tag):
                print ("tag", tag.tag, tag.text)
        nsmap = {'svg': 'http://www.w3.org/2000/svg'}
        xpaths = root.findall('.//svg:path', namespaces=nsmap)
        svg_height = root.get("height")
        measurement = svg_height[len(svg_height) - 2:]
        if measurement == "mm" or measurement == "cm" or measurement == "in" or measurement == "px" or measurement == "pt":
            svg_height = float(svg_height[:-2])
        else:
            svg_height = float(svg_height)
        originald = circuit.xpath(f'//*[@id = "{pathid}"]')[0].attrib['d']
        # todo find parent of path with id
        # remove all paths below parent
        # add flipped path
        originals = circuit.xpath(f'//*[@id = "{pathid}"]')[0].attrib['style']
        path = parse_path(originald)
        flipped_segments = []
        for segment in path:
            flipped_segments.append(segment.translated(complex(0, -svg_height)).scaled(1, -1).translated(complex(0, svg_height)))
        flipped_path = Path(*flipped_segments)
        circuit.write(output_svg, encoding='utf-8', xml_declaration=True)
    except Exception as e:
        raise ValueError(f"Invalid SVG path data: {e}")
    return

warnings.filterwarnings('ignore')

inputname = "BalatonParkorig.svg"
pathid = "path1"

#flip_svg_path_vertically(inputname, "o" + inputname, pathid)

inputname = "PhillipIslandorig.svg"
pathid = "path2419"

flip_svg_path_vertically(inputname, "o" + inputname, pathid)

key = input("Wait")
