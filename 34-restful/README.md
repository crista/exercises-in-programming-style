Style #34
==============================

REST = REpresentational State Transfer (http://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)

REST is a style for network-based interactive applications that
underlies the Web. The example here doesn't go over the network, but
preserves the main contraints of REST, which are:

- Interactive: end-to-end between an active agent (e.g. a person) and a backend

- Separation between Client (user interface) and Server (data storage)

- Statelessness, as in client--stateless-server: every request from
  client to server must contain all the information necessary for the
  server to serve the request. The server cannot store
  context of the interaction. Session state is on the client.

- Uniform interface: resources that are created and retrieved,
  resource identifiers and hypermedia representation that is the
  engine of application state

Additionally, the networked style has the following contraints, not shown here:

- Cache

- Layered system

- Code-on-demand

Possible names:

- RESTful
- Stateless Ping-Pong

