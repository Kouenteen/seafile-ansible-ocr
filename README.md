# TL;DR
TL;DR : Seafile deployment by using Ansible automation tool.

## Description
This is a small project chosen to teach me how to use ansible by deploying the "Open Source File Sync and Share Software" Seafile.
The deployment is using Ansible's modules as possible. For some tasks, I didn't find a way other than using the module "raw" to send "dirty" SSH commands.

## How to use
There are some important prerequisites before using it.

1. The "nodemanager" here is a PopOS 21.04 (Ubuntu-based), with two deployment nodes which are running on Debian 10 codename Buster : "seafile1" & "seafile2".
2. On the nodemanager, you will need "SSH", "sshpass", "python3-virtualenv" packages. I also created a user "user-ansible" on it for all ansible-related activities. On the deployment nodes, add the "sudo" and "SSH" packages. 
3. Then, I created a virtualenv "$ virtualenv ansible", activated it by doing "$ source ansible/bin/activate" and finally, installed ansible inside : "$ pip install ansible".
4. After that, still on the nodemanager, add the deployment nodes in the file "# nano /etc/hosts" because I didn't have any local DNS server.
5. Activate root login via SSH for "seafile1" and "seafile2" nodes, restart the service then accept their keys : "$ ssh root@seafile1" & "$ ssh root@seafile2".
6. By using ansible's module "debug", hash a password for the future "user-ansible" that we'll create on "seafile1" and "seafile2" nodes.
7. Create the user "user-ansible" via ansible with your precedently hashed password, and add him into the "sudo" group. It should return : 
<pre>$ ansible -i inventaire.ini -m user -a 'name=user-ansible groups=sudo append=yes ' --user user-ansible --ask-pass --become --ask-become-pass all
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

8. Still on the nodemanager, generate ECDSA SSH keys : '$ ssh-keygen -t ecdsa' and by using the module 'authorized_key', send them to the nodes :
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

9. Change your user while on the nodemanager with "su - user-ansible" then "source ansible/bin/activate" and you should be ready to clone this repository.
<pre>Add the steps for cloning and start using it</pre>
