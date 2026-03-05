import os
import sys
import csv
import math
import unicodedata
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.graphics import renderPDF
from datetime import datetime, date, timedelta
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import blue, green, black, red, pink, gray, brown, purple, orange, yellow
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics  
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch, mm
from svglib.svglib import svg2rlg, load_svg_file, SvgRenderer
import xml.etree.ElementTree as ET

circuitsdata = []
row = 4
col = 0
leftmargin = 22.5
rowheight = 150
colwidth = 110
circuit_y = row * rowheight + 50
motogpfont = "LiberationSerif"

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

pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))

file_to_open = "Data/Circuits.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        circuitsdata.append(row)
        count += 1
my_canvas = canvas.Canvas("PDF/MotoGP.pdf", pagesize = A4)
width, height = A4
my_canvas.setFont(motogpfont, 12)
my_canvas.setTitle("MotoGP")
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.rect(0, 0, width, height, fill=1)

drawing = scaleSVG('SVG/MotoGPlogo.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 50, 750)

for i in range(len(circuitsdata)):
    if i == 11:
        col = 4
    my_canvas.setStrokeColor(yellow)
    my_canvas.rect(leftmargin + col * colwidth, circuit_y, colwidth, colwidth, stroke = 1, fill = 0)
    my_canvas.setFillColor(HexColor("#000000"))
    svgfile = "SVG/" + circuitsdata[i][0] + ".svg"
    tree = ET.parse(svgfile)
    root = tree.getroot()
    attrib = root.attrib
    for name, value in attrib.items():
        if name == "viewBox":
            print(svgfile, '{0}="{1}"'.format(name, value))
    scale = float(circuitsdata[i][1])
    drawing = scaleSVG(svgfile, scale)
    renderPDF.draw(drawing, my_canvas, leftmargin + col * colwidth, circuit_y)
    my_canvas.drawString(leftmargin + col * colwidth, circuit_y - 20, circuitsdata[i][0])
    col = col + 1
    if col == 5:
        col = 0
        circuit_y = circuit_y - rowheight

my_canvas.save()
key = input("Wait")
