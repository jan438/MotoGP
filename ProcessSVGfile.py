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
        wsvg(flipped_path, attributes=attributes, filename=output_svg)
    except Exception as e:
        raise ValueError(f"Invalid SVG path data: {e}")
    return

def svg_to_positive_coords(input_svg, output_svg):
    try:
        # Load paths and attributes from the SVG
        paths, attributes = svg2paths(input_svg)
        # Extract all coordinates from all paths
        segments = []
        all_x = []
        all_y = []
        for path in paths:
            for segment in path:
                #print("Segment start", segment.start)
                if isinstance(segment, CubicBezier):
                    segments.append(segment)
                    for point in segment:
                        all_x.append(point.real)
                        all_y.append(point.imag)

        if not all_x or not all_y:
            print("No coordinates found in the SVG.")
            return

        # Find minimum x and y to shift coordinates into positive space
        min_x = min(all_x)
        min_y = min(all_y)

        shift_x = -min_x if min_x < 0 else 0
        shift_y = -min_y if min_y < 0 else 0
        print(len(all_x), len(segments))
        return
        # Apply the shift to all paths
        shifted_paths = []
        for path in paths:
            shifted_segments = []
            for segment in path:
                shifted_segments.append(segment.translated(shift_x + 1j * shift_y))
            shifted_paths.append(type(path)(shifted_segments))

        # Save the shifted SVG
        wsvg(shifted_paths, attributes=attributes, filename=output_svg)
        print(f"Shifted SVG saved to: {output_svg}")

    except FileNotFoundError:
        print(f"Error: File '{input_svg}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

warnings.filterwarnings('ignore')

inputname = "BalatonParkorig.svg"
pathid = "path1"

flip_svg_path_vertically(inputname, "PDF/" + inputname, pathid)

inputname = "PhillipIslandorig.svg"
pathid = "path2419"

flip_svg_path_vertically(inputname, "PDF/" + inputname, pathid)

#svg_to_positive_coords(inputname, "PDF/" + inputname, pathid)

key = input("Wait")
