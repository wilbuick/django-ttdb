"""Test cases that switch the default test database to a different db."""

import mock

from django.conf import settings
from django.test import TestCase
from django.test import TransactionTestCase
from django.test import LiveServerTestCase
from django.core.management import call_command


class TemplateDBMixin(object):

    """Mixin class that defines methods for interacting with the template db."""

    template_database = None
    reload_after_test = True

    def _use_template_database(self):
        """Start the decorator, patch the db connection and settings dict."""
        from django.db import connections

        self._conn_patch = mock.patch(
            'django.db.connections._connections.default',
            connections[self.template_database])

        self._db_patch = mock.patch(
            'django.db.connections.databases',
            {'default': settings.DATABASES[self.template_database]})

        self._db_patch.start()
        self._conn_patch.start()

    def _reload_template_database(self):
        """Drops and creates the template database."""
        from django.db import connections

        if self.reload_after_test is True:
            connection = connections[self.template_database]
            connection.creation.destroy_test_db(
                connection.settings_dict['ORIGINAL_NAME'], 0)
            connection.settings_dict['NAME'] = connection.settings_dict['ORIGINAL_NAME']
            connection.creation.create_test_db(verbosity=0)

    def _restore_default_database(self):
        """Stop the patches."""
        self._conn_patch.stop()
        self._db_patch.stop()


class TemplateDBTestCase(TemplateDBMixin, TestCase):

    """TestCase with TemplateDB support."""

    def _pre_setup(self):
        """Switch to the template database before each test case."""
        self._use_template_database()
        super(TemplateDBTestCase, self)._pre_setup()

    def _post_teardown(self):
        """Restore the default database after each test case."""
        super(TemplateDBTestCase, self)._post_teardown()
        self._restore_default_database()


class TemplateDBTransactionTestCase(TemplateDBMixin, TransactionTestCase):
    
    """TransactionTestCase with TemplateDB support."""

    def _pre_setup(self):
        """Switch to the template database before each test case."""
        self._use_template_database()
        with mock.patch('django.core.management.commands.flush.Command'):
            super(TemplateDBTransactionTestCase, self)._pre_setup()

    def _post_teardown(self):
        """Restore the default database after each test case."""
        with mock.patch('django.core.management.commands.flush.Command'):
            super(TemplateDBTransactionTestCase, self)._post_teardown()
        self._restore_default_database()
        self._reload_template_database()


class TemplateDBLiveServerTestCase(TemplateDBMixin, LiveServerTestCase):

    """LiveServerTestCase with TemplateDB support."""

    _use_template_database = classmethod(TemplateDBMixin._use_template_database.__func__)
    _restore_default_database = classmethod(TemplateDBMixin._restore_default_database.__func__)
    _reload_template_database = classmethod(TemplateDBMixin._reload_template_database.__func__)

    @classmethod
    def setUpClass(cls):
        """Switch to the template database before the LiveServer is started."""
        cls._use_template_database()
        super(TemplateDBLiveServerTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """Restore the defaut database after the LiveServer is stopped."""
        super(TemplateDBLiveServerTestCase, cls).tearDownClass()
        cls._restore_default_database()
        cls._reload_template_database()

    def _pre_setup(self):
        """Switch to the template database before each test case."""
        with mock.patch('django.core.management.commands.flush.Command'):
            super(TemplateDBLiveServerTestCase, self)._pre_setup()

    def _post_teardown(self):
        """Restore the default database after each test case."""
        with mock.patch('django.core.management.commands.flush.Command'):
            super(TemplateDBLiveServerTestCase, self)._post_teardown()
