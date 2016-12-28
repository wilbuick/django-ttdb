"""Test runner that creates a database using a postgresql template db."""

import functools
import mock

from django.conf import settings
from django.test import TransactionTestCase
from django.test.runner import DiscoverRunner as Runner


def sql_table_creation_suffix(self):
    """Create a test database using the real database as a template."""
    return 'WITH TEMPLATE %s' % self.connection.settings_dict['ORIGINAL_NAME']


def create_test_db(self, *args, **kwargs):
    """Disable syncdb on test creation because database already contains data."""
    from django.core.management.commands import migrate

    if kwargs.get('reload', False) is True:
        if hasattr(self, 'create_test_db_kwargs'):
            kwargs = self.create_test_db_kwargs
        if hasattr(self, 'create_test_db_args'):
            args = self.create_test_db_args       
    else:
        self.create_test_db_kwargs = kwargs
        self.create_test_db_args = args

    if 'reload' in kwargs:
        del kwargs['reload']

    if self.connection.alias in settings.TTDB:
        with mock.patch.object(migrate, 'Command'):
            self._old_create_test_db(*args, **kwargs)
    else:
        self._old_create_test_db(*args, **kwargs)


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
            if connection.alias in settings.TTDB:
                connection.settings_dict['ORIGINAL_NAME'] = connection.settings_dict['NAME']

                connection.creation.sql_table_creation_suffix = functools.partial(
                    sql_table_creation_suffix, connection.creation)

                connection.creation._old_create_test_db = connection.creation.create_test_db
                connection.creation.create_test_db = functools.partial(
                    create_test_db, connection.creation)

        return super(TemplateDatabaseRunner, self).setup_databases(**kwargs)
