
default: test

test:
	python ./manage.py test

coverage:
	@# pip install coverage
	coverage run --source='.' manage.py test
	coverage report -m

serve:
	python ./manage.py runserver_plus

install:
	pip install -r requirements/requirements-all.txt
