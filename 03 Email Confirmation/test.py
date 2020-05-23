# Interacting with SQLite

import sqlite3


connection = sqlite3.connect('dbsqlite3.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

# user = (1, 'ashish', 'admin')
insert_user = "INSERT INTO users VALUES (?, ?, ?)"
# cursor.execute(insert_user, user)

users = [
    (1, 'ashish', 'admin'),
    (2, 'user1', 'admin'),
    (3, 'user2', 'admin'),
    (4, 'user3', 'admin')
]
cursor.executemany(insert_user, users)

select_user = "SELECT * FROM users"
for row in cursor.execute(select_user):
    print(row)

connection.commit()
connection.close()
