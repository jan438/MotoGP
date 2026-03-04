import os
import sys
import csv
import math
import unicodedata
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.graphics import renderPDF
from datetime import datetime, date, timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm
from svglib.svglib import svg2rlg, load_svg_file, SvgRenderer

circuitsdata = []
row = 4
col = 0
leftmargin = 25
rowheight = 160
colwidth = 180

def scaleSVG(svgfile, scaling_factor):
    svg_root = load_svg_file(svgfile)
    svgRenderer = SvgRenderer(svgfile)
    drawing = svgRenderer.render(svg_root)
    scaling_x = scaling_factor
    scaling_y = scaling_factor
    drawing.width = drawing.minWidth() * scaling_x
    drawing.height = drawing.height * scaling_y
    drawing.scale(scaling_x, scaling_y)
    return drawing

if sys.platform[0] == 'l':
    path = '/home/jan/git/MotoGP'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/MotoGP"
os.chdir(path)
file_to_open = "Data/Circuits.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        circuitsdata.append(row)
        count += 1
my_canvas = canvas.Canvas("PDF/MotoGP.pdf", pagesize = A4)
width, height = A4
my_canvas.setTitle("MotoGP")

drawing = scaleSVG('SVG/MotoGPlogo.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 50, 750)

for i in range(len(circuitsdata)):
    if i == 1:
        break
    drawing = scaleSVG("SVG/" + circuitsdata[i][0] + ".svg", 0.5)
    renderPDF.draw(drawing, my_canvas, leftmargin + 50, 700)
    my_canvas.drawString(leftmargin + 150, 700, circuitsdata[i][0])
    col = col + 1
    if col == 5:
        col = 0
        row = row + 1

drawing = scaleSVG('SVG/Indonesia.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 50, 50)
my_canvas.drawString(50, 45, "Indonesia")
drawing = scaleSVG('SVG/Italy.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 150, 50)
my_canvas.drawString(150, 45, "Italy")
drawing = scaleSVG('SVG/Catalonia.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 250, 50)
my_canvas.drawString(250, 45, "Catalonia")
drawing = scaleSVG('SVG/Australia.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 350, 50)
my_canvas.drawString(350, 45, "Australia")
drawing = scaleSVG('SVG/Thailand.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 450, 50)
my_canvas.drawString(450, 45, "Thailand")

drawing = scaleSVG('SVG/Brazil.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 50, 250)
my_canvas.drawString(50, 245, "Brazil")
drawing = scaleSVG('SVG/USA.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 150, 250)
my_canvas.drawString(150, 245, "USA")
drawing = scaleSVG('SVG/Qatar.svg', 0.09)
renderPDF.draw(drawing, my_canvas, 250, 250)
my_canvas.drawString(250, 245, "Qatar")
drawing = scaleSVG('SVG/Spain.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 350, 250)
my_canvas.drawString(350, 245, "Spain")
drawing = scaleSVG('SVG/France.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 450, 250)
my_canvas.drawString(450, 245, "France")

drawing = scaleSVG('SVG/Hungary.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 50, 450)
my_canvas.drawString(50, 445, "Hungary")
drawing = scaleSVG('SVG/Czechia.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 150, 450)
my_canvas.drawString(150, 445, "Czechia")
drawing = scaleSVG('SVG/Netherlands.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 250, 450)
my_canvas.drawString(250, 445, "Netherlands")
drawing = scaleSVG('SVG/Germany.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 350, 450)
my_canvas.drawString(350, 445, "Germany")
drawing = scaleSVG('SVG/Great Britain.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 450, 450)
my_canvas.drawString(450, 445, "Great Britain")

drawing = scaleSVG('SVG/Aragon.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 50, 650)
my_canvas.drawString(50, 645, "Aragon")
drawing = scaleSVG('SVG/San Marino;.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 150, 650)
my_canvas.drawString(150, 645, "San Marino")
drawing = scaleSVG('SVG/Austria.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 250, 650)
my_canvas.drawString(250, 645, "Austria")
drawing = scaleSVG('SVG/Japan.svg', 0.4)
renderPDF.draw(drawing, my_canvas, 350, 650)
my_canvas.drawString(350, 645, "Japan")
drawing = scaleSVG('SVG/Malaysia.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 450, 650)
my_canvas.drawString(450, 645, "Malaysia")

drawing = scaleSVG('SVG/Portugal.svg', 0.4)
renderPDF.draw(drawing, my_canvas, 50, 350)
my_canvas.drawString(50, 345, "Portugal")
drawing = scaleSVG('SVG/Valencia.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 450, 350)
my_canvas.drawString(450, 345, "Valencia")

my_canvas.save()
key = input("Wait")
