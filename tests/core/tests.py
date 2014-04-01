import mock
import unittest

from django.test import TestCase
from django.test import TransactionTestCase
from django.test import LiveServerTestCase
from django.db.backends.postgresql_psycopg2.base import PostgresqlDatabaseWrapper
from django.db.backends.sqlite3.base import SqliteDatabaseWrapper
from django.core.management.base import call_command
from django.conf import settings

from ttdb import TemplateDBTestCase
from ttdb import TransactionDBTransactionTestCase
from ttdb import TransactionDBLiveServerTestCase
from ttdb import use_template_database

from .models import Test as TestModel


class TestDecorator(TestCase):

    """Test decorating a TestCase test class."""

    def test_default_db(self):
        """Test sqlite database is default."""
        from django.db import connections
        self.assertIsInstance(connections['default'], SqliteDatabaseWrapper)

    @use_template_database('development')
    def test_method_decorator(self):
        """Test decorated method."""
        from django.db import connections

        # Check the database connection is correctly patched
        self.assertIsInstance(connections['default'], PostgresqlDatabaseWrapper)

        # Check the template test database contains data.
        self.assertEqual(TestModel.objects.count(), 4)

    def test_with_statement(self):
        """Test decorator works as with statement."""
        from django.db import connections

        # Assert default database connection object is unmodified.
        self.assertIsInstance(connections['default'], SqliteDatabaseWrapper)

        with use_default_database('development', reload_after_test=False):
            # Checl the database connection object is using the postgresql
            # adapter.
            self.assertIsInstance(connections['default'],
                                  PostgresqlDatabaseWrapper)

            # Make sure the test template database has data loaded without
            # fixtures.
            self.assertEqual(TestModel.objects.count(), 4)

        # Check the database connection object is returned to normal.
        self.assertIsInstance(connections['default'], SqliteDatabaseWrapper)

    @mock.patch('django.db.backends.creation.BaseDatabaseCreation._destroy_test_db')
    @mock.patch('django.db.backends.creation.BaseDatabaseCreation._create_test_db')
    def test_reload_database(self, _destroy_test_db, _create_test_db):
        """Test reload of test database."""
        with use_template_database('development'):
            pass
        self.assertEqual(_destroy_test_db.call_count, 1)
        self.assertEqual(_create_test_db.call_count, 1)

        with use_template_database('development', reload_after_test=False):
            pass
        self.assertEqual(_destroy_test_db.call_count, 0)
        self.assertEqual(_create_test_db.call_count, 0) 


class TestRunner(TestCase):

    """Test the test runner."""

    def test_runner(self):
        """."""
        runner = TemplateDatabaseRunner()

        with mock.patch('ttdb.runner.sql_table_creation_suffix') as create_table_suffix:
            runner.setup_databases()
            self.assertTrue(create_table_suffix.call_count == 1)

        with mock.patch('ttdb.runner.create_test_db') as create_test_db:
            runner.setup_databases()
            self.assertTrue(create_test_db.call_count == 1)

    def test_sql_table_creation_suffix(self):
        """Test the table creation suffix is correctly patched."""
        from django.db import connections
        self.assertEqual(connections['development'].creation.sql_table_creation_suffix(),
                         'WITH TEMPLATE %s' % settings.DATABASES['development']['NAME'])


