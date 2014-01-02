Style #25
==============================

This style is a variation of style #09, The One, with the following additional constraints:

Constraints:

- Core program functions have no side effects of any kind, including IO

- All IO actions must be contained in computation sequences that are
  clearly separated from the pure functions

- All sequences that have IO must be called from the main program

Possible names:

- Quarantine
- Monadic IO
- Imperative functional style
