Welcome to pytest-group-by-class!
=============================

pytest-group-by-class allows you to split your test runs into groups of tests that belongs to the same class
to make it easier to split up your test runs.


Usage
----------------------
    # Install pytest-group-by-class
    pip install pytest-group-by-class

    # Split the tests into groups based on class and run the second group
    py.test --test-group-class --test-group-class-id 2

    # Split the tests into groups based on class and run the tests belonging ot class NameOfTheClassToBeExecuted
    py.test --test-group-class --test-group-class-name NameOfTheClassToBeExecuted



Why would I use this?
----------------------

Sometimes you may have some long running test jobs that take a
while to complete. This can be a major headache when trying to
run tests quickly. pytest-group-by-class allows you to easily say
"split my tests into groups of classes and run the second group".
This is primarily useful in the context of CI builds.
