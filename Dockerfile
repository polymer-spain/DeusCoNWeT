FROM httpd:2.4

RUN apt-get update -y && apt-get install -y vim less git net-tools curl python-pip python-dev build-essential
RUN pip install --upgrade pip

RUN pip install pycrypto mongoengine python-memcached
RUN mkdir -p /var/www
COPY ./server_config/website.conf /etc/apache2/sites-enabled
COPY ./server_config/apache2.conf /etc/apache2/

COPY . /var/www/
