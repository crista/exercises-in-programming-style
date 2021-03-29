":";exec java -cp "$HOME/.m2/repository/org/clojure/clojure/1.5.1/clojure-1.5.1.jar" clojure.main $0 $*

; Sort of a hack; Clojure isn't really intended as a scripting language. :-/

(require '[clojure.string :refer [split]]
         '[clojure.java.io :refer [reader]]
         '[clojure.pprint :refer [pprint]])

(defn stopwords
  "Reads a set of comma-separated stopwords from the given filename."
  [file]
  (-> file
      slurp
      (split #"\s+,\s+")
      set))

(defn words
  "Splits a string into a sequence of words."
  [string]
  (clojure.string/split string #"[^a-zA-Z]+"))

(defn normalize
  "Normalizes split words to terms."
  [word]
  (.toLowerCase word))

(defn too-short?
  "Is a word too short for consideration?"
  [word]
  (<= (.length word) 2))

; Lazily split the file into lines, explode lines into words, normalize into
; terms, reject unsuitable candidates, compute frequencies, and take the top
; 25.
(with-open [f (reader "../pride-and-prejudice.txt")]
  (->> f
       line-seq
       (mapcat words)
       (map normalize)
       (remove too-short?)
       (remove (stopwords "../stop_words.txt"))
       frequencies
       (sort-by second)
       reverse
       (take 25)
       pprint))
