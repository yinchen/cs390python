import sqlite3
conn = sqlite3.connect('picture_share.db')

c = conn.cursor()

# Turn on foreign key support
c.execute("PRAGMA foreign_keys = ON")

# Create users table
c.execute('''CREATE TABLE users
             (email TEXT NOT NULL,
              password TEXT NOT NULL,
              PRIMARY KEY(email))''')

# Create friends table
c.execute('''CREATE TABLE friends
             (email1 TEXT NOT NULL,
              email2 TEXT NOT NULL,
              circle INTEGER NOT NULL)''')

# Create waitlist table
c.execute('''CREATE TABLE waitlist
             (email1 TEXT NOT NULL,
              email2 TEXT NOT NULL)
              ''')


# Create album table
# Visibility is 'public' or 'private'
#c.execute('''CREATE TABLE albums
 #            (name TEXT NOT NULL,
  #            owner TEXT NOT NULL,
   #           visibility TEXT NOT NULL,
    #          FOREIGN KEY (owner) REFERENCES users(email),
     #         PRIMARY KEY(name, owner))''')

# Create post table
c.execute('''CREATE TABLE posts
              (owner TEXT NOT NULL,
              text TEXT NOT NULL,
              circle INTEGER NOT NULL,
              picture_uri TEXT,
              time timestamp NOT NULL,
              FOREIGN KEY(owner) REFERENCES users(email))''')

# Create sessions table
c.execute('''CREATE TABLE sessions
             (user TEXT NOT NULL,
              session TEXT NOT NULL,
              FOREIGN KEY(user) REFERENCES users(email),
              PRIMARY KEY(session))''')


# Save the changes
conn.commit()

# Close the connection
conn.close()
