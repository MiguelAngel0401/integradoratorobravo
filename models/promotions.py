from .db import get_connection

mydb = get_connection()

class Promotion:

    def __init__(self, name, description, id=None):
        self.id = id
        self.name = name
        self.description = description

    def save(self):
        # Create a New Object in DB
        if self.id is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO promotions(name, description) VALUES(%s, %s)"
                val = (self.name, self.description)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.id
        # Update an Object
        else:
            with mydb.cursor() as cursor:
                sql = "UPDATE promotions SET name = %s, description = %s WHERE id = %s"
                val = (self.name, self.description, self.id)
                cursor.execute(sql, val)
                mydb.commit()
                return self.id
            
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM promotions WHERE id = { self.id }"
            cursor.execute(sql)
            mydb.commit()
            return self.id
            
    @staticmethod
    def get(id):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT name, description FROM promotions WHERE id = { id }"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
            promotion = Promotion(result["name"], result["description"], id)
            return promotion
        
    @staticmethod
    def get_all():
        promotions = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT id, name, description FROM promotions"
            cursor.execute(sql)
            result = cursor.fetchall()
            for item in result:
                promotions.append(Promotion(item["name"], item["description"], item["id"]))
            return promotions
        
    def __str__(self):
        return f"{ self.id } - { self.name }"