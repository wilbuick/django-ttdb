"""Test cases that switch the default test database to a different db."""

from django.conf import settings
from django.test import TestCase
from django.test import TransactionTestCase
from django.test import LiveServerTestCase
from django.core.management import call_command
import mock
from ttdb.utils import reload_template_database
from ttdb.utils import restore_default_database
from ttdb.utils import enable_template_database 


class TemplateDBTestCase(TestCase):

    """TestCase with TemplateDB support."""

    reload_after_test = False

    def _pre_setup(self):
        """Switch to the template database before each test case."""
        self._templatedb_patches = enable_template_database(self.template_database)
        super(TemplateDBTestCase, self)._pre_setup()

    def _post_teardown(self):
        """Restore the default database after each test case."""
        super(TemplateDBTestCase, self)._post_teardown()
        restore_default_database(*self._templatedb_patches)
        if self.reload_after_test is True:
            reload_template_database(self.template_database)


class TemplateDBTransactionTestCase(TransactionTestCase):
    
    """TransactionTestCase with TemplateDB support."""

    reload_after_test = True

    def _pre_setup(self):
        """Switch to the template database before each test case."""
        self._templatedb_patches = enable_template_database(self.template_database)
        with mock.patch('django.core.management.commands.flush.Command'):
            super(TemplateDBTransactionTestCase, self)._pre_setup()

    def _post_teardown(self):
        """Restore the default database after each test case."""
        with mock.patch('django.core.management.commands.flush.Command'):
            super(TemplateDBTransactionTestCase, self)._post_teardown()
        restore_default_database(*self._templatedb_patches)
        if self.reload_after_test is True:
            reload_template_database(self.template_database)


class TemplateDBLiveServerTestCase(LiveServerTestCase):

    """LiveServerTestCase with TemplateDB support."""

    reload_after_test = True

    @classmethod
    def setUpClass(cls):
        """Switch to the template database before the LiveServer is started."""
        cls._templatedb_patches = enable_template_database(cls.template_database)
        super(TemplateDBLiveServerTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """Restore the defaut database after the LiveServer is stopped."""
        super(TemplateDBLiveServerTestCase, cls).tearDownClass()
        restore_default_database(*cls._templatedb_patches)
        if cls.reload_after_test is True:
            reload_template_database(cls.template_database)

    def _pre_setup(self):
        """Switch to the template database before each test case."""
        with mock.patch('django.core.management.commands.flush.Command'):
            super(TemplateDBLiveServerTestCase, self)._pre_setup()

    def _post_teardown(self):
        """Restore the default database after each test case."""
        with mock.patch('django.core.management.commands.flush.Command'):
            super(TemplateDBLiveServerTestCase, self)._post_teardown()
