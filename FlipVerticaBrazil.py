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

print("------------------")

original_path_data = "m -120.47965,934.90965 c -79.18271,43.79499 -151.54925,6.04995 -174.96795,-53.27743 l -18.16276,-46.01233 c -16.94756,-42.93383 -7.64826,-98.37564 16.95191,-137.43157 l 176.1788,-279.70653 c 10.98964,-17.44747 28.434083,-31.4636 47.223176,-39.95808 L 128.956,287.10418 c 39.83678,-18.01006 98.95082,7.34537 111.27249,61.79802 10.45708,46.21253 -18.85918,95.72494 -71.3148,102.87798 L 35.720099,469.94295 c -28.8473503,3.93373 -59.295054,20.55844 -74.467324,45.4069 L -157.41061,709.6914 c -15.19572,24.88688 9.19685,57.91015 30.8767,65.38595 l 17.55734,6.05425 c 31.289204,10.78937 72.439236,-11.63293 91.419233,-38.74722 L -0.6054254,718.16736 C 17.621151,692.12939 43.076073,669.48872 72.045623,656.41397 L 345.6979,532.90719 c 20.94194,-9.45167 41.13835,-23.86773 53.8831,-42.98501 l 47.22295,-70.83497 C 458.17646,402.02832 442.7387,369.86668 425.00863,359.5718 L 406.24044,348.67414 C 387.17599,337.60446 380.42356,304.0541 392.92109,285.89362 l 38.74722,-56.30456 c 19.03411,-27.65894 60.58266,-48.06561 93.84069,-52.67188 l 476.47,-65.9915 c 28.321,-3.92248 65.3332,28.3421 64.1751,56.90999 l -1.8162,44.80148 c -1.6734,41.27773 -31.0516,84.13867 -67.20226,104.13317 z"

svg_height = 1052.3622

try:
    flipped_path_data = flip_svg_path_vertically(original_path_data, svg_height)
    print("Original Path:", original_path_data)
    print("------------------")
    print("Flipped Path: ", flipped_path_data)
except ValueError as e:
    print("Error:", e)

key = input("Wait")
