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

original_path_data = "m 524.1311,631.4325 c 6.176,7.15133 16.9801,7.94181 24.1314,1.76581 l 336.66,-410.231 c 5.18932,-8.39127 3.5106,-19.3098 -3.95973,-25.7551 -7.47033,-6.44494 -18.517,-6.505 -26.0571,-0.14181 l -174.804,191.284 c -5.82197,4.21532 -13.3327,5.3298 -20.128,2.98673 -6.79497,-2.3434 -12.0227,-7.85038 -14.009,-14.7581 l -16.4796,-143.61 c -4.60339,-14.6684 -16.1028,-26.1491 -30.7792,-30.7282 -14.676,-4.57869 -30.6644,-1.67405 -42.7915,7.7743 -18.0268,17.5163 -46.7159,17.5163 -64.7424,0 L 376.98997,71.117128 c -23.1621,-16.596 -52.6013,-21.7913 -80.0451,-14.1255 l -114.182,28.251 c -6.83401,1.48352 -12.1818,6.80498 -13.699,13.6316 -1.51722,6.827002 1.07343,13.912602 6.63614,18.150902 l 266.032,231.895 c 8.56512,14.3274 9.44769,31.9751 2.35441,47.0856 l -23.5428,34.1367 c -3.62271,4.96209 -9.47705,7.79633 -15.616,7.56008 -6.13929,-0.23591 -11.7587,-3.5116 -14.9894,-8.73729 l -248.375,-269.563 c -10.0086,-6.55539 -22.9512,-6.55539 -32.9598,0 -9.11501,3.40816 -16.9354,9.58216 -22.3656,17.6571 -6.38388,10.9058 -6.38388,24.408 0,35.3139 l 242.489,326.066 c 2.84659,3.1816 6.91376,4.99979 11.1828,4.99979 4.26938,0 8.33621,-1.8182 11.1828,-4.99979 l 11.7714,-12.9486 c 5.02148,-7.85172 15.0281,-10.8538 23.5425,-7.06291 l 55.914,8.24012 81.8105,104.765 z"

svg_height = 719.69885

try:
    flipped_path_data = flip_svg_path_vertically(original_path_data, svg_height)
    print("Original Path:", original_path_data)
    print("------------------")
    print("Flipped Path: ", flipped_path_data)
except ValueError as e:
    print("Error:", e)

key = input("Wait")
