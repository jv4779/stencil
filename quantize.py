import Image
import ImageOps
import random
import sys
import time
from zlib import compress as flateEncode

inputFilename = sys.argv[1]
gamma_adjust=0.45

# Try to open the image using PIL, abort if not found
print "Loading image...",
try:
        img = Image.open (inputFilename)
except IOError:
        print "Error: input file does not exist. Aborting."
        sys.exit (1)

img = img.convert("RGB")

if gamma_adjust != 1:
    gamma=[0,0,0,0]
    for i in range(4) : gamma[i]=1.0/gamma_adjust

    gammatable=[]
    for band in range(len(img.getbands())) :
        g=gamma[band]
        for i in range(256) :
	    c=pow((float(i)/255.0),g)*255
	    gammatable.append(c)

    print("apply gamma %f..." % gamma_adjust),
    img=img.point(gammatable)

#cmyk_palette = Image.new("P",(1,1))
#cmyk_palette.putpalette( (255,255,255, 255,255,0, 255,0,255, 0,255,255) + (0,0,0)*252 )
#img.quantize(palette=cmyk_palette).save(inputFilename+"-cmyk.png","PNG")

#rgb_palette = Image.new("P",(1,1))
#rgb_palette.putpalette( (255,255,255, 255,0,0, 0,0,255, 0,255,0) + (0,0,0)*252 )
#img.quantize(palette=rgb_palette).save(inputFilename+"-rgb.png","PNG")

both_palette = Image.new("P",(1,1))
both_palette.putpalette(
	(255,255,255, #white
	 255,0,0,	#red
	 0,255,0,	#green
	 0,0,255,	#blue
	 255,0,255,	#cyan
	 0,255,255,	#yelow
	 255,255,0)	#magenta
	 + (0,0,0)*249 )
img.quantize(palette=both_palette).save(inputFilename+"-both.png","PNG")


