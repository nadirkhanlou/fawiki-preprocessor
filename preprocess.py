import re
import timeit
import sys
import getopt

import hazm
#import parsivar
from bs4 import BeautifulSoup, BeautifulStoneSoup

import nltk
from nltk import word_tokenize

import codecs

# Regular expression for different character types in persian
# courtesy of https://github.com/mirhmousavi/Regex.Persian.Language

# All possible space characters
space = '\u0020\u2000-\u200F\u2028-\u202F'

# Punctuation
punctuation = (
                '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~«»'
                + '–'   # EN dash \u2013
                + '—'   # EM dash \u2014
                + '…'   # Horizontal Ellipsis \u2026
            )

# Persian and arabic punctiation
persian_punctuation = '،؛؟ـ٪٫٬'
# = '\u060C\u061B\u061F\u0640\u066A\u066B\u066C'

# Persian alphabet
persian_alpha = 'ءآأؤإئابتثجحخدذرزسشصضطظعغفقلمنهوَُِّٕپچژکگھی'
# = '\u0621-\u0628\u062A-\u063A\u0641-\u0642\u0644-\u0648\u064E-\u0651\u0655\u067E\u0686\u0698\u06A9\u06AF\u06BE\u06CC'

# Arabic characters common in persian texts
additional_arabic_alpha = 'ةكىيًٍە'
# = '\u0629\u0643\u0649-\u064B\u064D\u06D5'

# Other relevant alphabet characters appearing in persian text
other_alpha = (
                'ٔ'        # Hamzah \u0654
                + 'ٰ'    # Superscript Alef \u0670
                + 'ۀ'   # Arabic Heh with Yeh above \u06c0
                + 'ﷲ'   # Arabic Ligature Allah Isolated Form \ufdf2
            )

# Persian digits
persian_digits = '۰۱۲۳۴۵۶۷۸۹'
# = '\u06F0-\u06F9'

# Arabic digits
arabic_digits = '٠١٢٣٤٥٦٧٨٩'
# = '\u0660-\u0669'

# Combine alphabets
alpha = persian_alpha + additional_arabic_alpha + other_alpha

# Combine digits
digits = persian_digits + arabic_digits

# Combine alphabets and digits
alpha_digits = alpha + digits

all_valid_chars = (
                    alpha_digits +
                    punctuation +
                    persian_punctuation +
                    space
                )

def GetArticles(filename):
    # Load the raw xml file
    xml = open(filename, encoding="utf8").read()
    articles = [x+'</doc>' for x in xml.split('</doc>')]

    return articles[:-1]    # Last element in list is '</doc>'

# Normalize using the hazm normalzier
def NormalizeHazm(text):
    hazm_normalizer = hazm.Normalizer()
    return hazm_normalizer.normalize(text)

# Tokenize the (normalized) text using the hazm word tokenizer
def TokenizeHazm(text):
    return hazm.word_tokenize(text)

def PreprocessText(filename, outputName="out", normalize_output=False):
    # A string containing all valid characters
    global all_valid_chars

    file = codecs.open(outputName, "w", "utf-8")

    # Fetch the articles from the dump file
    print("LOG: Fetching articles from the dump file")
    articles = GetArticles(filename)
    print("LOG: Total number of articles:", len(articles))

    # Initialize counters
    n = 0
    n_empty = 0

    print("LOG: Initiating the cleaning process")
    print("LOG: Output normalization is set to", normalize_output)
    start = timeit.default_timer()
    for a in articles:
        n += 1
        if (n % 50000 == 0):
            print("LOG: Processed", n, "articles")
        
        # Check whether article has content
        soup = BeautifulSoup(a, 'html.parser')
        title = soup.find("doc")['title']
        plaintext = soup.get_text().strip('\n')
        # Empty articles only have a title in the first line
        if (title == plaintext or plaintext == ""):
            n_empty += 1
        else:
            paragraphs = plaintext.split('\n')
            for p in paragraphs:
                if not (p.isspace() or p == ''):
                    # Normalize and tokenize the paragraph
                    norm = NormalizeHazm(p)
                    tokens = TokenizeHazm(norm)
                    # Discard all invalid tokens (i.e. tokens with illegal characters)
                    valid_tokens = [w for w in tokens if re.match('^['+all_valid_chars+']{1,}$', w)]
                    # Join remaining tokens and normalize (in order to remove extra characters)
                    if normalize_output:
                        output_paragraph = NormalizeHazm(" ".join(valid_tokens))
                    else:
                        output_paragraph = " ".join(valid_tokens)
                    # Write output to file
                    file.write(output_paragraph+'\n')

    finish = timeit.default_timer()
    file.close()

    print("LOG: Finished processing the articles. Total number of articles processed:", n)
    print("LOG: number of non-empty articles:", n - n_empty)
    print("LOG: number of empty articles:", n_empty)
    print("LOG: Time elapsed:", '%.2f'%(finish - start), "seconds")

def main(argv):
    infile = ''
    outfile = ''
    normalize_output = False
    try:
        opts, args = getopt.getopt(argv,"hi:o:n", ["help", "input=", "output=", "normalize-output"])
    except getopt.GetoptError:
        print("usage: preprocess.py [-h] [-i INPUT] [-o OUTPUT] [-n]")
        print("\n")
        print("error: the following arguments are required: -i, -o")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("usage: preprocess.py [-h] [-i INPUT] [-o OUTPUT] [-n]")
            print()
            print("Required Parameters:")
            print("-i, --input  <PATH>  Path to the input file")
            print("-o, --output <PATH>  Path to the output file")
            print()
            print("Optional Parameters:")
            print("-h, --help               Help")
            print("-n, --normalize-output   Normalize the output text (default False)")
            sys.exit()
        elif opt in ["-i", "--input"]:
            infile = arg
        elif opt in ["-o", "--output"]:
            outfile = arg
        elif opt in ["n", "--normalize-output"]:
            normalize_output = True

    
    if infile == '' or outfile == '':
        print("usage: preprocess.py [-h] [-i INPUT] [-o OUTPUT] [-n]")
        print()
        print("error: the following arguments are required: -i, -o")
        sys.exit(2)
    
    PreprocessText(infile, outfile, normalize_output)

if __name__ == "__main__":
    argv = sys.argv[1:]
    main(argv)
    