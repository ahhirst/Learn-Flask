# Database connection setup
from binascii import Error
from werkzeug.security import generate_password_hash, check_password_hash

import mysql.connector






def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root@123",
            database="attendance"
        )
        print("Connecting to database...")
        if connection.is_connected():
            print("MySQL se successfully connected!")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        connection = None
def close_db(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection closed.")
    # finally:
        # if connection.is_connected():
            # connection.close()
            # print("MySQL connection close ho gayi.")
# Function to show all tables the table
def all_tables_details():
    
    connection = connect_db()
    if connection:
        try:
            mycursor = connection.cursor()
            # Check how many rows match the condition
            mycursor.execute("SELECT COUNT(*) FROM registration WHERE LENGTH(password) < 15")
            count = mycursor.fetchone()[0]
            print(f"Rows matching condition: {count}")
            
            # Delete rows where the length of the password is less than 15
            mycursor.execute("DELETE FROM registration WHERE LENGTH(password) < 15")
            connection.commit()
            print(f"Deleted rows where password length is less than 15")
        except Error as e:
            print(f"Error deleting rows: {e}")
        # finally:
        #     close_db(connection)
# Call the function to alter the table
all_tables_details()

#for update password of existing password

def update_password(username, new_password):
    try:
        connection=connect_db()
        mycursor = connection.cursor()
        hashed_password = generate_password_hash(new_password)
        print(hashed_password)
        mycursor.execute("UPDATE registration SET password=%s WHERE name=%s", (hashed_password, username))
        connection.commit()
        print(f"Password updated successfully for {username}")
    except Error as e:
        print(f"Error updating password: {e}")
    # finally:
    #     mycursor.close()
    #     close_db(connection)

def one_student(name):
    try:
        connection=connect_db()
        mycursor = connection.cursor()
        mycursor.execute("SELECT * FROM registration WHERE name=%s", (name,))
        s = mycursor.fetchone()
        return list(s) if s else None
    except Error as e:
        print(f"Error fetching student: {e}")
        return None
    # finally:
    #     mycursor.close()
    #     close_db(connection)

def all_student():
    try:
        connection=connect_db()
        mycursor = connection.cursor()
        mycursor.execute("SELECT * FROM registration ORDER BY name DESC")
        all_student_data = mycursor.fetchall()
        mycursor.execute("SHOW COLUMNS FROM registration")
        columns = [column[0] for column in mycursor.fetchall()]
        return all_student_data, columns
    except Error as e:
        print(f"Error fetching all students: {e}")
        return [], []
    # finally:
    #     mycursor.close()
    #     close_db(connection)
 

def check_name_pass(username, password):
    user = one_student(username)
    if user and check_password_hash(user[5], password):  # Adjust the index if necessary
        return True
    return False
