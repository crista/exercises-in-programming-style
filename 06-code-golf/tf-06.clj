":";exec java -cp "$HOME/.m2/repository/org/clojure/clojure/1.5.1/clojure-1.5.1.jar" clojure.main $0 $*

(require '[clojure.string :as s])

(doseq [c (take 25 
            (sort-by val > 
              (frequencies
                (remove 
                  #(some (partial = %) (s/split (slurp "../stop_words.txt") #","))
                  (re-seq #"[a-z]{2,}" (s/lower-case (slurp (first *command-line-args*))))))))]
  (printf "%s - %d\n" (first c) (nth c 1)))