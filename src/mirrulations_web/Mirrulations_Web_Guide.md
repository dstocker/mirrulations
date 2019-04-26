#Mirrulations Web
This is the documentation for usage of the mirrulations_web module in mirrulations. This module contains the code for the mirrulations website front and back end.

##Connecting to the AWS server
Using the key for the AWS server, ssh into it using:
~~~~ 
ssh -i /path/to/mirrulations_web.pem ubuntu@ip.of.aws.server
~~~~


##Starting Mirrulations_Web as a service 
Go to /lib/systemd/system/ and create a .service that contains:
~~~
[Unit]
Description=Start Mirrulations on Boot
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/local/bin/gunicorn -b 0.0.0.0:80 --chdir /home/ubuntu/mirrulatio$

[Install]
WantedBy=multi-user.target
~~~
Once that is done run the following commands and your service will be up an running:
~~~
sudo chmod 644 /lib/systemd/system/service_name.service
sudo systemctl daemon-reload
sudo systemctl enable service_name.service
sudo reboot
~~~


##Updating The Web Server
We created a bash script using systemd that when ran stops the server, pulls the changes, and then restarts the web server. If you want to recreate this script create a .sh in the mirrulations repo and add:
~~~
#!/bin/bash
sudo systemctl stop service_name
git pull origin master
sudo systemctl start service_name
~~~
    
