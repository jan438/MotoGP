import sys
from svgpathtools import svg2paths, wsvg
from xml.dom import minidom

def svg_to_positive_coords(input_svg, output_svg):
    doc = minidom.parse(input_svg)
    path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
    doc.unlink()
    print(str(path_strings))
    return
    try:
        # Load paths and attributes from the SVG
        paths, attributes = svg2paths(input_svg)

        # Extract all coordinates from all paths
        all_x = []
        all_y = []
        for path in paths:
            for segment in path:
                for point in [segment.start, segment.end]:
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

inputname = "path.svg"
inputfile = open(inputname)

print(inputfile)

svg_to_positive_coords(inputname, "PDF/outfile")

key = input("Wait")
