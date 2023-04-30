Style #12
==============================

Constraints:

- The larger problem is decomposed into 'things' that make sense for
  the problem domain 

- Each 'thing' is a capsule of data that exposes one single procedure,
  namely the ability to receive and dispatch messages that are sent to
  it

- Message dispatch can result in sending the message to another capsule

Possible names:

- Letterbox
- Messaging style
- Objects
- Actors

## Style #12.2

Constraints:

- For each 'thing' class, let's bring the `info` methods from the Things style (#11)

- In the Things style, we used inheritance via a Python call to `super` to call a shared function from a base class

- We should apply this concept of code-reuse, but make sure to do so without using inheritance

- Just like in style 11, we will not be calling `info` in the main routine

Possible names:

- Delegation
