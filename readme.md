# Colour Contrast checker
This quick little script will give you colour contrast info about a set of colours. The colour info is based on guidelines set by the [WACG](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html)

## The output
A grid of the contrast, made by `squareGrid()` has input of `3` and `#38D7E7 #F9F7F1 #EE316B #842D72`

<img src="graphics\example_gridContrast_blanks.png"  width="50%">

Note that on the diagonal, the colours are identical and as such nothing is seen, the contrast ratio is exactly 1 (no contrast)

Single contrast example, made by `imageContrastExample()` </br>
<img src="graphics\example_squareContrast.png"  width="40%">

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
