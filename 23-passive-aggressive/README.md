Style #23
==============================

Constraints:

- Every single procedure and function checks the sanity of its
  arguments and refuses to continue when the arguments are
  unreasonable, throwing an exception

- When calling out other functions, program functions only check for exceptions if they are in a position to react meaningully

- Exception handling occurs at higher levels of function call chains, wherever it is meaningul to do so

Possible names:

- Passive aggressive


