import mysql.connector

class Database:
    def __init__(self):
            self.mydb = mysql.connector.connect(
                host="",
                user="",
                passwd="",
                database="")
    
    def run_query(self, query):
        cursor = self.mydb.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data