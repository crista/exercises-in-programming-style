Style #16
==============================

Constraints:

- Larger problem is decomposed into entities using some form of abstraction
  (objects, modules or similar)

- The entities are never called on directly for actions

- Existence of an infrastructure for publishing and subscribing to
  events, aka the bulletin board

- Entities post event subscriptions (aka 'wanted') to the bulletin
  board and publish events (aka 'offered') to the bulletin board. the
  bulletin board does all the event management and distribution

Possible names:

- Bulletin board
- Publish-Subscribe
