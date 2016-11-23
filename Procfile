release: python iitgurp/manage.py migrate
web: gunicorn --pythonpath iitgurp iitgurp.wsgi:application --log-file -
