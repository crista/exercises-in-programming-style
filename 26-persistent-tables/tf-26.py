#!/usr/bin/env python
import sys, re, string, sqlite3, os.path

#
# The relational database of this problem consists of 3 tables:
# documents, words, characters
#
def create_db_schema(connection):
    c = connection.cursor()
    c.execute('''CREATE TABLE documents (id INTEGER PRIMARY KEY AUTOINCREMENT, name)''')
    c.execute('''CREATE TABLE words (id, doc_id, value)''')
    c.execute('''CREATE TABLE characters (id, word_id, value)''')
    connection.commit()
    c.close()

def load_file_into_database(path_to_file, connection):
    """ Takes the path to a file and loads the contents into the database,
    then returns the doc_id """
    def _extract_words(path_to_file):
        with open(path_to_file) as f:
            str_data = f.read()
        pattern = re.compile('[\W_]+')
        word_list = pattern.sub(' ', str_data).lower().split()
        with open('../stop_words.txt') as f:
            stop_words = f.read().split(',')
        stop_words.extend(list(string.ascii_lowercase))
        return [w for w in word_list if not w in stop_words]

    words = _extract_words(path_to_file)

    # Now let's add data to the database
    # Add the document itself to the database
    c = connection.cursor()
    c.execute("INSERT INTO documents (name) VALUES (?)", (path_to_file,))
    c.execute("SELECT id from documents WHERE name=?", (path_to_file,))
    doc_id = c.fetchone()[0]

    # Add the words to the database
    c.execute("SELECT MAX(id) FROM words")
    row = c.fetchone()
    word_id = row[0]
    if word_id == None:
        word_id = 0
    for w in words:
        c.execute("INSERT INTO words VALUES (?, ?, ?)", (word_id, doc_id, w))
        # Add the characters to the database
        char_id = 0
        for char in w:
            c.execute("INSERT INTO characters VALUES (?, ?, ?)", (char_id, word_id, char))
            char_id += 1
        word_id += 1
    connection.commit()
    c.close()
    return doc_id

#
# Create if it doesn't exist
#
if not os.path.isfile('tf.db'):
    with sqlite3.connect('tf.db') as connection:
        create_db_schema(connection)
        load_file_into_database(os.path.abspath(sys.argv[1]), connection)

# Now, let's query
with sqlite3.connect('tf.db') as connection:
    c = connection.cursor()
    
    # Determine if we need to generate new words based on the filename provided
    c.execute("SELECT id FROM documents WHERE name=?", (os.path.abspath(sys.argv[1]),))
    row = c.fetchone()
    if row == None:
        # document ID didn't exist: create words
        doc_id = load_file_into_database(os.path.abspath(sys.argv[1]), connection)
    else:
        # Get the document ID
        doc_id = row[0]
    
    # Get the cached results from the database based on the filename provided
    c.execute("SELECT value, COUNT(*) as C FROM words WHERE doc_id=? GROUP BY value ORDER BY C DESC", (doc_id,))
    for i in range(25):
        row = c.fetchone()
        if row != None:
            print(row[0], '-', str(row[1]))
