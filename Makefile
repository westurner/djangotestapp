
default: test

test:
	python ./manage.py test -d

coverage:
	@# pip install coverage
	coverage run --source='.' manage.py test
	coverage report -m

serve:
	python ./manage.py runserver_plus

install:
	pip install -r requirements/requirements-all.txt

setupdev:
	python ./manage.py check
	python ./manage.py createsuperuser --noinput --username=admin --email=admin@local.local
	@# python ./manage.py changepassword admin
	@# django-extensions
	python ./manage.py set_fake_passwords
	#python ./manage.py set_default_site --system-fqdn
	$(MAKE) migrate
	#python ./manage.py generate_secret_key

collectstatic:
	python ./manage.py collectstatic --no-input  # STATIC_ROOT

migrate:
	python ./manage.py migrate -v3

dumpdata:
	python ./manage.py dumpdata --all \
		| python -mjson.tool > djangotestapp/fixtures/dump.json

rebuild_index:
	python ./manage.py rebuild_index --noinput


elasticsearch-serve:
	./bin/elasticsearch -Dpath.data="${_VAR}/es/data" -Dpath.logs="${_LOG}/es"	



composeps:
	docker-compose ps

composeup:
	docker-compose up -d
	docker-compose ps

composedown:
	docker-compose down
	docker-compose ps

composebuild:
	docker-compose build app

composebuild-no-cache:
	docker-compose build --no-cache app
