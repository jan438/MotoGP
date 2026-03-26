import sys
from svgpathtools import svg2paths, wsvg
from svgpathtools import parse_path, Path, Line, CubicBezier
from reportlab.lib.units import inch, mm
import lxml.etree as ET
import warnings

def flip_svg_path_vertically(input_svg, output_svg, pathid):
    """
    Flip an SVG path vertically around the horizontal axis at y = height / 2.

    :param path_data: The 'd' attribute string from an SVG <path>.
    :param height: The total height of the SVG canvas.
    :return: Flipped path data string.
    """
    try:
        circuit = ET.parse(input_svg)
        root = circuit.getroot()
        nsmap = {'svg': 'http://www.w3.org/2000/svg'}
        xpaths = root.findall('.//svg:path', namespaces=nsmap)
        svg_height = root.get("height")
        measurement = svg_height[len(svg_height) - 2:]
        if measurement == "mm" or measurement == "cm" or measurement == "in" or measurement == "px" or measurement == "pt":
            svg_height = float(svg_height[:-2])
        else:
            svg_height = float(svg_height)
        original_path_data = circuit.xpath(f'//*[@id = "{pathid}"]')[0].attrib['d']
        path = parse_path(original_path_data)
        # Apply vertical flip: scale y by -1 and translate
        flipped_segments = []
        for segment in path:
            flipped_segments.append(segment.translated(complex(0, -svg_height)).scaled(1, -1).translated(complex(0, svg_height)))
        flipped_path = Path(*flipped_segments)
        paths, attributes = svg2paths(input_svg)
        original_style_data = circuit.xpath(f'//*[@id = "{pathid}"]')[0].attrib['style']
        #print("Style", pathid, dir(original_style_data))
        wsvg(flipped_path, attributes=attributes, filename = "w" + output_svg)
        circuit.write("x" + output_svg, encoding='utf-8', xml_declaration=True)
    except Exception as e:
        raise ValueError(f"Invalid SVG path data: {e}")
    return

warnings.filterwarnings('ignore')

inputname = "BalatonParkorig.svg"
pathid = "path1"

flip_svg_path_vertically(inputname, "o" + inputname, pathid)

inputname = "PhillipIslandorig.svg"
pathid = "path2419"

flip_svg_path_vertically(inputname, "o" + inputname, pathid)

key = input("Wait")
