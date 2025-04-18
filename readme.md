<div align="center" style="display:grid;place-items:center;">

![Sea Logo](res/logo.svg)

# Sea

[guide](doc/guide.md) - [samples](samples/)

</div>

> _C for the modern world._

---

Sea is a general-purpose language made to allow programmers to write low-level,
performant, and portable code without needing to write C.

> If you are conversing about Sea and C, then you may want to pronounce Sea as
> `see-uh` instead of `see` to prevent ambiguity. You could also call it
> `fish c` or any other random thing that helps to fix the ambiguity.

**Features:**

- 100% interoperability with C. All C libraries can be cleanly used in Sea, and vice-versa too.
  - C interoperability is also completely overhead-free!
- As little ambiguity as possible (except in the pronunciation of Sea and C, whoops).
- Equally as fast as C since Sea gets transpiled to C.

**Inspired By:**

- C, obviously
- [Odin](https://odin-lang.org)
- [V](https://vlang.io)
- [Cyclone](https://cyclone.thelanguage.org), partially
- [Go](https://go.dev)

## Installation

Sea is currently very unfinished. If you still want to use it, you can use the
prototype implementation with `python3 -m proto path/to/input/file.sea -rs .`

You can also build the new compiler using `python3 -m proto src/main.sea -s .`

## Why?

I simply enjoy writing languages! :P

For a more "real" reason: I love writing C, however I also like modern syntax
and a more... usable standard library.

> C's stdlib is absolutely usable, however a modern stdlib designed around
> modern practices is significantly more usable than a stdlib designed around
> code practices from the 70s.

Of note, the Sea standard library can be 100% ignored and you can use solely the
C standard library if you wish.
