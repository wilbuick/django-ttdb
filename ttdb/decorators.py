"""Decorator to change the database the tests are run with."""

from django.test import LiveServerTestCase
from django.test import TestCase
from django.test import TransactionTestCase
import functools
from ttdb.testcases import TemplateDBTestCase 
from ttdb.testcases import TemplateDBLiveServerTestCase
from ttdb.testcases import TemplateDBTransactionTestCase
from ttdb.utils import reload_template_database
from ttdb.utils import restore_default_database
from ttdb.utils import enable_template_database  


class use_template_database(object):

    """Decorator that switches the test database to another."""

    def __init__(self, db_name, reload_after_test=True):
        """Set args for the decorator."""
        self.template_database = db_name
        self.reload_after_test = reload_after_test

    def __enter__(self):
        """For using in with statement."""
        self._templatedb_patches = enable_template_database(self.template_database)

    def __exit__(self, exc_type, exc_value, traceback):
        """For using in with statement."""
        restore_default_database(*self._templatedb_patches)
        if self.reload_after_test is True:
            reload_template_database(self.template_database)

    def __call__(self, test_func):
        """Switch the test database to the one specified.
        
        If decorating a test class, override the setUp methods to switch the 
        database. If decorating a test function, wrap the function in another
        and use the with statement to switch the database.
        
        """
        if isinstance(test_func, type) and issubclass(test_func, TransactionTestCase):
            test_func.template_database = self.template_database
            test_func.reload_after_test = self.reload_after_test

            if issubclass(test_func, TestCase):
                test_func.__bases__ = (TemplateDBTestCase,) + test_func.__bases__
            elif issubclass(test_func, LiveServerTestCase):
                test_func.__bases__ = (TemplateDBLiveServerTestCase,) + test_func.__bases__
            elif issubclass(test_func, TransactionTestCase):
                test_func.__bases__ = (TemplateDBTransactionTestCase,) + test_func.__bases__
            return test_func

        # If wrapping an individual test case use the with statement to apply
        # the patch.
        @functools.wraps(test_func)
        def inner(*args, **kwargs):
            with self:
                return test_func(*args, **kwargs)
        return inner 
