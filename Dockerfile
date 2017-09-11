FROM mgood/appengine-python

RUN apt-get update -y && apt-get install -y vim less git stunnel4 net-tools curl
RUN mkdir -p /var/www
RUN pip install pycrypto mongoengine
COPY . /var/www/
COPY ./server_config/stunnel4 /etc/default/ 
COPY ./server_config/stunnel.* /etc/stunnel/
