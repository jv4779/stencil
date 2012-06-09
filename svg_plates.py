import Image
import ImageOps
import random
import sys
import time

# 90 for inkscake, 96 for coreldraw
pix_per_in = 96

colors=("black","red","green","yellow","blue","magenta","cyan","white")
colors_rbg={
	"black":"000000",
	"red":"FF0000",
	"green":"00FF00",
	"yellow":"FFFF00",
	"blue":"0000FF",
	"magenta":"FF00FF",
	"cyan":"00FFFF",
	"white":"FFFFFF" }


def svg_header(f):
	f.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   id="svg2"
   height="1575"
   width="1035"
   version="1.1"
   inkscape:version="0.48.1 "
   sodipodi:docname="plate_template.svg">
  <defs
     id="defs2999" />
  <sodipodi:namedview
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1"
     objecttolerance="10"
     gridtolerance="10"
     guidetolerance="10"
     inkscape:pageopacity="0"
     inkscape:pageshadow="2"
     inkscape:window-width="1920"
     inkscape:window-height="1178"
     id="namedview2997"
     showgrid="false"
     inkscape:zoom="0.62793651"
     inkscape:cx="517.5"
     inkscape:cy="660.09858"
     inkscape:window-x="1912"
     inkscape:window-y="-8"
     inkscape:window-maximized="1"
     inkscape:current-layer="svg2" />
  <metadata
     id="metadata7">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title />
      </cc:Work>
    </rdf:RDF>
  </metadata>
""")

path_id = 1

def svg_circle(f,x,y,d,c):
	global path_id
	path_id += 1
	f.write("""  <circle
     cx="%(x)f"
     cy="%(y)f"
     r="%(r)f"
     id="path%(id)d"
     style="fill:#%(color)s;stroke:#000000;stroke-width:0.0903498;stroke-linecap:butt;stroke-linejoin:bevel;stroke-miterlimit:4;stroke-dasharray:none;stroke-dashoffset:0" />
""" % { "id":path_id,"scale": d/0.25, "x": x*pix_per_in, "y": y*pix_per_in, "color": colors_rbg[c], "r":d*pix_per_in/2.0 } )

def svg_text(f,x,y,txt):
	f.write("""  <text
     id="text3116"
     style="font-size:48px;font-style:normal;font-weight:normal;line-height:125%%;letter-spacing:0px;word-spacing:0px;fill:#000000;font-family:Sans"
     line-height="125%%"
     font-weight="normal"
     font-size="40px"
     font-style="normal"
     y="0"
     x="0"
     xml:space="preserve"
     sodipodi:linespacing="125%%"
     transform="translate(%(x)f,%(y)f)"><tspan
       id="tspan3118"
       y="0"
       x="0">%(text)s</tspan></text>
""" % { "text":txt,"x":x*pix_per_in,"y":y*pix_per_in })

def svg_footer(f):
	f.write("""</svg>""")



inputFilename = sys.argv[1]
baseFolder = inputFilename[0:inputFilename.rfind ("/")]

# Try to open the image using PIL, abort if not found
print "Loading image...",
try:
        img = Image.open(inputFilename).convert("RGB")
except IOError:
        print "Error: input file does not exist. Aborting."
        sys.exit (1)

(pix_w,pix_h) = img.size
print('(original size w=%u,h=%u)' % (pix_w,pix_h))
pix = list(img.getdata())

out_w = 11.0
out_spacing = out_w / pix_w
out_diameter = out_spacing * 0.90

files = {}

for c in colors:
	f = open (inputFilename+"-plate-"+c+".svg", "w")
	svg_header(f)
	svg_circle(f,0,-1,0.5,"black")
	svg_circle(f,0,16,0.5,"black")
	svg_circle(f,11,-1,0.5,"black")
	svg_circle(f,11,16,0.5,"black")
	svg_text(f,2,16,c)
	files[c]=f

for y in xrange(0,pix_h):
    y_offset = y * out_spacing

    row = pix[y * pix_w:(y + 1) * pix_w]

    for index, pixel in enumerate(row):
        x_offset = index * out_spacing
	(r,g,b)=pixel
	c=(r>127)+(g>127)*2+(b>127)*4
        svg_circle(files[colors[c]],x_offset,y_offset,out_diameter,colors[c])
	#print("i=%d r=%d g=%d b=%d c=%d %s" % (index,r,g,b,c,colors[c]))

for c in colors:
	svg_footer(files[c])
	files[c].close()

