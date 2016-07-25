

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

django
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


Contributors
--------------
- `@westurner <https://github.com/westurner>`_
