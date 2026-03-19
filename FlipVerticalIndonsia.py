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

original_path_data = "m -51.44751,-76.663828 264.39435,-73.516362 c 0,0 28.15921,-4.9137 29.86011,16.63095 1.7009,21.54464 0.56697,88.446425 0.56697,88.446425 0,0 1.17043,13.328835 -14.17411,10.961309 -17.62555,-2.719465 -20.41071,-7.181548 -26.08035,6.236607 -5.66965,13.418155 -8.69346,18.8988095 6.42559,33.261905 15.11905,14.363095 45.92411,41.199405 45.92411,41.199405 0,0 8.50446,6.236607 8.50446,34.584821 0,28.348218 0.18899,50.081848 0.18899,50.081848 0,0 0.75595,11.15029 -15.68601,28.5372 -16.44197,17.3869 -36.66369,41.57738 -36.66369,41.57738 0,0 -6.61459,10.39435 -29.48214,10.39435 -22.86756,0 -35.90774,3.96875 -60.85417,32.50595 -24.94643,28.5372 -25.89137,27.21428 -51.21578,41.01042 -25.3244,13.79613 -82.96577,44.97916 -82.96577,44.97916 0,0 -32.88393,22.11161 -30.23809,-24.37946 2.64583,-46.49107 3.40178,-67.09078 3.40178,-67.09078 0,0 -0.94494,-21.92262 31.37202,-34.20684 32.31697,-12.28423 56.50745,-15.11905 51.40477,-59.53125 -5.10268,-44.4122 -7.74852,-74.650299 -7.74852,-74.650299 0,0 1.13393,-27.78125 -38.36458,-29.482143 0,0 -31.18303,-1.511905 -54.99553,-33.450893 -23.8125,-31.938988 -49.89286,-72.382441 -49.89286,-72.382441 0,0 -14.74107,-17.764881 -5.29167,-54.995534 9.44941,-37.23066 26.647323,-30.61607 26.647323,-30.61607 0,0 13.418157,0.18899 8.693457,42.33333 -4.72471,42.144346 4.15773,37.419643 26.26934,31.561012 z"

svg_height = 536.70074

try:
    flipped_path_data = flip_svg_path_vertically(original_path_data, svg_height)
    print("Original Path:", original_path_data)
    print("------------------")
    print("Flipped Path: ", flipped_path_data)
except ValueError as e:
    print("Error:", e)

key = input("Wait")
