Style #30
==============================

Very similar to style #29, but with an additional twist

Constraints:

- Input data is divided in chunks, similar to what an inverse multiplexer does to input signals

- A map function applies a given worker function to each chunk of data, potentially in parallel

- The results of the many worker functions are reshuffled in a way
  that allows for the reduce step to be also parallelized

- The reshuffled chunks of data are given as input to a second map
  function that takes a reducible function as input

Possible names:

- Double inverse multiplexer 
- Map-reduce 
- Hadoop style
