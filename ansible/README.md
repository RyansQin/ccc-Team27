
# Ansible Deployment
## Reset password in the Melbourne Research Cloud and COPY it. Also download the OpenStack RC file to the /ansible/nectar
## Firstly, run the run-nectar.sh. It will create the security groups and launch four different instances. 
## Then edit the host.ini file, replace the corrsponding IP address for instances, and specify the right path to the ssh key after the IP address.
## Then run the environment.sh, it will set the environments and install the docker for all instances. 
## Finally run the instance1.sh, instance23.sh and instance4.sh respectively, to deploy the docker containers on each instance and start them. In addition, we didn't set the couchdb cluster in this playbook, as we set the cluster via couchdb cluster wizard(a web GUI) and it's also the prefered way in official documentation. 
