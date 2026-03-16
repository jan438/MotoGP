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
from xml.dom import minidom
from svgpathtools import parse_path, Path, Line, CubicBezier

monthnames = ["JAN", "FEB", "MRT", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "NOV", "DEC"]
circuitsdata = []
raceevents = []
row = 4
col = 0
leftmargin = 22.5
rowheight = 150
colwidth = 110
circuit_y = row * rowheight + 50
motogpfont = "LiberationSerif"
cadre_mode = True
worldmap_x = 128
worldmap_y = 300
worldmapscale = 0.33
dx = 0
dy = 0

class RaceEvent:
    def __init__(self, summary, day, location, description, starttime, endtime, month):
        self.summary = summary
        self.day = day
        self.location = location
        self.description = description
        self.starttime = starttime
        self.endtime = endtime
        self.month = month
        
def weekDay(year, month, day):
    offset = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    afterFeb = 1
    if month > 2: afterFeb = 0
    aux = year - 1700 - afterFeb
    dayOfWeek  = 5
    dayOfWeek += (aux + afterFeb) * 365                  
    dayOfWeek += aux / 4 - aux / 100 + (aux + 100) / 400     
    dayOfWeek += offset[month - 1] + (day - 1)               
    dayOfWeek %= 7
    return round(dayOfWeek)
    
def lookupraceevent(country):
    raceevent = None
    for j in range(len(raceevents)):
        if raceevents[j].summary == country:
            raceevent = raceevents[j]
    return raceevent

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
    
def drawwikicircuit(c, file, scale, x, y):
    first_command = True
    doc = minidom.parse(file)
    path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
    doc.unlink()
    p = c.beginPath()
    for path_string in path_strings:
        path = parse_path(path_string)
        for e in path:
            if isinstance(e, Line):
                x0 = e.start.real
                y0 = e.start.imag
                x1 = e.end.real
                y1 = e.end.imag
            elif isinstance(e, CubicBezier):
                cubic = e
                start_x = cubic.start.real / 10
                start_y = cubic.start.imag / 10
                control1_x = cubic.control1.real / 10
                control1_y = cubic.control1.imag / 10
                control2_x = cubic.control2.real / 10
                control2_y = cubic.control2.imag / 10
                end_x = cubic.end.real / 10
                end_y = cubic.end.imag / 10
                if first_command:
                    first_command = False
                    p.moveTo(x + start_x, y + start_y)
                    p.curveTo(x + control1_x, y + control1_y, x + control2_x, y + control2_y, x + end_x, y + end_y)
                else:
                    p.curveTo(x + control1_x, y + control1_y, x + control2_x, y + control2_y, x + end_x, y + end_y)
    p.close()
    c.drawPath(p, stroke = 1, fill = 0)
    return

if sys.platform[0] == 'l':
    path = '/home/jan/git/MotoGP'
if sys.platform[0] == 'w':
    path = "C:/Users/janbo/OneDrive/Documents/GitHub/MotoGP"
os.chdir(path)

