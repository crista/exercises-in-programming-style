import sys, re, string

def extract_words(path_to_file):
    """
    Takes a path to a file and returns the non-stop
    words, after properly removing nonalphanumeric chars
    and normalizing for lower case
    """
    words = re.findall('[a-z]{2,}', open(path_to_file).read().lower())
    stopwords = set(open('../stop_words.txt').read().split(','))
    return [w for w in words if w not in stopwords]

