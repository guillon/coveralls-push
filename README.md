coveralls-push utility
======================

Push coverage results to coveralls, the coverages pushed are
then available at coveralls URL:
https://coveralls.io/github/guillon/coveralls-push

Usage
=====

One can inspect the expected YML file input format at
https://github.com/guillon/coveralls-push/blob/master/example-hello.yml

Clone this repository, or simply get the script file with:

    $ curl -o coveralls-push.py https://github.com/guillon/coveralls-push/raw/master/coveralls-push.py
    $ chmod +x coveralls-push.py

Here is for instance a partial content of the example:

    $ cat example-hello.yml
    "hello.exe/main":
    - [ null, "// file hello.exe" ]   # This source line is not applicable
    ...
    - [ 3, "0x400526:     55                      push   %rbp" ]   # This source line is covered 3 times
    ...
    "hello.exe/puts":
    - [ 0, "0x000566:   68 00 00 00 00          pushq  $0x0" ]    # This source line is not covered

For instance, push the example with:

    $ ./coveralls-push examples-hello.yml
    ...
    Password for 'https://coveralls-push@github.com': <enter here the coveralls-push password>
    ...
    Succesfully pushed coverage
    Identifier: Job #11.1
    Browse at:  https://coveralls.io/jobs/25749502

You can then browse your coverage, here at:
https://coveralls.io/jobs/25749502

Note that one must know the coveralls-push password which is requested
for updating the coverages data repository.

Alternatively, one can push as its own github account login with:

    $ env COV_USER=<github_login> ./coveralls-push examples-hello.yml
    ...

In this case the github user must be a collaborator of the coveralls-push repository.

Refer to github coveralls-push doc at:
https://guillon.github.io/coveralls-push

Refer to sources at:
https://github.com/coveralls-push

Refer to all coverages pushed at:
https://coveralls.io/github/guillon/coveralls-push
