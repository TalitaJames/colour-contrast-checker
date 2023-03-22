import re
import random
import math
from PIL import Image, ImageDraw, ImageFont 

#region image gen methods

# makes a single square image with the contrast ratio and hex values
def imageContrastExample(hexTuple,contrastMin):
    
    hexBG=hexTuple[0]
    hexFG=hexTuple[1]
    
    
    # ---- Coordinates
    width=500 #size of the square
    
    # ---- Fonts
    hexFont=ImageFont.truetype("arial.ttf",65)
    crFont=ImageFont.truetype("arial.ttf",130)
    
 
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
 
# does the same as squareGrid but don't include the same colour in both boxes diagonal
def constrastGrid(hexList,squareDim,contrastMin):
    
    
    # squareSize = int(math.sqrt(len(hexList)))
    cols=len(hexList[0])
    rows=len(hexList)
    
    gridContrast=Image.new('RGB', (cols*squareDim, rows*squareDim), color = 'white')
     
    # gridContrast_Draw=ImageDraw.Draw(gridContrast)
    
    # font = ImageFont.truetype("arial.ttf", 70)
    
    for i in range(cols):
        x=i*squareDim
        for j in range(rows):
            y=j*squareDim
            
            image=imageContrastExample(hexList[j][i],contrastMin)
            
            gridContrast.paste(image, (x,y))
            # gridContrast_Draw.text([x+50,y+50],f"{i},{j}",fill="White",font=font)        
    
    return gridContrast
 
#endregion


# turns a list into a 2d list of tupple=[row][column] (background, forground)
def listSquare(hexList, match=True):
    listSquare=[]
    
    for hexBG in hexList:
        listRow=[]
        for hexFG in hexList:
            colourCombo= (hexBG,hexFG) if (match or hexBG!=hexFG) else "REMOVE"
            listRow.append(colourCombo)
        listSquare.append(listRow)
    
            
    if not match:
        for row in listSquare:
            for col in row: # column number and value
                if col == "REMOVE":
                    row.remove(col)
    
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
    
    # i don't know why these numbers, blame the WACG

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
    return '#%02x%02x%02x' % (random.randint(0,255), random.randint(0,255), random.randint(0,255))

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
            # print("\tWCAG value:",contrastMin)
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
            # print(f"\t{hexList}")
            
        elif stringIn.isnumeric() and 2<=int(stringIn)<=10:
            hexList=[randomHex() for i in range(int(stringIn))]
            # print(f"\t{hexList}")
            
        else: 
            hexList = re.findall("#.{6}", stringIn)  
    
    return contrastMin,hexList

if __name__ == '__main__':
    
    
            
    contrastMin,hexList=getInfo()
    print(f"\n\tContrast: {contrastMin}\n\thexList: {hexList}")
    
    hexSquare_all=listSquare(hexList,True)
    hexSquare_min=listSquare(hexList,False)
            
    version="v1.4"
    fileName=f"example" #export_{version}"
    
    
    square=imageContrastExample(hexSquare_min[0][0],contrastMin)
    square.save(f"graphics\{fileName}_square.png")

    gridContrast_blanks=constrastGrid(hexSquare_all,500,contrastMin)
    gridContrast_blanks.save(f"graphics\{fileName}_all.png")
    
    gridContrast=constrastGrid(hexSquare_min,500,contrastMin)
    gridContrast.save(f"graphics\{fileName}_min.png")
    
    print("\nPhoto Saved")
        
        
        
        
