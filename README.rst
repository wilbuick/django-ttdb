=============================
Django Template Test Database
=============================

.. image:: https://secure.travis-ci.org/wilbuick/django-ttdb.png
    :alt: Build Status
    :target: http://travis-ci.org/wilbuick/django-ttdb

Django template test database is a testing tool for django that provides an alternative
to fixtures when tools like FactoryBoy aren't suitable. The use case is simple: for 
integration tests that require the test database to be populated with a specific (large) 
set of test data before they will even run. Loading this test data using fixtures would 
be very slow. This problem is solved by loading the test data during database creation 
at the database level and allows us to avoid all of the overhead by loading data through
django.

How it works
------------

It uses postgresql database templates to create the test database. Because of this it 
only works with postgresql, however if you are interested in extending this to support 
other database backends feel free to do so.

To make this work we need three parts:

* A custom test runner to customize test db creation
* Custom test cases to prevent the test database being flushed after each run
* Decorator that allows existing test cases to run against a template test database.

Documentation
-------------

`Documentation`_ can be found on `readthedocs.org`_.

.. _`Documentation`: http://django-ttdb.readthedocs.org/en/latest/
.. _`readthedocs.org`: http://readthedocs.org
