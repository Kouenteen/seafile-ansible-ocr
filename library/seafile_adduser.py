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
  db_user:
    description: name of the mysql user which will be used to insert the SQL statement
    required: yes
  db_userpwd:
    description: password of the mysql user
    required: yes
'''

EXAMPLES = '''
- name: "Task name"
  seafile_adduser:
    sql: "insert into EmailUser (email, passwd, is_staff, is_active, ctime) VALUES ('sales@test.com', 'hashed_pw', 0, 1, '1631284357945659');
    database: "ccnet-db"
    db_user: "root"
    db_userpwd: "route"
'''

RETURN = '''
results:
    description: Not supposed to have any MySQL related answer because it's an INSERT INTO statement, but if it's a SELECT statement,
    it will return the normal mySQL statement's result.
'''

# Importing library classes
from ansible.module_utils.basic import AnsibleModule
import MySQLdb

# /!\------------------------------------------------------------------------------/!\
# If you want a different default password for the user that will be added, you
# can generate a new hashed password with the python "function" that is given to
# you in the file "password.py". After that change the existing hashed password in
# the YAML file that contains the sql statement

# Arguments definition (main function)
def main():
    module = AnsibleModule(
        argument_spec=dict(
            sql        = dict(required=True, type='str'),
	          database   = dict(required=True, type='str'),
            db_user    = dict(required=True, type='str'),
            db_userpwd = dict(required=True, type='str'),
        )
    )

    # Arguments values
    sql_local        = module.params.get("sql")
    database_local   = module.params.get("database")
    db_user_local    = module.params.get("db_user")
    db_userpwd_local = module.params.get("db_userpwd")

    # Database connection
    db = MySQLdb.connect("localhost", db_user_local, db_userpwd_local, database_local)
    cur = db.cursor()
    cur.execute(sql_local)

    # Executing the SQL statement
    db.commit()

    # Retrieving the results
    resultat = cur.fetchall()
    db.close()

    # Returning the results to Ansible
    module.exit_json(changed=False, results=resultat)

# Function execution
if __name__ == "__main__":
    main()
