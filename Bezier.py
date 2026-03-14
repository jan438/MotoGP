# Source - https://stackoverflow.com/a/45807723
# Posted by Heath Raftery
# Retrieved 2026-03-14, License - CC BY-SA 3.0

from svgpathtools import Path, Line, CubicBezier

complex = (300+100j)
print(complex.real)

bezier_curve = CubicBezier(start=(300+100j), control1=(100+100j), control2=(200+200j), end=(200+300j))
bezier_path = Path(bezier_curve)

NUM_SAMPLES = 10

myPath = []
for i in range(NUM_SAMPLES):
    myPath.append(bezier_path.point(i/(NUM_SAMPLES-1)))

print(myPath)

key = input("Wait")

