":";exec java -cp "$HOME/.m2/repository/org/clojure/clojure/1.5.1/clojure-1.5.1.jar" clojure.main $0 $*

(doseq [c (take 25 
            (sort-by val > 
              (frequencies
                (remove 
                  #(contains? (set (.split (slurp "../stop_words.txt") ",")) %)
                  (re-seq #"[a-z]{2,}" (.toLowerCase (slurp (first *command-line-args*))))))))]
  (println (first c) "-" (nth c 1)))
