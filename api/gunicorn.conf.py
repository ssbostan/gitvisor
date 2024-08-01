bind = "0.0.0.0:8000"
wsgi_app = "api:create_app()"
workers = 4
accesslog = "-"
errorlog = "-"