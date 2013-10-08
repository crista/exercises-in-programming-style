#include <iostream>
#include <fstream>
#include <sstream>
#include <regex>
#include <map>

using namespace std;

struct Freq {
  string word;
  int freq;
  Freq(string w, int f) : word(w), freq(f) {}
};


//
// Helpers
//

static int tospace(int c)
{
  if (!isalpha(c))
    return ' ';
  else
    return c;
}

static vector<string> get_stop_words()
{
  string word;
  vector<string> stop_words;
  ifstream is("../stop_words.txt");
  
  while (getline(is, word, ',')) {
    stop_words.push_back(word);
  }

  char w[2];
  w[1] = '\0';
  for (char c : "abcdefghijklmopqrstuvwxyz") {
    w[0] = c;
    stop_words.push_back(string(w));
  } 

  sort(stop_words.begin(), stop_words.end());
  
  return stop_words;
}

static bool sort_by_freq(Freq x, Freq y)
{
  return y.freq < x.freq;
}

//
// The functions
//

/** Takes a path to a file and returns the entire
    contents of the file as a string
*/
string read_file(const char* path_to_file)
{
  string data;
  ifstream is(path_to_file, std::ifstream::binary);

  if (is) {
    is.seekg (0, is.end);
    int length = is.tellg();
    is.seekg (0, is.beg);

    char* buffer = new char [length + 1];
    is.read(buffer,length);
    buffer[length] = '\0';
    data = buffer;
    delete [] buffer;
  }
  return data;
}

/** Takes a string and returns a copy with all nonalphanumeric 
    chars replaced by white space
*/
string filter_chars(string str_data)
{
  std::transform(str_data.begin(), str_data.end(), str_data.begin(), ::tospace);
  return str_data;
}


/** Takes a string and returns a copy with all chars in lower case
*/
string normalize(string str_data)
{
  std::transform(str_data.begin(), str_data.end(), str_data.begin(), ::tolower);
  return str_data;
}    
  

/** Takes a string and scans for words, returning
    a list of words.
*/
vector<string> scan(string str_data)
{
  string word;
  vector<string> words;
  istringstream is(str_data);
  
  while (is >> word) {
    words.push_back(word);
  }
  
  return words;
}

/** Takes a list of words and returns a copy with all stop 
    words removed
*/
vector<string> remove_stop_words(vector<string> words)
{
  vector<string> stop_words = get_stop_words();
  vector<string> filtered_list;
  
  filtered_list.reserve(words.size());
  for (string w : words) {
    if (!binary_search(stop_words.begin(), stop_words.end(), w))
      filtered_list.push_back(w);
  }
  
  return filtered_list;
}

/** Takes a list of words and returns a dictionary associating
    words with frequencies of occurrence
*/
map<string,int> frequencies(vector<string> words)
{
  map<string,int> freq;
  
  for (string w : words) {
    map<string,int>::iterator it = freq.find(w);
    if (it != freq.end()) {
      it->second++;
    }
    else {
      freq.insert(pair<string,int>(w,1));
    }
  }
  return freq;
}

/** Takes a dictionary of words and their frequencies
    and returns a list of pairs where the entries are
    sorted by frequency
*/
vector<Freq> sort(map<string,int> word_freq)
{
  vector<Freq> out_list;
  
  out_list.reserve(word_freq.size());
  for (pair<string,int> p : word_freq) {
    out_list.push_back(Freq(p.first, p.second));
  }
  sort(out_list.begin(), out_list.end(), sort_by_freq);
  return out_list;
}

//
// The main function
//

int main(int argc, char* argv[])
{
  vector<Freq> word_freqs = sort(frequencies(remove_stop_words(scan(normalize(filter_chars(read_file(argv[1])))))));
  
  for (vector<Freq>::iterator it = word_freqs.begin(); it != word_freqs.begin()+25; it++)
    cout << it->word << " - " << it->freq << endl;

  return 0;
}
