import re
import random
import math
from PIL import Image, ImageDraw, ImageFont 

#region image gen methods

# makes a single square image with the contrast ratio and hex values
def imageContrastExample(hexFG, hexBG,contrastMin):
    
    #region font and coordinates
    # ---- Coordinates
    width=500 #size of the square
    
    # ---- Fonts
    hexFont=ImageFont.truetype("arial.ttf",65)
    crFont=ImageFont.truetype("arial.ttf",130)
    
    
    #endregion
    
    
    contrastSquare=Image.new('RGB', (width, width), color = hexBG)
    contrastDraw = ImageDraw.Draw(contrastSquare)  
    
    
    #region icons (tick/cross)
    cross=Image.open('graphics\icon_cross.png')
    tick=Image.open('graphics\icon_tick.png')
    
    scale=0.5
    cross=cross.resize((int(scale*cross.width),int(scale*cross.height)))
    tick=tick.resize((int(scale*tick.width),int(scale*tick.height)))
    
    colourIcon=Image.new('RGB', (cross.width,cross.height), hexFG)   
     
    icon = tick if contrastRatio(hexFG, hexBG) >= contrastMin else cross
    contrastSquare.paste(colourIcon, (width//2-icon.width//2,40),mask=icon)
    #endregion
    
    #region hex and ratio text
    hexString=f"F {hexFG.upper()}\nB {hexBG.upper()}"
    contrastDraw.multiline_text((width//2, width-75), hexString, fill=hexFG, font=hexFont,anchor='mm')
    contrastDraw.text((width//2, 30+width//2), str(contrastRatio(hexFG, hexBG)), fill=hexFG, font=crFont,anchor='mm')
    #endregion
    
  
    
    return contrastSquare

# uses imageContrastExample to make a grid of all possible combinations
def squareGrid(hexList,squareDim,contrastMin):
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
        
    
    return gridContrast
 
def squareGrid_noBlank(hexList,squareDim,contrastMin):
    print("not implemented")
    # do the same as squareGrid but don't include the same colour in both boxes diagonal
    pass
 
#endregion





# turns a list into a 2d list of all possible combinations   
def listSquare(hexList):
    listSquare=[]
    for hexBG in range(len(hexList)):
        for hexFG in range(len(hexList)):
            listSquare.append([hexList[hexBG],hexList[hexFG]])
            
    
    return listSquare


#region colour maths methods

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

# uses input() to get contrast & hex info from user
def getInfo():
    
    WCAGdict = {'AA-N':4.5, 'AA-L':3, 'AAA-N':7, 'AAA-L':4.5}
    
    # ------- Contrast -------
    
    contrastMin="start"
    print("\nEnter a number, leave blank, or type 'AA-N or 'AA-L' per your WCAG requirements")
    # while contrastMin isn't a number and isn't blank
    while not contrastMin.isnumeric() and contrastMin != '':
        contrastMin=input("Contrast Ratio: ")
        if contrastMin =='':
            contrastMin=4.5
            print("\tWCAG value:",contrastMin)
            break
        elif re.sub("(\.|-)", "", contrastMin).isnumeric(): # regex out the decimal point & neg sign to check if all numbers
            contrastMin=float(contrastMin)
            if contrastMin>21 or contrastMin<1:
                print("\tMust be between 1 and 21 inclusive")
                contrastMin="try again"
            else:
                contrastMin=float(contrastMin)
                break
        elif contrastMin.upper() in WCAGdict:
            contrastMin=WCAGdict[contrastMin.upper()]
            print("\tWCAG value:",contrastMin)
            break
    
    # ------- Hex List -------
    
    hexList=[]
    print("\n\nEnter list of hex codes (starting with '#'), int for x random, leave blank for 3")
    while len(hexList)==0:
        stringIn=input("Hex list: ")
        if not stringIn:
            hexList=[randomHex() for i in range(3)]
            print(f"\t{hexList}")
            
        elif stringIn.isnumeric():
            hexList=[randomHex() for i in range(int(stringIn))]
            print(f"\t{hexList}")
            
        else: 
            hexList = re.findall("#.{6}", stringIn)  
    
    return contrastMin,hexList

if __name__ == '__main__':

      
    contrastMin,hexList=getInfo()
    
    # print(f"\n\tcontrast: {contrastMin}\n\thexList: {hexList}")

    square=imageContrastExample("#F9F7F1","#EE316B",contrastMin)
    square.save("graphics\example_squareContrast.png")

    hexSquare = listSquare(hexList)
    # print(f"\nfull hex square\t{hexSquare}")    
    gridContrast=squareGrid(hexSquare, 500,contrastMin)
    gridContrast.save("graphics\example_gridContrast_blanks.png")
    
    print("\nPhoto Saved")
    
    
    
    
