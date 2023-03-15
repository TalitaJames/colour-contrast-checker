# Colour Contrast checker
I needed something that would allow me to check the colour contrast ratios of lots of colours at once, so i made it

## The output
A grid of the contrast, made by `squareGrid()` has input of `4.5` and `#38D7E7 #F9F7F1 #EE316B #842D72`

<img src="graphics\example_gridContrast_blanks.png"  width="60%">

Note that on the diagonal, the colours are identical and as such nothing is seen, the contrast ratio is exactly 1 (no contrast)

Single contrast example, made by `imageContrastExample()` </br>
<img src="graphics\example_squareContrast.png"  width="30%">

## Input
Each of these values accept one of the dotpoints as an input

**Contrast ratio:**
- will expect either a float (between 1 and 21 inclusive)
- empty value (will then defult to 4.5)
- a WCAG contrast code, AA or AAA and large or normal (eg AAA-L or AA-N)


**Hex List:** 
- empty (will randomly generate 3 hex values) 
- string that gets regexes to take the first 6 values after every `#`
- int will rng that many hex values
