import sqlite3

class DataBase:
    def __init__(self, db_file):
        self.connect = sqlite3.connect(db_file)
        self.cursor = self.connect.cursor()

    async def createUser(self, user_id, user_name):
        with self.connect:
            return self.cursor.execute("INSERT INTO users (user_id, user_name) VALUES (?, ?)", [user_id, user_name])

    async def createOrder(self, user_id, subject):
        with self.connect:
            return self.cursor.execute("INSERT INTO orders (user_id, subject) VALUES (?, ?)", [user_id, subject])

    async def insertFile(self, user_id, file_id):
        with self.connect:
            return self.cursor.execute("UPDATE orders SET file=(?) WHERE user_id=(?) AND close=(?)", [file_id, user_id, 0])

    async def insertPhoto(self, user_id, photo_id):
        with self.connect:
            return self.cursor.execute("UPDATE orders SET photo=(?) WHERE user_id=(?) AND close=(?)", [photo_id, user_id, 0])

    async def paidState(self, user_id, ok):
        with self.connect:
            return self.cursor.execute("UPDATE orders SET paid=(?) WHERE user_id=(?) AND close=(?)", [ok, user_id, 0])

    async def closeState(self, user_id, close):
        with self.connect:
            return self.cursor.execute("UPDATE orders SET close=(?) WHERE user_id=(?)", [close, user_id])

    async def setGrade(self, user_id, grade):
        with self.connect:
            return self.cursor.execute("UPDATE orders SET grade=(?) WHERE user_id=(?) AND close=(?)", [grade, user_id, 0])

    async def setAmount(self, user_id, amount):
        with self.connect:
            return self.cursor.execute("UPDATE orders SET amount=(?) WHERE user_id=(?) AND close=(?)", [amount, user_id, 0])

    async def getOrderByFile(self, file_id):
        with self.connect:
            return self.cursor.execute("SELECT id FROM orders WHERE file=(?) AND close=(?)", [file_id, 0]).fetchall()

    async def getUserByPhoto(self, photo_id):
        with self.connect:
            return self.cursor.execute("SELECT user_id FROM orders WHERE photo=(?) AND close=(?)", [photo_id, 0]).fetchall()

    async def getAmount(self, user_id):
        with self.connect:
            return self.cursor.execute("SELECT amount FROM orders WHERE user_id=(?) AND close=0", [user_id]).fetchall()

    async def checkPaidState(self, user_id):
        with self.connect:
            return self.cursor.execute("SELECT paid FROM orders WHERE user_id=(?) AND close=0", [user_id]).fetchall()

    async def getP2P(self):
        with self.connect:
            return self.cursor.execute("SELECT p2p FROM config").fetchall()

    def getToken(self):
        with self.connect:
            return self.cursor.execute("SELECT token FROM config").fetchall()

    async def getAdmin(self):
        with self.connect:
            return self.cursor.execute("SELECT admin FROM config").fetchall()