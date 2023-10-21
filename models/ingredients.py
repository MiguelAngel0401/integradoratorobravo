from .db import get_connection

mydb = get_connection()

class Ingredient:

    def __init__(self, name, marca, size, stock, image, id=None):
        self.id = id
        self.name = name
        self.marca = marca
        self.size = size
        self.stock = stock
        self.image = image

    def save(self):
        # Create a New Object in DB
        if self.id is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO ingredients(name, marca, size, stock, image)"
                sql += "VALUES(%s, %s, %s, %s, %s, %s)"
                val = (self.name, self.marca, 
                       self.size, self.stock, 
                       self.image)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.id
        # Update an Object
        else:
            with mydb.cursor() as cursor:
                sql = "UPDATE ingredients SET name = %s, marca = %s, size = %s, "
                sql += "stock = %s, image = %s WHERE id = %s"
                val = (self.name, self.marca, 
                       self.size, self.stock, 
                        self.image, self.id)
                cursor.execute(sql, val)
                mydb.commit()
                return self.id
            
    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM ingredients WHERE id = { self.id }"
            cursor.execute(sql)
            mydb.commit()
            return self.id
            
    @staticmethod
    def get(id):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM ingredients WHERE id = { id }"
            cursor.execute(sql)
            ingredient = cursor.fetchone()
            if ingredient:
                ingredient = Ingredient(name=ingredient["name"],
                                  marca=ingredient["marca"],
                                  size=ingredient["size"],
                                  stock=ingredient["stock"],
                                  image=ingredient["image"],
                                  id=ingredient["id"])
                return ingredient
            return None

    @staticmethod
    def get_all(limit=10, page=1):
        offset = limit * page - limit
        ingredients = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM ingredients LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for ingredient in result:
                ingredients.append(Ingredient(name=ingredient["name"],
                                  marca=ingredient["marca"],
                                  size=ingredient["size"],
                                  stock=ingredient["stock"],
                                  image=ingredient["image"],
                                  id=ingredient["id"]))
            return ingredients
        
    @staticmethod
    def count_all():
        with mydb.cursor() as cursor:
            sql = f"SELECT COUNT(id) FROM ingredients"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result[0]
        
    def __str__(self):
        return f"{ self.id } - { self.name }"