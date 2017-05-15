coveralls-push utility
======================

Push coverage results to coveralls, the coverages pushed are
then available at coveralls.io project [coveralls-push](https://coveralls.io/github/guillon/coveralls-push)

Usage
=====

One can inspect the expected YML file input format [example](example-hello.yml)

Clone this repository, or simply get the script file with:

    $ curl -Lo coveralls-push.py https://github.com/guillon/coveralls-push/raw/master/coveralls-push.py
    $ chmod +x coveralls-push.py

Here is for instance a partial content of the example:

    $ curl -Lo example-hello.yml https://github.com/guillon/coveralls-push/raw/master/example-hello.yml
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
    Please provide the password key for coveralls-push: <enter here the expected key>
    ...
    Succesfully pushed coverage
    Identifier: Job #11.1
    Browse at:  https://coveralls.io/jobs/25749502

You can then browse your coverage at the given URL, here at [job 11.1](https://coveralls.io/jobs/25749502).

Note that the key should have been shared previously.
Otherwise open a support request to get an access.

Refer to all pushed covarges on coveralls.io project [coveralls-push](https://coveralls.io/github/guillon/coveralls-push).

Refer to github coveralls-push [project page](https://guillon.github.io/coveralls-push).

Refer to github coveralls-push [sources](https://github.com/guillon/coveralls-push).

