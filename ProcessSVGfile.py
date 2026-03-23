import sys
from svgpathtools import svg2paths, wsvg
from svgpathtools import parse_path, Path, Line, CubicBezier

def flip_svg_path_vertically(path_data, height):
    """
    Flip an SVG path vertically around the horizontal axis at y = height / 2.

    :param path_data: The 'd' attribute string from an SVG <path>.
    :param height: The total height of the SVG canvas.
    :return: Flipped path data string.
    """
    try:
        path = parse_path(path_data)
    except Exception as e:
        raise ValueError(f"Invalid SVG path data: {e}")

    # Apply vertical flip: scale y by -1 and translate
    flipped_segments = []
    for segment in path:
        flipped_segments.append(segment.translated(complex(0, -height)).scaled(1, -1).translated(complex(0, height)))

    flipped_path = Path(*flipped_segments)
    return flipped_path.d()

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
                print("Segment start", segment.start)
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

original_path_data = "M150 5 L75 200 L225 200 Z"

inputname = "BalatonPark.svg"

svg_height = 210

try:
    flipped_path_data = flip_svg_path_vertically(original_path_data, svg_height)
    print("Original Path:", original_path_data)
    print("------------------")
    print("Flipped Path: ", flipped_path_data)
except ValueError as e:
    print("Error:", e)
    
svg_to_positive_coords(inputname, "PDF/outfile")

key = input("Wait")
