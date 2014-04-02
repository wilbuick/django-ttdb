.PHONY: test

DJANGO_SETTINGS_MODULE := tests.settings

test:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) django-admin.py syncdb --noinput
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) django-admin.py loaddata tests/fixtures/testdata.json
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE) django-admin.py test tests
