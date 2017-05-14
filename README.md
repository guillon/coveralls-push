coveralls-push utility
======================

Push coverage results to coveralls, the coverages pushed are
available at coveralls URL: https://coveralls.io/github/guillon/coveralls-push

Usage
=====

One can inspect the expected YML file input format at
https://github.com/guillon/coveralls-push/blob/master/example-hello.yml

Clone this repository or simply get the script file with:

    $ curl -o coveralls-push.py https://github.com/guillon/coveralls-push/raw/master/coveralls-push.py
    $ chmod +x coveralls-push.py

Here is for instance a partial content of the exemple:

    $ cat example-hello.yml
    "hello.exe/main":
    - [ null, "// file hello.exe" ]   # This source line is not applicable
    ...
    - [ 3, "0x400526:     55                      push   %rbp" ]   # This source line is covered 3 times
    ...
    "hello.exe/puts":
    - [ 0, "0x000566:   68 00 00 00 00          pushq  $0x0" ]    # This source line is not covered

In order to push a coverage file, you need a github account
(login `<github_user>` below) and the coveralls-push.py script.

For instance, push the example with:

    $ env COV_USER=<github_user> ./coveralls-push examples-hello.yml
    ...
    Succesfully pushed coverage
    Identifier: Job #11.1
    Browse at:  https://coveralls.io/jobs/25749502

You can then browse your coverage, here at:
https://coveralls.io/jobs/25749502

NOTE: your github account password may be requested by
your git client if not already configured.

NOTE: one must be registered as contributor to
the github  coveralls-push project in order to be able
to push the sources and coverage information.

Refer to github coveralls-push doc at:
https://guillon.github.io/coveralls-push

Refer to sources at:
https://github.com/coveralls-push

Refer to all coverages pushed at:
https://coveralls.io/github/guillon/coveralls-push
