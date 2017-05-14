coveralls-push utility
======================

Push coverage results to coveralls, the coverages pushed are
available at coveralls URL: https://coveralls.io/github/guillon/coveralls-push

Usage
=====

For instance build the local example with:

    $ make

Then one can inspect the expected YML file input format in:

    $ cat examples/hello-cov.yml
    "hello.exe/main":
    ...
    - [ 1, "0x400526:     55                      push   %rbp" ]
    ...
    
In order to push this coverage file, do:

    $ ./coveralls-push examples/hello-cov.yml
    ...
    Succesfully pushed coverage
    Identifier: Job #8.1
    Browse at: https://coveralls.io/jobs/25748408

You can then browse your coverage, here at:
https://coveralls.io/jobs/25748408

NOTE: your github account may be requested by
your git client if not already configured.

NOTE: one must be registered as contributor to
the coveralls-push project in order to be able
to push the sources and coverage information.
