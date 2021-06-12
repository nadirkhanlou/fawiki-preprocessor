# fawiki-preprocessor
A preprocessor for Persian Wikipedia articles

This script can be used to extract plaintext from Persian wikipedia articles extracted using [WikiExtractor](https://github.com/attardi/wikiextractor)

# Usage
To use the pre-processor, first check that you have the required libraries installed:
* [Hazm](https://github.com/sobhe/hazm)
* BS4
* NLTK
Then, use the guide below to pre-process your data. Note that the input file must be in the format of WikiExtractor's output

```
usage: preprocess.py [-h] [-i INPUT] [-o OUTPUT] [-n]

Required Parameters:
-i, --input  <PATH>  Path to the input file
-o, --output <PATH>  Path to the output file

Optional Parameters:
-h, --help               Help
-n, --normalize-output   Normalize the output text (default False)
```
