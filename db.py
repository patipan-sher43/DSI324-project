import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="fordzaa55"
)

my_cursor = mydb.cursor()

