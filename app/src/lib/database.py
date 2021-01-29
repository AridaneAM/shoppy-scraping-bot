import psycopg2
import os

class Database():
    def __init__(self):
            self.conn = psycopg2.connect(database=os.environ['POSTGRES_DB'], 
            user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'], 
            host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'])
            self.conn.autocommit = True
            print("Database opened successfully")

    def close(self):
        self.conn.close()

    def insertUser(self, chatID):
        cur = self.conn.cursor()     
        # comprobar si no existe usuario ya
        cur.execute("SELECT * FROM telegram_users WHERE tel_chat_id = %s", (chatID,))
        result = cur.fetchall()

        # añadir usuario si no existe
        if len(result) == 0:
            cur.execute("INSERT INTO telegram_users (tel_chat_id) VALUES (%s)",(chatID,))
        cur.close()

    def insertProduct(self, chatID, productID, title, stock):
        # comprobar si no extiste producto ya
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM products WHERE product = %s", (productID,))
        result = cur.fetchall()
        cur.close()

        # añadir producto si no existe
        if len(result) == 0:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO products (product) VALUES (%s)",(productID,))
            cur.close()

        # comprobar si no está registrada la notificación
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM telegram_users WHERE tel_chat_id = %s", (chatID,))
        result = cur.fetchall()
        # SELECT m.name, cp.id_category
        # FROM manufacturer as m
        # INNER JOIN product as p
        #     ON m.id_manufacturer = p.id_manufacturer
        # INNER JOIN category_product as cp
        #     ON p.id_product = cp.id_product
        # WHERE cp.id_category = 'some value'

        # cur.execute("SELECT * FROM notifications WHERE AND product = %s", (productID,))
        # result = cur.fetchall() 

        # registrar si no
        # obtener id telegram_user
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM telegram_users WHERE tel_chat_id = %s", (chatID,))
        result = cur.fetchall()
        user_id = result[0][0]
        # obtener id product
        cur.execute("SELECT id FROM products WHERE product = %s", (productID,))
        result = cur.fetchall()
        product_id = result[0][0]

        cur.execute("INSERT INTO notifications (product_id, telegram_user_id) VALUES (%s, %s)",(product_id, user_id))
        cur.close()


        # cur = self.conn.cursor()
        # cur.execute("INSERT INTO notifications (product_id, telegram_user_id) VALUES (%s)",(productID,))
        # cur.close()
        # # rechazar si ya está registrada
        # if len(result) == 0:
   
        #     return 0
        # else:
        #     cur.close()
        #     return -1





    def fetchProducts(self, chatID):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tel_user WHERE tel_chat_id = %s", (chatID,))
        result = cur.fetchall()
        cur.close()
        products = []
        for row in result:
            products.append(row[2])
        return products

    def removeProduct(self, chatID, productID):
        #comprobar si  extiste 
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tel_user WHERE tel_chat_id = %s AND product = %s", (chatID, productID))
        result = cur.fetchall()
        cur.close()

        if len(result):
            cur = self.conn.cursor()
            cur.execute("DELETE FROM tel_user WHERE tel_chat_id = %s AND product = %s", (chatID, productID))
            cur.close()



# crear diccionario
# coger todas las filas de db
# ir mirando cada productID, si no existe añadir nueva key y en vale array el usuario
    # si ya existe, añadir usuario al array de ese key

# products = {
#     "product1": ["user1"],
#     "product2": ["user1", "user2"]
# }