class TestClassDecorator(TestCase):

    """Test the TemplateDBTestCase."""

    def test_decorate_testcase(self):
        """Test decorating TestCase class."""
        @use_template_database('development')
        class DummyTestCase(TestCase):
            def test(self):
                self.assertTrue(True)

        self.assertIn(TemplateDBTestCase, DummyTestCase.__bases__)

        suite = unittest.TestSuite()
        suite.addTests(DummyTestCase())

        _pre_setup = mock.patch('ttdb.testcases.TemplateDBTestCase._pre_setup')
        _post_teardown = mock.patch('ttdb.testcases.TemplateDBTestCase._post_teardown')
        _use_template_database = mock.patch('ttdb.testcases.TemplateDBMixin._use_template_database')
        _reload_template_database = mock.patch('ttdb.testcases.TemplateDBMixin._reload_template_database')
        _restore_default_database = mock.patch('ttdb.testcases.TemplateDBMixin._restore_default_database')

        _pre_setup.start()
        _post_teardown.start()
        _use_template_database.start()
        _reload_template_database.start()
        _restore_default_database.start()

        unititest.TestTestrunner().run(suite())

        self.assertEqual(_pre_setup.call_count, 1)
        self.assertEqual(_post_teardown.call_count, 1)
        self.assertEqual(_use_template_database.call_count, 1)
        self.assertEqual(_reload_template_database.call_count, 0)
        self.assertEqual(_reload_default_database.call_count, 1)

        _pre_setup.stop()
        _post_teardown.stop()
        _use_template_database.stop()
        _reload_template_database.stop()
        _restore_default_database.stop()

    def test_decorate_transactiontestcase(self):
        """Test decorating TransactionTestCase class."""
        @use_template_database('development')
        class DummyTestCase(TransactionTestCase):
            def test(self):
                self.assertTrue(True)

        self.assertIn(TemplateDBTransactionTestCase, DummyTestCase.__bases__)

        _pre_setup = mock.patch('ttdb.testcases.TemplateDBTransactionTestCase._pre_setup')
        _post_teardown = mock.patch('ttdb.testcases.TemplateDBTransactionTestCase._post_teardown')
        _use_template_database = mock.patch('ttdb.testcases.TemplateDBMixin._use_template_database')
        _reload_template_database = mock.patch('ttdb.testcases.TemplateDBMixin._reload_template_database')
        _restore_default_database = mock.patch('ttdb.testcases.TemplateDBMixin._restore_default_database')
        flush = mock.patch('django.core.management.commands.flush.Command')

        _pre_setup.start()
        _post_teardown.start()
        _use_template_database.start()
        _reload_template_database.start()
        _restore_default_database.start()
        flush.start()

        unititest.TestTestrunner().run(suite())

        self.assertEqual(_pre_setup.call_count, 1)
        self.assertEqual(_post_teardown.call_count, 1)
        self.assertEqual(_use_template_database.call_count, 1)
        self.assertEqual(_reload_template_database.call_count, 1)
        self.assertEqual(_reload_default_database.call_count, 1)
        self.assertEqual(flush.call_count, 0)

        _pre_setup.stop()
        _post_teardown.stop()
        _use_template_database.stop()
        _reload_template_database.stop()
        _restore_default_database.stop()
        flush.stop()

    def test_decorate_liveservertestcase(self):
        """Test decorating LiveServerTestCase class."""
        @use_template_database('development')
        class DummyTestCase(LiveServerTestCase):
            def test(self):
                self.assertTrue(True)

        self.assertIn(TemplateDBLiveServerTestCase, DummyTestCase.__bases__) 

        setUpClass = mock.patch('ttdb.testcases.TemplateDBLiveServerTestCase.setUpClass')
        tearDownClass = mock.patch('ttdb.testcases.TemplateDBLiveServer;lTestCase.tearDownClass')
        _use_template_database = mock.patch('ttdb.testcases.TemplateDBMixin._use_template_database')
        _reload_template_database = mock.patch('ttdb.testcases.TemplateDBMixin._reload_template_database')
        _restore_default_database = mock.patch('ttdb.testcases.TemplateDBMixin._restore_default_database')
        flush = mock.patch('django.core.management.commands.flush.Command')

        setUpClass.start()
        tearDownClass.start()
        _use_template_database.start()
        _reload_template_database.start()
        _restore_default_database.start()
        flush.start()

        unititest.TestTestrunner().run(suite())

        self.assertEqual(setUpClass.call_count, 1)
        self.assertEqual(tearDownClass.call_count, 1)
        self.assertEqual(_use_template_database.call_count, 1)
        self.assertEqual(_reload_template_database.call_count, 0)
        self.assertEqual(_reload_default_database.call_count, 1)
        self.assertEqual(flush.call_count, 0)

        setUpClass.stop()
        tearDownClass.stop()
        _use_template_database.stop()
        _reload_template_database.stop()
        _restore_default_database.stop()
        flush.stop()
