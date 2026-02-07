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

format: ## Sorts the imports and reformats the code
	# sort imports / remove unused
	ruff check --fix --select I
	ruff check --fix
	# reformat
	ruff format

dist:
	uv build

upload:dist
	twine upload dist/* --skip-existing

update-translations:
	pybabel extract -F babel.cfg -k lazy_gettext -o portal/translations/messages.pot .
	pybabel update -i portal/translations/messages.pot -d portal/translations/

add-translation:
	@read -p "Enter new language shortcode:" lang; \
	pybabel init -i portal/translations/messages.pot -d portal/translations/ -l $$lang

compile-translations:
	pybabel compile -d portal/translations/
