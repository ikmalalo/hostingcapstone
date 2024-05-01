from collections import deque
from colorama import Fore
import mysql.connector
from mysql.connector import Error

class SingletonLogger:
   _instance = None  
   _connection = None

   def __new__(cls):
      if cls._instance is None:
         cls._instance = super().__new__(cls)
         cls._instance.connect_to_database()
      return cls._instance

   def connect_to_database(self):
      try:
         hostname = "462.h.filess.io"
         database = "reytop3_perfectly"
         port = "3306"
         username = "reytop3_perfectly"
         password = "73bac833e2e1437cc2e127b57d2a70b7b4f11308"

         self._connection = mysql.connector.connect(
               host=hostname,
               database=database,
               user=username,
               password=password,
               port=port
         )
         if self._connection.is_connected():
               print("Welcome to ReyTop ✨")
      except Error as e:
         print("Error while connecting to MySQL", e)

   def log(self, message):
      print(message)

   def close_connection(self):
      if self._connection:
         self._connection.close()
         print("Please wait, Going to Connecting Database")

logger1 = SingletonLogger()
logger2 = SingletonLogger()

if logger1 is logger2:
   print("Instance Checking, Success")

logger1.close_connection()

class User:
   def __init__(self, username, password):
      self.username = username
      self.password = password

class Admin(User):
   def __init__(self, username, password, shop):
      if shop.authenticate_admin(username, password):
         super().__init__(username, password)
         self.shop = shop  
      else:
         raise ValueError("Invalid username or password.")

class Customer(User):
   def __init__(self, username, password, shop):
      if shop.authenticate_user(username, password):
         super().__init__(username, password)
         self.shop = shop
      else:
         raise ValueError("Invalid username or password.")

   def place_order(self, order_type, id_barang, quantity, days=1):
      try:
            found = False
            id_barang = int(id_barang)
            for laptop in self.shop.barang:  
               if laptop.get('id_barang') == id_barang:
                  stock = int(laptop['stock'])
                  harga = int(laptop['harga'])
                  nama_barang = laptop['nama_barang']
                  total_harga = harga * quantity
                  if stock >= quantity:
                        order = (id_barang, quantity, order_type, days, total_harga)
                        self.shop.order_queue.append(order)  
                        try:
                           connection = self.shop.connect_to_database()  
                           if connection:
                              cursor = connection.cursor(dictionary=True)
                              if order_type == "pembelian":
                                    cursor.execute("""
                                       INSERT INTO transaksi (id_transaksi, id_barang, total_barang)
                                       VALUES (DEFAULT, %s, %s)
                                    """, (id_barang, quantity))
                                    cursor.execute("""
                                       INSERT INTO pembelian (id_pembelian, id_transaksi, tanggal_pembelian, total_harga)
                                       VALUES (DEFAULT, LAST_INSERT_ID(), CURRENT_DATE(), %s)
                                    """, (total_harga,))
                              elif order_type == "penyewaan":
                                    jaminan = input("Masukkan jaminan: ")
                                    cursor.execute("""
                                       INSERT INTO transaksi (id_transaksi, id_barang, total_barang)
                                       VALUES (DEFAULT, %s, %s)
                                    """, (id_barang, quantity))
                                    from datetime import datetime, timedelta
                                    today = datetime.now()
                                    return_date = today + timedelta(days=days)
                                    cursor.execute("""
                                       INSERT INTO penyewaan (id_penyewaan, id_transaksi, tanggal_minjam, jaminan, tanggal_kembali, total_harga)
                                       VALUES (DEFAULT, LAST_INSERT_ID(), CURRENT_DATE(), %s, %s, %s)
                                    """, (jaminan, return_date.strftime('%Y-%m-%d'), total_harga))
                              connection.commit()
                              connection.close()
                        except Exception as e:
                           print(Fore.RED + f"Failed to insert transaction data.")
                        if order_type == "pembelian":
                           laptop['stock'] = str(stock - quantity)
                           print(Fore.GREEN + f"Order placed by {self.username}: {quantity} {nama_barang.capitalize()}(s)")
                        elif order_type == "penyewaan":
                           price_per_day = harga / 50
                           total_harga = price_per_day * days * quantity
                           print(Fore.GREEN + f"Order placed by {self.username}: {quantity} {nama_barang.capitalize()}(s) for {days} days. Total price: ${total_harga}")
                        found = True
                        break
                  else:
                        raise ValueError(f"Insufficient stock for {nama_barang.capitalize()}")
            if not found:
               raise ValueError(f"Laptop with ID {id_barang} not found")
      except ValueError as e:
            print(Fore.RED + f"Invalid Input data.")
      except Exception as e:
            print(Fore.RED + f"Invalid Input data.")

