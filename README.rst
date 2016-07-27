

djangotestapp
===============

| Src: https://github.com/westurner/djangotestapp


.. contents::
   :depth: 10

Usage
-------

.. code:: bash

   git clone ssh://git@github.com/westurner/djangotestapp
   cd djangotestapp
   make install test
   make setupdev migrate serve
   # username/password: admin/password

-  http://localhost:8000/
-  http://localhost:8000/_admin_/


Apps
-----

testapp
~~~~~~~~
| Src: https://github.com/westurner/djangotestapp/tree/develop/djangotestapp/testapp

- Message model
- #hashtag and @usertag support:
  https://github.com/westurner/djangotestapp/blob/develop/djangotestapp/testapp/utils.py


Framework
-----------

Django
~~~~~~~
| Homepage: https://www.djangoproject.com/
| Src: https://github.com/django/django
| PyPI: https://pypi.python.org/pypi/django
| Docs: https://docs.djangoproject.com/en/1.9/

API
-----

django-rest-framework
~~~~~~~~~~~~~~~~~~~~~~~
| Src: https://github.com/tomchristie/django-rest-framework
| Docs: http://www.django-rest-framework.org/
| PyPI: https://pypi.python.org/pypi/djangorestframework


auth
------

django-rest-framework-social-oauth2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
| Src: https://github.com/PhilipGarnero/django-rest-framework-social-oauth2
| PyPI: https://pypi.python.org/pypi/django-rest-framework-social-oauth2

- `python-social-auth`_
- `django-oauth-toolkit`_

python-social-auth
~~~~~~~~~~~~~~~~~~~~~~
| Src: https://github.com/omab/python-social-auth
| Docs: http://psa.matiasaguirre.net/docs/
| PyPI: https://pypi.python.org/pypi/python-social-auth

- Third-party authentication

django-oauth-toolkit
~~~~~~~~~~~~~~~~~~~~~~
| Src: https://github.com/evonove/django-oauth-toolkit
| Docs: https://django-oauth-toolkit.readthedocs.io/en/latest/
| Docs: https://django-oauth-toolkit.readthedocs.io/en/latest/rest-framework/rest-framework.html
| PyPI: https://pypi.python.org/pypi/django-oauth-toolkit

- OAuth2

curlish
~~~~~~~~~
| Src: https://github.com/fireteam/curlish
| Docs: https://pythonhosted.org/curlish/
| PyPI: https://pypi.python.org/pypi/curlish

- Curl + OAuth2


``~/.ftcurlish.json``:

.. code:: json

    {
      "curl_path": "curl",
      "http_port": 62231,
      "json_indent": 2,
      "sites": {
        "dt": {
          "extra_headers": {},
          "request_token_params": {},
          "authorize_url": "http://localhost:8000/auth/token",
          "base_url": "http://localhost:8000/",
          "client_id": "4nDF3xY0z8kUdLGxj4hiSMIbRWo9WqTiidC9oTKM",
          "client_secret": "ufywDcTi8dNit8gfVfk0zaxy2SUj0gY3i0NNx37X6ZzGQqp6NOUxGCWz5ACIoM9HUsxyxsLbsiPezE0VqpotoYwfSDcRPlfnamq3nT2q27JUZiSgRCLtdDAC1XbS0LDN",
          "grant_type": "password",
          "access_token_url": "/auth/token"
        }
      }
    }

- Get ``client_id``, ``client_secret`` from:
  http://localhost:8000/admin/oauth2_provider/application/add/


Datastore
-----------

MySQL
~~~~~~
| Wikipedia: https://en.wikipedia.org/wiki/MySQL
| Homepage: https://www.mysql.com/
| Src: https://github.com/mysql/mysql-server
| Docs: https://dev.mysql.com/doc/

