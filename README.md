# TL;DR
TL;DR : Seafile deployment by using Ansible automation tool.

## Description
This is a small project chosen to teach me how to use ansible by deploying the "Open Source File Sync and Share Software" Seafile.
The deployment is using Ansible's modules as possible. For some tasks, I didn't find a way other than using the module "raw" to send "dirty" SSH commands.

## How to use
There are some important prerequisites before using it.

**1.** The "nodemanager" here is a PopOS 21.04 (Ubuntu-based), with two deployment nodes which are running on Debian 10 codename Buster : "seafile1" & "seafile2".

**2.** On the nodemanager, you will need "SSH", "sshpass", "python3-virtualenv", "default-libmysqlclient-dev" packages. I also created a user "user-ansible" on it for all ansible-related activities (see the step 6). On the deployment nodes, add the "sudo" and "SSH" packages.

**3.** Then, I created a virtualenv "$ virtualenv ansible", activated it by doing <pre>$ source ansible/bin/activate</pre> and finally, installed ansible inside : <pre>$ pip install ansible</pre>

**4.** After that, still on the nodemanager, add the deployment nodes in the file "# nano /etc/hosts" because I didn't have any local DNS server.
<pre>192.168.77.1  seafile1
192.168.77.2  seafile2</pre>

**5.** Activate root login via SSH for "seafile1" and "seafile2" nodes, restart the service then accept their keys : "$ ssh root@seafile1" & "$ ssh root@seafile2".

**6.** By using ansible's module "debug", hash a password for the future "user-ansible" that we'll create on "seafile1" and "seafile2" nodes.
<pre>$ ansible localhost -i inventaire.ini -m debug -a "msg={{ 'seafilepwd' | password_hash('sha512', 'sceretsalt') }}"
localhost | SUCCESS => {
  "msg": "$6$sceretsalt$Qo75g/53vx5LUFXNQ2ke7Ng70pwLMCNOz8ogsn4P79MHAyquRNO6VrN/8ZG9z57VFwZi/1AbJnp5oLTKvEiD41"
}</pre>
          
For both commands below (6a & 6b), we specify the password of the root user because the "user-ansible" isn't created yet. Later we'll be using the user "user-ansible" and its password.

**6a.** Creating the user "user-ansible" with our hashed password.
<pre>$ ansible -i inventaire.ini -m user -a 'name=user-ansible password=$6$sceretsalt$Qo75g/53vx5LUFXNQ2ke7Ng70pwLMCNOz8ogsn4P79MHAyquRNO6VrN/8ZG9z57VFwZi/1AbJnp5oLTKvEiD41 shell=/bin/bash' --user root --ask-pass all
  SSH password: ("route" because we are executing it as "root")</pre>

**6b.** Adding the user "user-ansible" in the sudo group.
<pre>$ ansible -i inventaire.ini -m user -a 'name=user-ansible groups=sudo append=yes ' --user root --ask-pass all
  SSH password: ("route" because we are executing it as "root")</pre>

Now, the user "user-ansible" is created and in the sudo group. We can now use it in our following commands, or by executing again the previous one to test it.

**7.** Testing our freshly created user by executing the same command again BUT as user "user-ansible".
<pre>$ ansible -i inventaire.ini -m user -a 'name=user-ansible groups=sudo append=yes ' --user user-ansible --ask-pass --become --ask-become-pass all
  SSH password: ("seafilepwd" because the user is now "user-ansible")
  SUDO password[defaults to SSH password]: ("seafilepwd")

seafile2 | SUCCESS => {
  "append": true,
  "changed": false,
  "comment": "",
  "group": 1001,
  "groups": "sudo",
  "home": "/home/user-ansible",
  "move_home": false,
  "name": "user-ansible",
  "shell": "/bin/bash",
  "state": "present",
  "uid": 1001
}
seafile1 | SUCCESS => {
  "append": true,
  "changed": false,
  "comment": "",
  "group": 1001,
  "groups": "sudo",
  "home": "/home/user-ansible",
  "move_home": false,
  "name": "user-ansible",
  "shell": "/bin/bash",
  "state": "present",
  "uid": 1001
}</pre>

