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

        # Check if user exists (tel_chat_id)
        cur.execute("SELECT id FROM telegram_users WHERE tel_chat_id = %s", (chatID,))
        result = cur.fetchall()

        if len(result) == 0:
            # Insert user (tel_chat_id)
            cur.execute("INSERT INTO telegram_users (tel_chat_id) VALUES (%s)",(chatID,))
        cur.close()

    def insertNotification(self, chatID, productID, title, stock):
        cur = self.conn.cursor()     
        # Check if product exists  (product)
        cur.execute("SELECT id FROM products WHERE product = %s", (productID,))
        result = cur.fetchall()

        if len(result) == 0:
            # Insert product (product)
            cur.execute("""INSERT 
                INTO products (product, last_stock, title) 
                VALUES (%s, %s, %s)""",(productID, stock, title))

        # Check if notification exists (tel_chat_id, product)
        cur.execute("""
            SELECT notifications.id FROM products
            INNER JOIN notifications
                ON notifications.product_id = products.id
            INNER JOIN telegram_users
                ON notifications.telegram_user_id = telegram_users.id
            WHERE telegram_users.tel_chat_id = %s AND products.product = %s
            """,(chatID, productID,))
        result = cur.fetchall()

        if len(result) == 0:
            # Insert notification (tel_chat_id, product,)
            cur.execute("SELECT id FROM telegram_users WHERE tel_chat_id = %s", (chatID,))
            result = cur.fetchall()
            user_id = result[0][0]
            cur.execute("SELECT id FROM products WHERE product = %s", (productID,))
            result = cur.fetchall()
            product_id = result[0][0]            
            cur.execute("""INSERT 
                INTO notifications (product_id, telegram_user_id) 
                VALUES (%s, %s)""",(product_id, user_id))
            cur.close()
            return 0
        else:
            cur.close()
            return -1

    def fetchUserProducts(self, chatID):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT products.product, products.title
            FROM products
            INNER JOIN notifications
                ON notifications.product_id = products.id
            INNER JOIN telegram_users
                ON notifications.telegram_user_id = telegram_users.id
            WHERE tel_chat_id = %s
        """, (chatID,))
        result = cur.fetchall()
        cur.close()
        return result

    def fetchAllProducts(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT telegram_users.tel_chat_id, products.product, products.last_stock
            FROM products
            INNER JOIN notifications
                ON notifications.product_id = products.id
            INNER JOIN telegram_users
                ON notifications.telegram_user_id = telegram_users.id
            """)
        result = cur.fetchall()
        cur.close()
        return result

    def removeNotification(self, chatID, product):
        # Check if notification exists (tel_chat_id, product)
        cur = self.conn.cursor()
        cur.execute("""
            SELECT telegram_users.id, products.id
            FROM products
            INNER JOIN notifications
                ON notifications.product_id = products.id
            INNER JOIN telegram_users
                ON notifications.telegram_user_id = telegram_users.id
            WHERE telegram_users.tel_chat_id = %s AND products.product = %s
            """,(chatID, product))
        result = cur.fetchall()

        if len(result) == 1:
            user_id = result[0][0]
            product_id = result[0][1]
            cur.execute("""DELETE FROM notifications 
                WHERE product_id = %s AND telegram_user_id = %s
                """, (product_id, user_id))
            cur.close()
            return 0
        else:
            cur.close()
            return -1

    def removeProducts(self):
        cur = self.conn.cursor()
        cur.execute("""DELETE FROM products 
            WHERE id NOT IN (SELECT product_id FROM notifications)""")
        cur.close()

    def updateStock(self, product, stock, title):
        cur = self.conn.cursor()
        cur.execute("""UPDATE products 
            SET last_stock = %s, title = %s 
            WHERE product = %s""", (stock, title, product))
        cur.close()
