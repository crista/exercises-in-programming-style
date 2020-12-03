Style #31
==============================

Constraints:

- Input data is divided in chunks, similar to what an inverse multiplexer does to input signals

- A map function applies a given worker function to each chunk of data, potentially in parallel

- A reduce function takes the results of the many worker functions and recombines them into a coherent output

Possible names:

- Map-reduce
- Inverse multiplexer (check out electronics)
