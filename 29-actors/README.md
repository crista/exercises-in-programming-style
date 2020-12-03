Style #29
==============================

Similar to the letterbox style, but where the 'things' have
independent threads of execution.

Constraints:

- The larger problem is decomposed into 'things' that make sense for
  the problem domain 

- Each 'thing' has a queue meant for other \textit{things} to place
messages in it

- Each 'thing' is a capsule of data that exposes only its
ability to receive messages via the queue

- Each 'thing' has its own thread of execution independent of the
others.

Possible names:

- Free agents
- Active letterbox
- Actors
