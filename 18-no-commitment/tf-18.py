#!/usr/bin/env python

import sys, ConfigParser, imp

def load_plugins():
    config = ConfigParser.ConfigParser()
    config.read("config.ini")
    words_plugin = config.get("Plugins", "words")
    frequencies_plugin = config.get("Plugins", "frequencies")
    global tfwords, tffreqs
    tfwords = imp.load_compiled('tfwords', words_plugin)
    tffreqs = imp.load_compiled('tffreqs', frequencies_plugin)

#
# The main function
#

load_plugins()
word_freqs = tffreqs.top25(tfwords.extract_words(sys.argv[1]))

for tf in word_freqs:
    print tf[0], ' - ', tf[1]