pdfmetrics.registerFont(TTFont('LiberationSerif', 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBold', 'LiberationSerif-Bold.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifItalic', 'LiberationSerif-Italic.ttf'))
pdfmetrics.registerFont(TTFont('LiberationSerifBoldItalic', 'LiberationSerif-BoldItalic.ttf'))

file_to_open = "Data/CircuitsWiki.csv"
with open(file_to_open, 'r') as file:
    csvreader = csv.reader(file, delimiter = ';')
    count = 0
    for row in csvreader:
        circuitsdata.append(row)
        print(circuitsdata[count][5])
        count += 1
eventcal = "Calendar/MotoGP2026.ics"
in_file = open(os.path.join(path, eventcal), 'r')
count = 0
lastpos = 0
found = 0
alleventslines = []
for line in in_file:
    newlinepos = line.find("\t\n")
    lastsubstring = line[lastpos:newlinepos]
    alleventslines.append(lastsubstring)
    count += 1
in_file.close()
print("Count eventslines", len(alleventslines))
for i in range(len(alleventslines)):
    neweventpos = alleventslines[i].find("BEGIN:VEVENT")
    summaryeventpos = alleventslines[i].find("SUMMARY")
    locationeventpos = alleventslines[i].find("LOCATION")
    descriptioneventpos = alleventslines[i].find("DESCRIPTION")
    dtstarteventpos = alleventslines[i].find("DTSTART")
    dtendeventpos = alleventslines[i].find("DTEND")
    endeventpos = alleventslines[i].find("END:VEVENT")
    if neweventpos == 0:
        summary = ""
        day = 0
        location = ""
        description = ""
        starttime = 0
        endtime = 0
        month = 0
    if dtstarteventpos == 0:
        eventdtstartstr = alleventslines[i][8:]
        datevaluepos = alleventslines[i].find("VALUE=DATE:")
        if datevaluepos == 8:
            eventdtstartstr = alleventslines[i][19:]
        year = int(eventdtstartstr[:4])
        month = int(eventdtstartstr[4:6])
        day = int(eventdtstartstr[6:8])
        weekday = weekDay(year, month, day)
        starttime = eventdtstartstr
    if dtendeventpos == 0:
        eventdtendstr = alleventslines[i][6:]
        endtime = eventdtendstr[9:11] + ':' + eventdtendstr[11:13]
    if summaryeventpos == 0:
        summary = alleventslines[i][8:]
    if locationeventpos == 0:
        location = alleventslines[i][9:]
    if descriptioneventpos == 0:
        description = alleventslines[i][12:]
    if endeventpos == 0:
        raceevents.append(RaceEvent(summary, day, location, description, starttime, endtime, month))
print("Count race events", len(raceevents))
my_canvas = canvas.Canvas("PDF/MotoGPCircuits2026.pdf", pagesize = A4)
width, height = A4
my_canvas.setFont(motogpfont, 12)
my_canvas.setTitle("MotoGPCircuits2026")
my_canvas.setFillColor(HexColor("#000000"))
my_canvas.rect(0, 0, width, height, fill=1)

drawing = scaleSVG('Wiki/MotoGPlogo.svg', 0.1)
renderPDF.draw(drawing, my_canvas, 50, 775)
renderPDF.draw(scaleSVG("Wiki/WorldMap.svg", worldmapscale), my_canvas, worldmap_x, worldmap_y)

date_y = 100

for i in range(len(circuitsdata)):
    if i == 6:
        break
    rce = lookupraceevent(circuitsdata[i][0])
    day = str(rce.day)
    month = monthnames[rce.month - 1]
    if i == 11:
        col = 4
    if cadre_mode:
        my_canvas.setStrokeColor(yellow)
        my_canvas.rect(leftmargin + col * colwidth, circuit_y, colwidth, colwidth, stroke = 1, fill = 0)
    my_canvas.setFillColor(HexColor("#000000"))
    displayname = circuitsdata[i][0]
    dx = float(circuitsdata[i][2])
    dy = float(circuitsdata[i][3])
    svgfile = displayname + "v.svg"
    tree = ET.parse(svgfile)
    root = tree.getroot()
    attrib = root.attrib
    for name, value in attrib.items():
        if name == "viewBox":
            print(svgfile, '{0}="{1}"'.format(name, value))
    scale = float(circuitsdata[i][1])
    drawwikicircuit(my_canvas, svgfile, scale, leftmargin + col * colwidth + dx, circuit_y + dy)
    my_canvas.setFillColor(HexColor("#FFFFFF"))
    namewidth = pdfmetrics.stringWidth(displayname, motogpfont, 12)
    my_canvas.drawString(leftmargin + col * colwidth + (colwidth - namewidth) / 2, circuit_y - 20, displayname)
    my_canvas.drawString(leftmargin + col * colwidth, circuit_y + date_y, day)
    my_canvas.drawString(leftmargin + col * colwidth + 20, circuit_y + date_y, month)
    col = col + 1
    if col == 5:
        col = 0
        circuit_y = circuit_y - rowheight

my_canvas.save()
key = input("Wait")
