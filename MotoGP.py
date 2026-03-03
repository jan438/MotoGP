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
my_canvas = canvas.Canvas("PDF/MotoGP.pdf", pagesize = A4)
width, height = A4
my_canvas.setTitle("MotoGP")
drawing = scaleSVG('SVG/Indonesia.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 50, 50)
drawing = scaleSVG('SVG/Italy.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 150, 50)
drawing = scaleSVG('SVG/Catalonia.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 250, 50)
drawing = scaleSVG('SVG/Australia.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 350, 50)
drawing = scaleSVG('SVG/Thailand.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 450, 50)

drawing = scaleSVG('SVG/Brazil.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 50, 250)
drawing = scaleSVG('SVG/USA.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 150, 250)
drawing = scaleSVG('SVG/Qatar.svg', 0.09)
renderPDF.draw(drawing, my_canvas, 250, 250)
drawing = scaleSVG('SVG/Spain.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 350, 250)
drawing = scaleSVG('SVG/France.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 450, 250)

drawing = scaleSVG('SVG/Hungary.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 50, 450)
drawing = scaleSVG('SVG/Czechia.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 150, 450)
drawing = scaleSVG('SVG/Netherlands.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 250, 450)
drawing = scaleSVG('SVG/Spain.svg', 0.5)
renderPDF.draw(drawing, my_canvas, 350, 450)
drawing = scaleSVG('SVG/France.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 450, 450)

my_canvas.save()
key = input("Wait")