Memcached
~~~~~~~~~~~
| Wikipedia: https://en.wikipedia.org/wiki/Memcached
| Homepage: http://memcached.org/
| Src: https://github.com/memcached/memcached
| Docs: https://github.com/memcached/memcached/wiki


Tasks
-------

RabbitMQ
~~~~~~~~~~
| Wikipedia: https://en.wikipedia.org/wiki/RabbitMQ
| Homepage: https://www.rabbitmq.com/
| Src: https://github.com/rabbitmq/rabbitmq-server
| Docker: https://hub.docker.com/_/rabbitmq/
| Docs: https://www.rabbitmq.com/documentation.html
| Docs: https://www.rabbitmq.com/networking.html

- AMQP Message Queue


Celery
~~~~~~~
| Wikipedia: `<https://en.wikipedia.org/wiki/Celery_(software)>`__
| Homepage: http://www.celeryproject.org/
| Src: https://github.com/celery/celery
| PyPI: https://pypi.python.org/pypi/celery
| Docs: http://docs.celeryproject.org/en/latest/
| Docs: http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html

- Asynchronous task queue
- Worker message protocol
- `rabbitmq`_


Search
--------

Elasticsearch
~~~~~~~~~~~~~~~~
| Wikipedia: https://en.wikipedia.org/wiki/Elasticsearch
| Homepage: https://www.elastic.co/
| Src: https://github.com/elastic/elasticsearch
| Docker: https://hub.docker.com/_/elasticsearch/
| Docs: https://www.elastic.co/guide/en/elasticsearch/guide/current/
| Docs: https://www.elastic.co/guide/en/elasticsearch/reference/current/
| Docs: https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-configuration.html

- RESTful JSON search
- https://www.elastic.co/guide/en/elasticsearch/guide/current/fuzziness.html


django-haystack
~~~~~~~~~~~~~~~~~
| Homepage: http://haystacksearch.org/
| Src: https://github.com/django-haystack/django-haystack
| PyPI: https://pypi.python.org/pypi/django-haystack
| Docs: https://django-haystack.readthedocs.io/en/latest/

- `django`_ + [`elasticsearch`_,]


celery-haystack
~~~~~~~~~~~~~~~~~
| Src: https://github.com/django-haystack/celery-haystack
| PyPI: https://pypi.python.org/pypi/celery-haystack
| Docs: https://celery-haystack.readthedocs.io/en/latest/

- `celery`_ + `django-haystack`_
- Realtime index synchronization


drf-haystack
~~~~~~~~~~~~~~~
| Src: https://github.com/inonit/drf-haystack
| PyPI: https://pypi.python.org/pypi/drf-haystack
| Docs: https://drf-haystack.readthedocs.io/en/latest/

- `django-rest-framework`_ + `django-haystack`_
- RESTful search API



Configuration Management
-------------------------

docker-engine
~~~~~~~~~~~~~~
| Wikipedia: `<https://en.wikipedia.org/wiki/Docker_(software)>`__|
| Homepage: https://www.docker.com/
| Src: https://github.com/docker/docker
| Docs: https://docs.docker.com/
| Docs: https://docs.docker.com/engine/

- Linux Containers
- CLI


docker-compose
~~~~~~~~~~~~~~~~
| Src: https://github.com/docker/compose
| PyPI: https://pypi.python.org/pypi/docker-compose
| Docs: https://docs.docker.com/compose/
| Docs: https://docs.docker.com/compose/compose-file/

- Declarative `Docker`_ config: ``docker-compose.yml``
- https://github.com/kelseyhightower/compose2kube

.

- https://docs.docker.com/compose/environment-variables/#/the-env-file
- https://docs.docker.com/compose/compose-file/#/variable-substitution

  .. code:: bash

  export _ETC="${VIRTUAL_ENV}/etc"
  export _VAR="${VIRTUAL_ENV}/var"
  export _LOG="${VIRTUAL_ENV}/var/log"

Contributors
--------------
- `@westurner <https://github.com/westurner>`_
