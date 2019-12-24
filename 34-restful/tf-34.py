#!/usr/bin/env python
import re, string, sys

with open("../stop_words.txt") as f:
    stops = set(f.read().split(",")+list(string.ascii_lowercase))
# The "database"
data = {}

# Internal functions of the "server"-side application
def error_state():
    return "Something wrong", ["get", "default", None]

# The "server"-side application handlers
def default_get_handler(args):
        rep = "What would you like to do?"
        rep += "\n1 - Quit" + "\n2 - Upload file"
        links = {"1" : ["post", "execution", None], "2" : ["get", "file_form", None]}
        return rep, links

def quit_handler(args):
    sys.exit("Goodbye cruel world...")

def upload_get_handler(args):
    return "Name of file to upload?", ["post", "file"]

def upload_post_handler(args):
    def create_data(fn):
        if fn in data:
            return
        word_freqs = {}
        with open(fn) as f:
            for w in [x.lower() for x in re.split("[^a-zA-Z]+", f.read()) if len(x) > 0 and x.lower() not in stops]:
                word_freqs[w] = word_freqs.get(w, 0) + 1
        wf = list(word_freqs.items())
        data[fn] = sorted(wf,key=lambda x: x[1],reverse=True)

    if args == None:
        return error_state()
    filename = args[0]
    try:
        create_data(filename)
    except:
        print("Unexpected error: %s" % sys.exc_info()[0])
        return error_state()
    return word_get_handler([filename, 0])

def word_get_handler(args):
    def get_word(filename, word_index):
        if word_index < len(data[filename]):
            return data[filename][word_index]
        else:
            return ("no more words", 0)

    filename = args[0]; word_index = args[1]
    word_info = get_word(filename, word_index)
    rep = '\n#{0}: {1} - {2}'.format(word_index+1, word_info[0], word_info[1])
    rep += "\n\nWhat would you like to do next?"
    rep += "\n1 - Quit" + "\n2 - Upload file"
    rep += "\n3 - See next most-frequently occurring word"
    links = {"1" : ["post", "execution", None],
             "2" : ["get", "file_form", None],
             "3" : ["get", "word", [filename, word_index+1]]}
    return rep, links

# Handler registration
handlers = {"post_execution" : quit_handler,
            "get_default" : default_get_handler,
            "get_file_form" : upload_get_handler,
            "post_file" : upload_post_handler,
            "get_word" : word_get_handler }

# The "server" core
def handle_request(verb, uri, args):
    def handler_key(verb, uri):
        return verb + "_" + uri

    if handler_key(verb, uri) in handlers:
        return handlers[handler_key(verb, uri)](args)
    else:
        return handlers[handler_key("get", "default")](args)

# A very simple client "browser"
def render_and_get_input(state_representation, links):
    print(state_representation)
    sys.stdout.flush()
    if type(links) is dict: # many possible next states
        input = sys.stdin.readline().strip()
        if input in links:
            return links[input]
        else:
            return ["get", "default", None]
    elif type(links) is list: # only one possible next state
        if links[0] == "post": # get "form" data
            input = sys.stdin.readline().strip()
            links.append([input]) # add the data at the end
            return links
        else: # get action, don't get user input
            return links
    else:
        return ["get", "default", None]

request = ["get", "default", None]
while True:
    # "server"-side computation
    state_representation, links = handle_request(*request)
    # "client"-side computation
    request = render_and_get_input(state_representation, links)
