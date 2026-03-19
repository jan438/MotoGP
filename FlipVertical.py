from svgpathtools import parse_path, Path
from xml.dom import minidom
import sys

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


# Example SVG path (replace with your own)
original_path_data = "M10 10 L50 10 L50 50 L10 50 Z"
svg_height = 100  # Height of the SVG canvas

try:
    flipped_path_data = flip_svg_path_vertically(original_path_data, svg_height)
    print("Original Path:", original_path_data)
    print("Flipped Path: ", flipped_path_data)
except ValueError as e:
    print("Error:", e)

print("------------------")

svgfile = "Indonesia.svg"
doc = minidom.parse(svgfile)
original_path_data = [path.getAttribute('d') for path
            in doc.getElementsByTagName('path')]
doc.unlink()
print(original_path_data)

key = input("Wait")
