from __future__ import absolute_import

import mock
import threading
import unittest

from django.test import TestCase
from django.test import TransactionTestCase
from django.test import LiveServerTestCase
from django.test.utils import override_settings
from django.db.backends.postgresql_psycopg2.base import DatabaseWrapper as PostgresqlDatabaseWrapper
from django.db.backends.sqlite3.base import DatabaseWrapper as SqliteDatabaseWrapper
from django.conf import settings

from ttdb.runner import TemplateDatabaseRunner
from ttdb import TemplateDBTestCase
from ttdb import TemplateDBTransactionTestCase
from ttdb import TemplateDBLiveServerTestCase
from ttdb import use_template_database

from .models import Test as TestModel


class TestMethodDecorator(TestCase):

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

        # Check that the database name is pointing to the test database.
        self.assertEqual(connections['default'].settings_dict['NAME'], 'test_django_ttdb')


class TestWithStatement(TestCase):

    """Test with statement."""

    def test_with_statement(self):
        """Test decorator works as with statement."""
        from django.db import connections

        # Assert default database connection object is unmodified.
        self.assertIsInstance(connections['default'], SqliteDatabaseWrapper)

        with use_template_database('development', reload_after_test=False):
            # Checl the database connection object is using the postgresql
            # adapter.
            self.assertIsInstance(connections['default'],
                                  PostgresqlDatabaseWrapper)

            # Make sure the test template database has data loaded without
            # fixtures.
            self.assertEqual(TestModel.objects.count(), 4)

        # Check the database connection object is returned to normal.
        self.assertIsInstance(connections['default'], SqliteDatabaseWrapper)


class TestReloadTemplateDatabase(TestCase):

    """Test reloading template test database."""

    @mock.patch('django.db.backends.creation.BaseDatabaseCreation._destroy_test_db')
    @mock.patch('django.db.backends.creation.BaseDatabaseCreation._create_test_db')
    def test_reload_database(self, _destroy_test_db, _create_test_db):
        """Test reload of test database."""
        with use_template_database('development'):
            pass
        self.assertEqual(_destroy_test_db.call_count, 1)
        self.assertEqual(_create_test_db.call_count, 1)

    @mock.patch('django.db.backends.creation.BaseDatabaseCreation._destroy_test_db')
    @mock.patch('django.db.backends.creation.BaseDatabaseCreation._create_test_db')
    def test_reload_database(self, _destroy_test_db, _create_test_db):
        """Test skip reload of test database."""
        with use_template_database('development', reload_after_test=False):
            pass
        self.assertEqual(_destroy_test_db.call_count, 0)
        self.assertEqual(_create_test_db.call_count, 0) 


@use_template_database('development')
class TestTestCaseDecorator(TestCase):

    """."""

    def test_class_bases(self):
        """."""
        self.assertIn(TemplateDBTestCase, TestTestCaseDecorator.__bases__)

    def test_correct_db(self):
        """."""
        from django.db import connections

        # Check the database connection is correctly patched
        self.assertIsInstance(connections['default'], PostgresqlDatabaseWrapper)

        # Check the template test database contains data.
        self.assertEqual(TestModel.objects.count(), 4)

        # Check that the database name is pointing to the test database.
        self.assertEqual(connections['default'].settings_dict['NAME'], 'test_django_ttdb')


@use_template_database('development')
class TestTransactionTestCaseDecorator(TransactionTestCase):

    """."""

    def test_class_bases(self):
        """."""
        self.assertIn(TemplateDBTransactionTestCase, TestTransactionTestCaseDecorator.__bases__)

    def test_correct_db(self):
        """."""
        from django.db import connections

        # Check the database connection is correctly patched
        self.assertIsInstance(connections['default'], PostgresqlDatabaseWrapper)

        # Check the template test database contains data.
        self.assertEqual(TestModel.objects.count(), 4)

        # Check that the database name is pointing to the test database.
        self.assertEqual(connections['default'].settings_dict['NAME'], 'test_django_ttdb')


@use_template_database('development')
class TestLiveServerTestCaseDecorator(LiveServerTestCase):

    """."""

    def test_class_bases(self):
        """."""
        self.assertIn(TemplateDBLiveServerTestCase, TestLiveServerTestCaseDecorator.__bases__)

    def test_correct_db(self):
        """."""
        from django.db import connections

        # Check the database connection is correctly patched
        self.assertIsInstance(connections['default'], PostgresqlDatabaseWrapper)

        # Check the template test database contains data.
        self.assertEqual(TestModel.objects.count(), 4)

        # Check that the database name is pointing to the test database.
        self.assertEqual(connections['default'].settings_dict['NAME'], 'test_django_ttdb')

    def test_correct_db_thread(self):
        """Test the correct db inside a thread."""
        def test_thread(cls):
            cls.test_correct_db()
            from django.db import connections
            connections['default'].close()

        t = threading.Thread(target=test_thread, args=(self,))
        t.start()
        t.join()
