import re
import random
import math
from PIL import Image, ImageDraw, ImageFont 

def imageContrastExample(hexFG, hexBG,contrastMin):
    
    #region font and coordinates
    
    # Coordinates
    width=500 #size of the square
    xText,yText=50,370
    
    # Fonts
    normalFont=ImageFont.truetype("arial.ttf",18)
    largeFont=ImageFont.truetype("arial.ttf",24)
    hexFont=ImageFont.truetype("arial.ttf",30)
    crFont=ImageFont.truetype("arial.ttf",130)
    
    
    #endregion
    
    
    contrastSquare=Image.new('RGB', (width, width), color = hexBG)
    contrastDraw = ImageDraw.Draw(contrastSquare)  
    
    
    #region icons (tick/cross)
    cross=Image.open('icon_cross.png')
    tick=Image.open('icon_tick.png')
    
    scale=0.5
    cross=cross.resize((int(scale*cross.width),int(scale*cross.height)))
    tick=tick.resize((int(scale*tick.width),int(scale*tick.height)))
    
    colourIcon=Image.new('RGB', (cross.width,cross.height), hexFG)   
     
    icon = tick if contrastRatio(hexFG, hexBG) >= contrastMin else cross
    contrastSquare.paste(colourIcon, (width//2-icon.width//2,40),mask=icon)
    #endregion
    
    #region hex and ratio text
    hexString=f"F: {hexFG}\nB: {hexBG}"
    contrastDraw.multiline_text((width-175, width-75), hexString, fill=hexFG, font=hexFont)
    contrastDraw.text((width//2, 30+width//2), str(contrastRatio(hexFG, hexBG)), fill=hexFG, font=crFont,anchor='mm')
    #endregion
    
    #region WCAG text
    #text string
    colourInfo=f"foreground: {hexFG}, background: {hexBG}"
    pangram="Sphinx of black quartz, judge my vow"
    fails="F"
    passes="P"
    
    # normal text
    # WCAG 2.0 level AA at least 4.5:1 and Lvl AAA 7:1 for normal text
    
    contrastNormalString=f'Normal text:{passes if contrastRatio(hexFG, hexBG) >= 4.5 else fails} Level AA, {passes if contrastRatio(hexFG, hexBG) >= 7 else fails} Level AAA'
    contrastDraw.text((xText, yText), contrastNormalString, fill=hexFG, font=normalFont)
   
   
   
    # # large text
    # Large text is defined as 14 point (typically 18.66px) and bold or larger, or 18 point (typically 24px) or larger.
    # WCAG 2.0 level AA: 3:1 and Level AAA: 4.5:1
    contrastLargeString=f'Large text:{passes if contrastRatio(hexFG, hexBG) >= 3 else fails} Level AA, {passes if contrastRatio(hexFG, hexBG) >= 4.5 else fails} Level AAA'
    contrastDraw.text((xText, yText+20), contrastLargeString, fill=hexFG, font=largeFont)
    
    # graphics and user interface components
    #  WCAG 2.1 requires a contrast ratio of at least 3:1 for graphics ect
    
    
    #endregion
    
    
    return contrastSquare


def squareGrid(hexList,squareDim):
    contrastMin=4.5
    squareSize = int(math.sqrt(len(hexList)))
    
    gridContrast=Image.new('RGB', (squareSize*squareDim, squareSize*squareDim), color = 'white')
    gridDraw = ImageDraw.Draw(gridContrast)  
    
    
    
    for i in range(squareSize):
        x=i*squareDim
        for j in range(squareSize):
            y=j*squareDim
            image=imageContrastExample(hexList[i*squareSize+j][0],hexList[i*squareSize+j][1],contrastMin)
            gridContrast.paste(image, (x,y))
            pass
        
    
    
    gridContrast.save("gridContrast.png")
 
# turns a list into a 2d list of all possible combinations   
def listSquare(hexList):
    listSquare=[]
    for hexBG in range(len(hexList)):
        for hexFG in range(len(hexList)):
            listSquare.append([hexList[hexBG],hexList[hexFG]])
            
    
    return listSquare


#region colour methods

def contrastRatio(hexFG, hexBG):
    lumFG = relativeLuminance(hexFG)
    lumBG = relativeLuminance(hexBG)
    maxLum = max(lumFG, lumBG)
    minLum = min(lumFG, lumBG)
    # ratio ranges from 1 to 21 (commonly written 1:1 to 21:1).
    
    # maxLum is the relative luminance of the lighter of the colors, and
    # minLum is the relative luminance of the darker of the colors.
    contrast=(maxLum + 0.05) / (minLum + 0.05)
    contrast=round(contrast,2)
    return contrast

def relativeLuminance(hex):
    r,g,b=hexToRGB(hex)
    
    rRatio = r/255
    gRatio = g/255
    bRatio = b/255
    

    if rRatio <= 0.03928:
        R = rRatio/12.92 
    else: 
        R = ((rRatio+0.055)/1.055) ** 2.4
    
    if gRatio <= 0.03928:
        G = gRatio/12.92
    else:
        G = ((gRatio+0.055)/1.055) ** 2.4
    
    if bRatio <= 0.03928:
        B = bRatio/12.92
    else:
        B = ((bRatio+0.055)/1.055) ** 2.4
    
    luminance = 0.2126 * R + 0.7152 * G + 0.0722 * B
        
        
    return round(luminance,2)

# converts a hex string (with or without a leading #) to rgb
def hexToRGB(hex):
    # convert hex string to rgb
    hex = re.sub("#", "", hex, 1)
    
    r = int(hex[0:2], 16)
    g = int(hex[2:4], 16)
    b = int(hex[4:6], 16)
    
    return r,g,b

#returns a rransom hex colour in string "#______" format
def randomHex():
    return '#%02x%02x%02x' % (random.randint(0,255),random.randint(0,255),random.randint(0,255))

#endregion


if __name__ == '__main__':
    hexList=[] #["#23599A", "#E54726", "#2BB250", "#363636", "#FFFFFF"]
    
    for i in range(6):
        hexList.append(randomHex())


    hexSquare = listSquare(hexList)
    print(f"\n{hexSquare}")
    squareGrid(hexSquare, 500)
    print("done")
    
    
    
    
