FROM ubuntu
RUN apt-get -y  update  --fix-missing
RUN apt-get  install  -y python2.7 python-pip python-dev  build-essential
# Install Nginx
RUN apt-get install -y  nginx
# Copy requirements
COPY ./requirements.txt /root/app/
# Install requirements
WORKDIR /root/app/
RUN pip install -r requirements.txt
# Copy all other stuff
COPY ./ /root/app/
WORKDIR /root/app/

# Enable the new webservice to server using nginx
RUN cp nginx_app_block /etc/nginx/sites-available/
RUN rm /etc/nginx/sites-available/default
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/nginx_app_block /etc/nginx/sites-enabled/

RUN chmod +x ./start.sh
CMD ["./start.sh"]