**8.** Still on the nodemanager, generate ECDSA SSH keys : <pre>$ ssh-keygen -t ecdsa</pre> and by using the module 'authorized_key', send them to the nodes :
<pre>$ ansible -i inventaire.ini -m authorized_key -a 'user=user-ansible state=present key="{{ lookup("file", "/home/user-ansible/.ssh/id_ecdsa.pub") }}"' --user user-ansible --ask-pass --become --ask-become-pass all
seafile2 | SUCCESS => {
  "changed": false,
  "comment": null,
  "exclusive": false,
  "follow": false,
  "key": "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAI= user-ansible@nodemanager",
  "key_options": null,
  "keyfile": "/home/user-ansible/.ssh/authorized_keys",
  "manage_dir": true,
  "path": null,
  "state": "present",
  "unique": false,
  "user": "user-ansible",
  "validate_certs": true
}
seafile1 | SUCCESS => {
  "changed": false,
  "comment": null,
  "exclusive": false,
  "follow": false,
  "key": "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAA= user-ansible@nodemanager",
  "key_options": null,
  "keyfile": "/home/user-ansible/.ssh/authorized_keys",
  "manage_dir": true,
  "path": null,
  "state": "present",
  "unique": false,
  "user": "user-ansible",
  "validate_certs": true
}</pre>

**9.** Change your user while on the nodemanager with <pre>su - user-ansible</pre> then <pre>source ansible/bin/activate</pre> and make sure that you have the MySQLdb python library installed in your ansible virtual-env by doing <pre>(ansible) user-ansible@nodemanager:~$ pip3 list</pre> If it's not listed, you must install it with this command (or you will likely have some error while executing my seafile_adduser module) :
<pre>(ansible) user-ansible@nodemanager:~$ pip3 install mysqlclient</pre> 

Now you should be able to clone this repository.

**10.** Clone the repository into your user-ansible's home folder, and check a second time that you are in your ansible's virtual environment.
<pre>(ansible) user-ansible@nodemanager:~$</pre>

You should be able to see the the repository's folders and files with the "ls" command.

**11.** If your deployment nodes are not named exactly like mine, you must edit the "inventaire.ini" file which contains their hostnames.
Same thing for the file "configuration.ini" because they are specified at the start of this file.

**12.** Execute the "configuration.yml" file with the following command to have Seafile installed : 
<pre>$ ansible-playbook -i inventaire.ini --user user-ansible --become --ask-become-pass configuration.yml -e 'ansible_python_interpreter=/usr/bin/python3' --ask-vault-pass"
BECOME password : ("seafilepwd")
Vault password : ("route")</pre>

And if everything is okay, it will start to execute each task in order to prepare the seafile installation and configuration.

Information : The password for the post-install user "com@test.fr" will be "route". If you want to change it, I'm providing a python file that will hash the wanted password. It's stored in "~./library/password_seafile.py"and you'll only need to edit the file and change the value of the 'password' variable.

## What is the script doing ?
The script is :
- installing the required apt packages (1st),
- installing the required pip packages (2st),
- installing the last required apt packages (3st),
- deleting and creating the user "seafile",
- enabling and starting mariadb & nginx services,
- installing the package "python-mysql" for debian,
- mimicking the behaviour of the "mysql_secure_installation" command by doing the same actions,
- creating the needed databases for seafile (ccnet-db, seafile-db, seahub-db),
- creating the "seafile" user on mysql,
- downloading and unpacking the "seafile-server.tar.gz" archive,
- copying modified versions of seafile installation script (setup-seafile-mysql.py, setup-seafile-mysql.sh) and executing them,
- creating /opt/* folders for seafile,
- modifying permissions for the /opt folders and files,
- copying a modified version of the "seahub.sh" starting script + the "check_init_admin.py" script (to create the default admin user),
- copying a modified "seafile.conf" file, in order to replace the SERVER NAME variable with the actual server's ip address,
- restarting the nginx service,
- adding a post-install user (com@test.fr) using the custom module (seafile_adduser).
