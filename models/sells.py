from .db import get_connection

mydb = get_connection()

class Sell:

    def __init__(self, date, id_user,
                 id_prod,
                 pago=0.0,
                 tProduct=0,
                 id=None):
        self.tProduct = tProduct
        self.pago = pago
        self.date = date
        self.id_prod = id_prod
        self.id_user = id_user
        self.id = id

    @staticmethod
    def update_total_sale(id):
        try:
            cursor = mydb.cursor()
            cursor.callproc('UpdateTotalSale', (id,))
            mydb.commit()
            
            print("Total de venta actualizado exitosamente")
        finally:
            cursor.close()

    def save(self):
        if self.id is None:
            with mydb.cursor() as cursor:
                sql = "INSERT INTO sells(id_prod, id_user, tProduct, pago, date) "
                sql += "VALUES(4, %s, %s, %s, %s)"
                val = (4, 7, self.tProduct, 
                       self.pago, self.date)
                cursor.execute(sql, val)
                mydb.commit()
                #update_total_sale(self.id)
                self.id = cursor.lastrowid
                return self.id
        else:
            with mydb.cursor() as cursor:
                sql = "UPDATE sells SET tProduct = %s "
                sql += "pago = %s, date = %s WHERE id = %s"
                val = (self.tProduct, 
                       self.pago, self.date, self.id)
                cursor.execute(sql, val)
                mydb.commit()
                return self.id

    def delete(self):
        with mydb.cursor() as cursor:
            sql = f"DELETE FROM sells WHERE id = { id }"
            cursor.execute(sql)
            mydb.commit()
            return self.id

    @staticmethod
    def get(id):
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM sells WHERE id = { id }"
            cursor.execute(sql)
            sell = cursor.fetchone()
            if sell:
                sell = Sell(id=sell["id"],
                                  tProduct=sell["tProduct"],
                                  pago=sell["pago"],
                                  date=sell["date"])
                return sell
            return None

    @staticmethod
    def get_all(limit=10, page=1):
        offset = limit * page - limit
        sells = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM sells LIMIT { limit } OFFSET { offset }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for sell in result:
                sells.append(Sell(id=sell["id"],
                                  id_prod=sell["id_prod"],
                                  id_user=sell["id_user"],
                                  tProduct=sell["tProduct"],
                                  pago=sell["pago"],
                                  date=sell["date"]))
            return sells

    @staticmethod
    def get_by_user(id_user):
        sells = []
        with mydb.cursor(dictionary=True) as cursor:
            sql = f"SELECT * FROM sells WHERE id_user = { id_user }"
            cursor.execute(sql)
            result = cursor.fetchall()
            for sell in result:
                sells.append(Sell(tProduct=sell["tProduct"],
                                  pago=sell["pago"],
                                  date=sell["date"]))
            return sells
        
    def __str__(self):
        return f"{ self.tProduct } { self.pago } { self.date }"
    
    @staticmethod
    def count():
        with mydb.cursor(dictionary=True) as cursor:
            sql = "SELECT count(id) as total FROM sells"
            cursor.execute(sql)
            result = cursor.fetchone()
            return result['total']
    