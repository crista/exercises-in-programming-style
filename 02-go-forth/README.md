Style #2
==============================

Constraints:

- Existence of an all-important data stack. All operations
  (conditionals, arithmetic, etc.) are done over data on the stack

- Existence of a heap for storing data that's needed for later
  operations. The heap data can be associated with names
  (i.e. variables). As said above, all operations are done over
  data on the stack, so any heap data that needs to be operated upon
  needs to be moved first to the stack and eventually back to the heap

- Abstraction in the form of user-defined "procedures" (i.e. names
  bound to a set of instructions), which may be called something else
  entirely

Possible names:

- Go-Forth (as in the Forth programming language)
- Stack machine

