# Colour Contrast checker
I needed something that would allow me to check the colour contrast ratios of lots of colours at once, so i made it

## Input
**Contrast ratio:**
- will expect either a float (between 1 and 21 inclusive)
- empty value (will then defult to 4.5)
- a WCAG contrast code, AA or AAA and large or normal (eg AAA-L or AA-N)


**Hex List:** 
- empty (will randomly generate 3 hex values) 
- string that gets regexes to take the first 6 values after every `#`
- int will rng that many hex values
