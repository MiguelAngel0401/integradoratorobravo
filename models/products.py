from .db import get_connection

mydb = get_connection()

class Product:

    def __init__(self, name,
                 category_id, price=0.0, 
                 size=0,
                 stock=10, image="", id=None):
        self.name = name
        self.size = size
        self.price = price
        self.stock = stock
        self.category_id = category_id
        self.image = image
        self.id = id

    def save(self):
        if self.id is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO products(name, size, price, stock, category_id, image, id_prom) "
                sql += "VALUES(%s, %s, %s, %s, %s, %s, %s)"
                val = (self.name, self.size, 
                       self.price, self.stock, 
                       self.category_id, self.image, 4)
                cursor.execute(sql, val)
                mydb.commit()
                self.id = cursor.lastrowid
                return self.id
        else:
            with mydb.cursor() as cursor:
                sql = "UPDATE products SET name = %s, size = %s, price = %s, "
                sql += "stock = %s, category_id = %s, image = %s WHERE id = %s"
                val = (self.name, self.size, 
                       self.price, self.stock, 
                       self.category_id, self.image, self.id)
                cursor.execute(sql, val)
                mydb.commit()
                return self.id

    def delete(self):
        with mydb.cursor() as cursor:
            sql = "DELETE FROM products WHERE id = %s"
            cursor.execute(sql, (self.id,))
            mydb.commit()
            return self.id

    @staticmethod
    def get(id):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM products WHERE id = { id }"
            cursor.execute(sql)
            product = cursor.fetchone()
            if product:
                product = Product(name=product["name"],
                                  size=product["size"],
                                  price=product["price"],
                                  stock=product["stock"],
                                  category_id=product["category_id"],
                                  image=product["image"],
                                  id=product["id"])
                return product
            return None

    @staticmethod
    @staticmethod
    def search(name):
        if name != None:
            with mydb.cursor(dictionary=True) as cursor:
                sql = "SELECT * FROM products LIKE %s WHERE name =  ORDER BY id DESC"
                cursor.execute(sql, (name,))
                product = cursor.fetchone()
                if product:
                    product = Product(name=product["name"],
                                    size=product["size"],
                                    price=product["price"],
                                    stock=product["stock"],
                                    category_id=product["category_id"],
                                    image=product["image"],
                                    id=product["id"])
                    return product
        return None

    
    @staticmethod
    def get_all(limit=10, page=1):
        offset = limit * page - limit
        products = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM products LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for product in result:
                products.append(Product(name=product["name"],
                                  size=product["size"],
                                  price=product["price"],
                                  stock=product["stock"],
                                  category_id=product["category_id"],
                                  image=product["image"],
                                  id=product["id"]))
            return products

    @staticmethod
    def get_by_category(id_category):
        products = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM products WHERE category_id = { id_category }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for product in result:
                products.append(Product(name=product["name"],
                                  size=product["size"],
                                  price=product["price"],
                                  stock=product["stock"],
                                  category_id=product["category_id"],
                                  image=product["image"],
                                  id=product["id"]))
            return products
        
    def __str__(self):
        return f"{ self.name } { self.size }"
    
    @staticmethod
    def count():
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT count(id) as total FROM products"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result['total']