class LaptopShop:
   def __init__(self):
      self.order_stack = deque()
      self.order_queue = deque()
      self.menu = []
      self.orders = []
      self.barang = self.fetch_laptops_from_database()
      self.users = self.fetch_users_from_database()
      self.admins = self.fetch_admins_from_database()

   def fetch_purchase_history_from_database(self):
      try:
         connection = self.connect_to_database()
         if connection:
               cursor = connection.cursor(dictionary=True)
               cursor.execute("""
                  SELECT pembelian.id_pembelian, pembelian.tanggal_pembelian, pembelian.total_harga, 
                  transaksi.total_barang
                  FROM pembelian
                  INNER JOIN transaksi ON pembelian.id_pembelian = transaksi.total_barang;
               """)
               purchase_history = cursor.fetchall()
               connection.close()
               return purchase_history
         else:
               print("Failed to connect to database")
               return []
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")
         return []

   def fetch_laptops_from_database(self):
      try:
         connection = self.connect_to_database()
         if connection:
               cursor = connection.cursor(dictionary=True)
               cursor.execute("SELECT id_barang, nama_barang, harga, stock, spek FROM barang;")
               barang = cursor.fetchall()
               connection.close()
               for laptop in barang:
                  if 'nama_barang' not in laptop:
                     raise ValueError("Missing key 'nama_barang' in laptop data")
               return barang
         else:
               print("Failed to connect to database")
               return []
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")
         return []

   def fetch_admins_from_database(self):
      try:
         connection = self.connect_to_database()
         if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admin;")
            admins_data = cursor.fetchall()
            connection.close()
            return admins_data
         else:
            print("Failed to connect to database")
            return []
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")
         return []
      
   def fetch_users_from_database(self):
      try:
         connection = self.connect_to_database()
         if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM pelanggan;")
            users_data = cursor.fetchall()
            connection.close()
            return users_data
         else:
            print("Failed to connect to database")
            return []
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")
         return []

   def authenticate_admin(self, username, password):
      try:
         connection = self.connect_to_database()
         if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admin WHERE nama_admin = %s AND password = %s", (username, password))
            admin = cursor.fetchone()
            connection.close()
            if admin:
               return True
            else:
               return False
         else:
            print("Failed to connect to database")
            return False
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")
         return False

   def authenticate_user(self, username, password):
      try:
         connection = self.connect_to_database()
         if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM pelanggan WHERE nama_pelanggan = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            connection.close()
            if user:
               return True
            else:
               return False
         else:
            print("Failed to connect to database")
            return False
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")
         return False

   def connect_to_database(self):
      hostname = "462.h.filess.io"
      database = "reytop3_perfectly"
      port = "3306"
      username = "reytop3_perfectly"
      password = "73bac833e2e1437cc2e127b57d2a70b7b4f11308"

      try:
         connection = mysql.connector.connect(host=hostname, database=database, user=username, password=password, port=port)
         if connection.is_connected():
               print("Connecting to Database, Thanks for the wait❤️")
               return connection
      except Error as e:
         print("Error while connecting to MySQL", e)
         return None

   def add_new_laptop(self, laptop_name, price, stock, spek):
      try:
         connection = self.connect_to_database()
         if connection:
               cursor = connection.cursor()
               cursor.execute("""
                  INSERT INTO barang (nama_barang, harga, stock, spek)
                  VALUES (%s, %s, %s, %s)
               """, (laptop_name, price, stock, spek))

               connection.commit()
               connection.close()
               self.update_menu_and_stock()
               print(Fore.GREEN + f"Laptop '{laptop_name}' added successfully.")
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")

   def update_laptop(self, laptop_id, new_price, new_stock, new_spek):
      try:
         connection = self.connect_to_database()
         if connection:
               cursor = connection.cursor()
               cursor.execute("""
                  UPDATE barang
                  SET harga = %s, stock = %s, spek = %s
                  WHERE id_barang = %s;
               """, (new_price, new_stock, new_spek, laptop_id))
               connection.commit()
               connection.close()
               self.update_menu_and_stock()
               print(Fore.GREEN + f"Laptop with ID '{laptop_id}' updated successfully.")
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")

   def del_laptop(self, laptop_id):
      try:
         connection = self.connect_to_database()
         if connection:
               cursor = connection.cursor()
               cursor.execute("""
                  DELETE FROM barang
                  WHERE id_barang = %s;
               """, (laptop_id,))
               connection.commit()
               connection.close()
               self.update_menu_and_stock()
               print(Fore.GREEN + f"Laptop with ID '{laptop_id}' deleted successfully.")
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")

   def display_pembelian_history(shop):
      try:
         return shop.order_queue
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")
         return []

   def display_penyewaan_history(shop):
      try:
         return shop.order_queue
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")
         return []

   def display_menu_and_stock(self, order_type="pembelian", sorting_order=None):
      try:
         if order_type == "pembelian" or order_type == "penyewaan":
               connection = self.connect_to_database()
               if connection:
                  cursor = connection.cursor(dictionary=True)
                  cursor.execute("SELECT id_barang, nama_barang, harga, stock, spek FROM barang;")
                  menu = cursor.fetchall()
                  connection.close()
                  if sorting_order:
                     self.sort_menu(sorting_order)
                  if order_type == "pembelian":
                     return self.barang
                  elif order_type == "penyewaan":
                     rented_menu = []
                     for laptop in self.barang:
                           laptop_copy = laptop.copy()
                           rented_menu.append(laptop_copy)
                     return rented_menu
         else:
               raise ValueError("Invalid order type. Please choose 'pembelian' or 'penyewaan'.")
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")
         return []

   def sort_menu(self, sorting_order='asc'):
      try:
         if sorting_order.lower() == 'asc':
               self.barang = sorted(self.barang, key=lambda x: x['harga'])
         elif sorting_order.lower() == 'desc':
               self.barang = sorted(self.barang, key=lambda x: x['harga'], reverse=True)
         else:
               raise ValueError("Invalid sorting order. Please choose 'asc' for ascending or 'desc' for descending.")
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")

   def update_menu_and_stock(self):
      try:
         return self.barang
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")
         return []

   def search_menu(self, keyword):
      try:
         results = []
         for laptop in self.barang:
            for key, value in laptop.items():
                  if keyword.lower() in str(value).lower():
                     results.append(laptop)
                     break  
         return results
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")
         return []

   def update_menu_and_stock(self):
      try:
         self.barang = self.fetch_laptops_from_database()
      except Exception as e:
         print(Fore.RED + f"Invalid Input data.")

   def add_new_admin(self, username, password, jobdesk):
      try:
            if not username.isalpha():
               raise ValueError("Username should only contain letters.")
            connection = self.connect_to_database()
            if connection:
               cursor = connection.cursor()
               cursor.execute("SELECT * FROM admin WHERE nama_admin = %s", (username,))
               existing_admin = cursor.fetchone()
               if existing_admin:
                  raise ValueError("Admin with this username already exists.")
               else:
                  cursor.execute("INSERT INTO admin (nama_admin, password, jobdesk) VALUES (%s, %s, %s)", (username, password, jobdesk))
                  connection.commit()
                  connection.close()
                  print(Fore.GREEN + "Admin registered successfully!")
      except Exception as e:
            print(Fore.RED + f"Invalid Input data.")

   def add_new_customer(self, username, password, email, nohp):
      try:
            if not username.isalpha():
               raise ValueError("Username should only contain letters.")
            connection = self.connect_to_database()
            if connection:
               cursor = connection.cursor()
               cursor.execute("SELECT * FROM pelanggan WHERE nama_pelanggan = %s", (username,))
               existing_customer = cursor.fetchone()
               if existing_customer:
                  raise ValueError("Customer with this username already exists.")
               else:
                  cursor.execute("INSERT INTO pelanggan (nama_pelanggan, password, email, nohp) VALUES (%s, %s, %s, %s)", (username, password, email, nohp))
                  connection.commit()
                  connection.close()
                  print(Fore.GREEN + "Customer registered successfully!")
      except Exception as e:
            print(Fore.RED + f"Invalid Input data.")