.PHONY: clean help test lint isort docs dist upload update-translations compile-translations add-translation

help:
	@echo "  clean                  remove unwanted stuff"
	@echo "  test                   run the testsuite"
	@echo "  docs                   build the documentation"
	@echo "  lint                   check the source for style errors"
	@echo "  isort                  sort the python imports"
	@echo "  dist                   creates distribution packages"
	@echo "  upload                 uploads a new version of the wheel package to PyPI"
	@echo "  update-translations    updates the translations"
	@echo "  compile-translations   compiles the translations"
	@echo "  add-translation        adds a new language to the translations"


clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

test:
	py.test

docs:
	$(MAKE) -C docs html

lint:check-flake8
	flake8

check-flake8:
	@type flake8 >/dev/null 2>&1 || echo "Flake8 is not installed. You can install it with 'pip install flake8'."

isort:check-isort
	isort --order-by-type -rc -up

check-isort:
	@type isort >/dev/null 2>&1 || echo "isort is not installed. You can install it with 'pip install isort'."

dist:
	python setup.py sdist bdist_wheel

upload:dist
	twine upload dist/*

update-translations:
	pybabel extract -F babel.cfg -k lazy_gettext -o portal/translations/messages.pot .
	pybabel update -i portal/translations/messages.pot -d portal/translations/

add-translation:
	@read -p "Enter new language shortcode:" lang; \
	pybabel init -i portal/translations/messages.pot -d portal/translations/ -l $$lang

compile-translations:
	pybabel compile -d portal/translations/
