#!/usr/bin/python3
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
module: seafile_adduser
author: Kouenteen
description: This module gives you the possibility to add an user after deploying Seafile
options:
  sql:
    description: SQL statement to add the user in the table "EmailUser" of "ccnet-db"
    required: yes
  database:
    description: name of the database
    required: yes
'''

EXAMPLES = '''
- name: "Task name"
  seafile_adduser:
    sql: "insert into EmailUser (email, passwd, is_staff, is_active, ctime) VALUES ('sales@test.com', 'hashed_pw', 0, 1, '1631284357945659');
    database: "ccnet-db"
'''

RETURN = '''
results:
    description: return the sql statement result like "Query OK, 1 row affected (0.001 sec)"
'''

# Importing library classes
from ansible.module_utils.basic import AnsibleModule
import MySQLdb

# If you want a different default password for the user that will be added, you
# can generate a new hashed password with the python "function" that is given to
# you in the file "password.py". After that change the existing hashed password in
# the YAML file that contains the sql statement

# Arguments definition
def main():
    module = AnsibleModule(
        argument_spec=dict(
            sql        = dict(required=True, type='str'),
	    database   = dict(required=True, type='str'),
        )
    )

    # Arguments values
    sql_local        = module.params.get("sql")
    database_local   = module.params.get("database")

    # Database connection
    db = MySQLdb.connect("localhost","root","seafilepwd",database_local)
    cur = db.cursor()
    cur.execute(sql_local)

    db.commit()

    resultat = cur.fetchall()
    db.close()

    # Returning the results to Ansible
    module.exit_json(changed=False, results=resultat)

# Function execution
if __name__ == "__main__":
    main()
