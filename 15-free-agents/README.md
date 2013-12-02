Style #15
==============================

Similar to the letterbox style, but where the 'things' have
independent threads of execution.

Constraints:

- The larger problem is decomposed into 'things' that make sense for
  the problem domain 

- Each 'thing' is a capsule of data that exposes one single procedure,
  namely the ability to receive and dispatch messages that are sent to
  it

- Each 'thing' has its own thread of execution independent of the others

- Each 'thing' has a queue where messages to it are placed

- Message dispatch can result in sending the message to another 'thing'

Possible names:

- Free agents
- Active letterbox
- Actors
