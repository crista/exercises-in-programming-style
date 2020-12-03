Style #15
==============================

Constraints:

- Larger problem is decomposed into entities using some form of abstraction
  (objects, modules or similar)

- The entities are never called on directly for actions

- The entities provide interfaces for other entities to be
  able to register callbacks

- At certain points of the computation, the entities call on the other
  entities that have registered for callbacks

Possible names:

- Hollywood agent: "don't call us, we'll call you"
- Inversion of control
- Callback heaven/hell
