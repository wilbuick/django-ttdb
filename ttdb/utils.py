"""Helper functions for switching out the default database."""

from django.conf import settings
import mock


def enable_template_database(db_name):
    """Patch the default database db connection and settings dict."""
    from django.db import connections

    connection_patch = mock.patch(
        'django.db.connections._connections.default',
        connections[db_name])

    settings_patch = mock.patch(
        'django.db.connections.databases',
        {'default': settings.DATABASES.get(db_name)})

    connection_patch.start()
    settings_patch.start()

    return connection_patch, settings_patch


def reload_template_database(db_name):
    """Drops and creates the template database."""
    from django.db import connections

    connection = connections[db_name]
    connection.creation.destroy_test_db(
        connection.settings_dict['ORIGINAL_NAME'], 0)
    connection.settings_dict['NAME'] = connection.settings_dict['ORIGINAL_NAME']
    connection.creation.create_test_db(verbosity=0, reload=True)


def restore_default_database(connection_patch, settings_patch):
    """Stop the patches to restore the default database."""
    connection_patch.stop()
    settings_patch.stop()
