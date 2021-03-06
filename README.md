coveralls-push utility
======================

Push any kind of coverage results to coveralls.io, the coverage files pushed are
then available at coveralls.io project [coveralls-push](https://coveralls.io/github/guillon/coveralls-push)

This tool does not aim at replacing standard coveralls.io tools for per-project
integration with github.com and travis.ci for instance.

The tool aims at providing a shared sandbox (actually this github project and
the associated coveralls.io project) for pushing any publicly visible
coverage result tree and have it displayed through coveralls.io.
Whatever the source tree pushed.

It is used for tutorials and demonstrations, for instance [qemu-tutorial](https://github.com/guillon/docker-qemu-tutorial)
or [qemu-plugins](https://github.com/guillon/docker-qemu-plugins)
in order to have people push their own example coverage files themselves with a temporarily shared secret key.

Actually, the workflow is summarized by this steps:
- the user generates a coverage file (including coverage info and sources), see below for the format
- the user pushes the coverage file using the `coveralls-push.py` and providing the requested secret key
  - the tool creates a source tree from the coverage file
  - the tool downloads an encrypted secret containing the tokens for the following steps and decrypts it from the secret key
  - the tool pushes the source tree to a unique orphean branch `coveralls-data/<id>` on the github.com project coveralls-push
  - the tool publishes the coverage and github unique branch ref to the coveralls.io project coveralls-push

Authentication is done through private tokens for github.com and coveralls.io, only available to the
coveralls-push github project admins. These tokens authenticate as the coveralls-push application account.

In order to allow other temporary contributors to push coverage information, a rotating secret key
is generated by the administrator and temporarily shared with them.

This key is used to decrypt an AES-256-CBC encrypted secret stored publicly on the github project
downloads. This encrypted secret contains the actual github and coveralls.io authentication tokens.
Tokens are rotated when the secret key expires and the publicly visible encrypted secret is updated
with new tokens and encrypted with a new secret key.


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

One can then browse the puslished coverage information at the given URL,
here at [job 11.1](https://coveralls.io/jobs/25749502).

Note that one must know the temporary secret key for using the tool.

Otherwise, one may open a support request to get a permanent access,
a github account is required for this use case.

Refer to all pushed covarges on coveralls.io project [coveralls-push](https://coveralls.io/github/guillon/coveralls-push).

Refer to github coveralls-push [project page](https://guillon.github.io/coveralls-push).

Refer to github coveralls-push [sources](https://github.com/guillon/coveralls-push).

