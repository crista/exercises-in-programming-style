import sys, re, string

def extract_words(path_to_file):
    """
    Takes a path to a file and returns the non-stop
    words, after properly removing nonalphanumeric chars
    and normalizing for lower case
    """
    if type(path_to_file) is not str or not path_to_file:
        return []

    try:
        with open(path_to_file) as f:
            str_data = f.read()
    except IOError as e:
        print "I/O error({0}) when opening {1}: {2}".format(e.errno, path_to_file, e.strerror)
        return []
    
    pattern = re.compile('[\W_]+')
    word_list = pattern.sub(' ', str_data).lower().split()

    try:
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
    except IOError as e:
        print "I/O error({0}) when opening ../stops_words.txt: {1}".format(e.errno, e.strerror)
        return []

    stop_words.extend(list(string.ascii_lowercase))
    return [w for w in word_list if not w in stop_words]

