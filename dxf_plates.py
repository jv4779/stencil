import Image
import ImageOps
import random
import sys
import time
from zlib import compress as flateEncode
import sdxf

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

def dxf_header():
	return sdxf.Drawing()

def dxf_circle(f,x,y,d,c):
	f.append(sdxf.Circle(center=(x,y),radius=d/2.0))

def dxf_text(f,x,y,h,txt):
	f.append(sdxf.Text(txt,point=(x,y-h/2.0),height=h))

def dxf_footer(f,filename):
	f.saveas(filename)


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
out_h = 17.0
out_spacing = out_w / pix_w
out_diameter = out_spacing * 0.90

files = {}

for c in colors:
	f=dxf_header()
	dxf_circle(f,0,0,0.5,"black")
	dxf_circle(f,0,out_h,0.5,"black")
	dxf_circle(f,out_w,0,0.5,"black")
	dxf_circle(f,out_w,out_h,0.5,"black")
	dxf_text(f,2,out_h,0.5,c)
	files[c]=f

for y in xrange(0,pix_h):
    y_offset = (pix_h - y) * out_spacing + 1

    row = pix[y * pix_w:(y + 1) * pix_w]

    for index, pixel in enumerate(row):
        x_offset = index * out_spacing
	(r,g,b)=pixel
	c=(r>127)+(g>127)*2+(b>127)*4
        dxf_circle(files[colors[c]],x_offset,y_offset,out_diameter,colors[c])

for c in colors:
	dxf_footer(files[c],inputFilename+"-plate-"+c+".dxf")

