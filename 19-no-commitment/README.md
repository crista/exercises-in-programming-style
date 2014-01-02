Style #20
==============================

Constraints:

- The problem is decomposed using some form of abstraction
  (procedures, functions, objects, etc.)

- All or some of those abstractions are physically encapsulated into
  their own, usually pre-compiled, packages. Main program and each of
  the packages are compiled independently. These packages are loaded
  dynamically by the main program, usually in the beginning (but not
  necessarily).

- Main program uses functions/objects from the dynamically-loaded
  packages, without knowing which exact implementations will be
  used. New implementations can be used without having to adapt or
  recompile the main program.

- External specification of which packages to load. This can be done
  by a configuration file, path conventions, user input or other
  mechanisms for external specification of code to be linked at run
  time.

Possible names:

- No commitment
- Plugins
- Dependency injection
