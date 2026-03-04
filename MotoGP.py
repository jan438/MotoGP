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
rowheight = 150
colwidth = 90
circuit_y = row * rowheight

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
    if i == 15:
        break
    if i == 11:
        col = 4  
    scale = float(circuitsdata[i][1])
    drawing = scaleSVG("SVG/" + circuitsdata[i][0] + ".svg", scale)
    renderPDF.draw(drawing, my_canvas, leftmargin + col * colwidth, circuit_y)
    my_canvas.drawString(leftmargin + col * colwidth, circuit_y - 20, circuitsdata[i][0])
    col = col + 1
    if col == 5:
        col = 0
        circuit_y = circuit_y - rowheight

my_canvas.save()
key = input("Wait")
