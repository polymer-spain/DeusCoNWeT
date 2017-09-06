FROM mgood/appengine-python

RUN apt-get update -y && apt-get install -y vim less git stunnel4 net-tools curl
RUN mkdir /app
COPY ./server_config/stunnel4 /etc/default/ 
COPY ./server_config/stunnel.* /etc/stunnel/
