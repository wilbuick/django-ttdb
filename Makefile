.PHONY: flake8 test coverage

flake8:
	flake8 ttdb tests

test:
	DJANGO_SETTINGS_MODULE=tests.settings tests/manage.py test core

coverage:
	coverage erase
	DJANGO_SETTINGS_MODULE=tests.settings \
	    coverage run tests/manage.py test core
	coverage html
