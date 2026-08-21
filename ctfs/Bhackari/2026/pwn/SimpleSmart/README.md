pwn
 Vego
A junior intern at a legacy systems team wrote a tiny custom reference-counting library in C as a quick demo.

They added a small REPL to test something based on strong/weak pointer semantics and called it SimpleSmart. The implementation looked simple: checksum in destructors, a compact API, and a friendly CLI... but it was written in a hurry.

Your job? Audit the demo and see what breaks.

If you manage to retrieve the flag, we may even consider giving you a small raise :)
