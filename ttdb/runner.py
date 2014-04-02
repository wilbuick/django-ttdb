"""Test runner that creates a database using a postgresql template db."""

import functools

from django import VERSION as DJANGO_VERSION
from django.test import TransactionTestCase

try:
    from django.test.runner import DiscoverRunner as Runner
except ImportError:
    from django.test.simple import DjangoTestSuiteRunner as Runner


def sql_table_creation_suffix(self):
    """Create a test database using the real database as a template."""
    return 'WITH TEMPLATE %s' % self.connection.settings_dict['ORIGINAL_NAME']


def create_test_db(self, verbosity=1, autoclobber=False):
    """Disable syncdb on test creation because database already contains data."""
    test_database_name = self._get_test_db_name()

    if verbosity >= 1:
        test_db_repr = ''
        if verbosity >= 2:
            test_db_repr = " ('%s')" % test_database_name
        print("Creating test database for alias '%s'%s..." % (
            self.connection.alias, test_db_repr))

    self.connection.settings_dict['ORIGINAL_NAME'] = self.connection.settings_dict['NAME']
    self._create_test_db(verbosity, autoclobber)

    self.connection.close()
    self.connection.settings_dict["NAME"] = test_database_name

    if DJANGO_VERSION[0] == 1 and DJANGO_VERSION[1] == 4: 
        # Confirm the feature set of the test database
        self.connection.features.confirm()

    self.connection.cursor()

    return test_database_name


class TemplateDatabaseRunner(Runner):

    """Test runner that patches the create test database methods.

    This runner patches the methods that create a test database so that a test 
    database can be created based on a postgres template database. It looks for 
    the TEST_TEMPLATE option in the settings.DATABASES dictionary.

    """

    def __init__(self, **kwargs):
        """Prepare runner kwargs."""
        super(TemplateDatabaseRunner, self).__init__(**kwargs)

    def setup_databases(self, **kwargs):
        """Handle template test databases differently."""
        from django.db import connections

        for alias in connections:
            connection = connections[alias]
            if connection.settings_dict.get('TEST_TEMPLATE', False) is True:

                connection.creation.sql_table_creation_suffix = functools.partial(
                    sql_table_creation_suffix, connection.creation)

                connection.creation.create_test_db = functools.partial(
                    create_test_db, connection.creation)

        return super(TemplateDatabaseRunner, self).setup_databases(**kwargs)
