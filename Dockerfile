FROM python:2.7

RUN apt-get update -y && apt-get install -y vim less git net-tools curl apache2 libapache2-mod-wsgi
RUN pip install --upgrade pip
run a2enmod rewrite ssl
RUN pip install pycrypto mongoengine python-memcached webapp2 webob pyyaml twython
RUN mkdir -p /var/www
COPY ./server_config/website.conf /etc/apache2/sites-enabled
COPY ./server_config/apache2.conf /etc/apache2/

COPY . /var/www/
