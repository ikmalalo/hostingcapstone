from collections import deque
from colorama import init, Fore
import mysql.connector
from mysql.connector import Error

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

   def delete_order(self, customer_name):
      try:
         for order in self.shop.order_queue:  
               if order[0] == customer_name:
                  self.shop.order_queue.remove(order)
                  print(Fore.GREEN + f"Order for {customer_name} deleted successfully.")
                  return
         print(Fore.RED + f"No order found for customer '{customer_name}'.")
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")

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
                  harga = int(laptop['harga'])  # Harga per unit laptop
                  nama_barang = laptop['nama_barang']
                  total_harga = harga * quantity  # Hitung total harga berdasarkan harga per unit dan jumlah barang

                  if stock >= quantity:
                     order = (id_barang, quantity, order_type, days, total_harga)  # Include order type, days, and total price
                     self.shop.order_queue.append(order)

                     # Tambahkan data transaksi ke database sesuai order_type
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
                                 cursor.execute("""
                                    INSERT INTO transaksi (id_transaksi, id_barang, total_barang)
                                    VALUES (DEFAULT, %s, %s)
                                 """, (id_barang, quantity)) 

                                 cursor.execute("""
                                    INSERT INTO penyewaan (id_penyewaan, id_transaksi, tanggal_minjam, jaminan, total_harga)
                                    VALUES (DEFAULT, LAST_INSERT_ID(), CURRENT_DATE(), %s, %s)
                                 """, (None, total_harga))

                           connection.commit()
                           connection.close()
                     except Exception as e:
                        print(Fore.RED + f"Failed to insert transaction data: {str(e)}")


                     if order_type == "pembelian":  # Check order type
                           laptop['stock'] = str(stock - quantity)
                           print(Fore.GREEN + f"Order placed by {self.username}: {quantity} {nama_barang.capitalize()}(s)")
                     elif order_type == "penyewaan":  # If order type is "penyewaan"
                           price_per_day = harga / 50  # Divide price by 50 for rental
                           total_price = price_per_day * days * quantity
                           print(Fore.GREEN + f"Order placed by {self.username}: {quantity} {nama_barang.capitalize()}(s) for {days} days. Total price: ${total_price}")

                     found = True
                     break
                  else:
                     raise ValueError(f"Insufficient stock for {nama_barang.capitalize()}")
         if not found:
               raise ValueError(f"Laptop with ID {id_barang} not found")
      except ValueError as e:
         print(Fore.RED + str(e))
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")



class LaptopShop:
   def __init__(self):
      self.total_income = 0
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
        print(Fore.RED + f"An error occurred: {str(e)}")
        return []

   def fetch_laptops_from_database(self):
      try:
         connection = self.connect_to_database()
         if connection:
               cursor = connection.cursor(dictionary=True)
               cursor.execute("SELECT id_barang, nama_barang, harga, stock FROM barang;")
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
         print(Fore.RED + f"An error occurred: {str(e)}")
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
         print(Fore.RED + f"An error occurred: {str(e)}")
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
         print(Fore.RED + f"An error occurred: {str(e)}")
         return []

   def authenticate_admin(self, username, password):
      try:
         for admin in self.admins:
            if admin.get('nama_admin') == username and admin.get('password') == password:
               return True
         return False
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")
         return False
      
   def authenticate_user(self, username, password):
      try:
         for user in self.users:
            if user.get('nama_pelanggan') == username and user.get('password') == password:
               return True
         return False
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")
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
               db_Info = connection.get_server_info()
               print("Connected to MySQL Server version ", db_Info)
               return connection
      except Error as e:
         print("Error while connecting to MySQL", e)
         return None


   def calculate_total_income(self):
      return self.total_income
   
   def update_laptop(self, laptop_name, new_price, new_stock):
      try:
         laptop_found = False
         for laptop in self.barang:
               if laptop['nama_barang'].lower() == laptop_name.lower():
                  laptop['harga'] = new_price
                  laptop['stock'] = new_stock
                  laptop_found = True
                  print(f"Laptop '{laptop_name}' updated successfully.")
                  break
         
         if not laptop_found:
               raise ValueError(f"Laptop '{laptop_name}' not found.")
      except ValueError as e:
         print(Fore.RED + str(e))
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")

   def add_new_laptop(self, laptop_name, price, stock, location):
      try:
         if location not in ['beginning', 'middle', 'end']:
               raise ValueError("Invalid location. Please choose 'beginning', 'middle', or 'end'.")
         
         if location == 'beginning':
               self.barang.insert(0, {"nama_barang": laptop_name, "harga": price, "stock": stock})
         elif location == 'end':
               self.barang.append({"nama_barang": laptop_name, "harga": price, "stock": stock})
         elif location == 'middle':
               middle_index = len(self.barang) // 2
               self.barang.insert(middle_index, {"nama_barang": laptop_name, "harga": price, "stock": stock})
      except ValueError as e:
         print(Fore.RED + str(e))
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")


   def del_laptop(self, laptop_name):
      try:
         laptop_found = False
         for laptop in self.barang:
               if laptop['nama_barang'].lower() == laptop_name.lower():
                  self.barang.remove(laptop)
                  laptop_found = True
                  print(f"Laptop '{laptop_name}' deleted successfully.")
                  break
         
         if not laptop_found:
               print(f"Laptop '{laptop_name}' not found.")
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")

      
   def display_pembelian_history(shop):
      try:
         return shop.order_queue
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")
         return []

   def display_penyewaan_history(shop):
      try:
         return shop.order_queue
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")
         return []

   def display_menu_and_stock(self, order_type="pembelian"):
      try:
         if order_type == "pembelian":
               return self.barang
         elif order_type == "penyewaan":
               rented_menu = []
               for laptop in self.barang:
                  laptop_copy = laptop.copy()  # Create a copy of the laptop dictionary
                  laptop_copy['harga']   # Divide the price by 50 for rental
                  rented_menu.append(laptop_copy)
               return rented_menu
         else:
               raise ValueError("Invalid order type. Please choose 'pembelian' or 'penyewaan'.")
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")
         return []

   def update_menu_and_stock(self):
      try:
         return self.barang
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")
         return []

   def display_orders(self):
      try:
         return self.order_queue
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")
         return []
      
   # def sort_menu_by_ascending(self):
   #    urutan_robux = sorted(self.daftar_robux.values(), key=lambda robux: robux.kode)

   def sort_menu_by_ascending(shop):
      try:
         connection = shop.connect_to_database()
         if connection:
               cursor = connection.cursor(dictionary=True)
               cursor.execute("SELECT * FROM barang ORDER BY harga ASC;")
               sorted_menu = cursor.fetchall()
               connection.close()
               return sorted_menu
         else:
               print("Failed to connect to database")
               return []
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")
         return []

   def sort_menu_by_descending(shop):
      try:
         connection = shop.connect_to_database()
         if connection:
               cursor = connection.cursor(dictionary=True)
               cursor.execute("SELECT * FROM barang ORDER BY harga DESC;")
               sorted_menu = cursor.fetchall()
               connection.close()
               return sorted_menu
         else:
               print("Failed to connect to database")
               return []
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")
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
         print(Fore.RED + f"An error occurred: {str(e)}")
         return []

   def add_new_admin(self, username, password):
      try:
         if not username.isalpha():
               raise ValueError("Username should only contain letters.")
         
         # Lakukan pengecekan apakah admin dengan username tersebut sudah ada
         for admin in self.admins:
               if admin.get('nama_admin') == username:
                  raise ValueError("Admin with this username already exists.")
         
         # Jika tidak ada admin dengan username yang sama, tambahkan admin baru
         self.admins.append({'nama_admin': username, 'password': password})
         print(Fore.GREEN + "Admin registered successfully!")
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")

   def add_new_customer(self, username, password):
      try:
         if not username.isalpha():
               raise ValueError("Username should only contain letters.")
         
         # Lakukan pengecekan apakah customer dengan username tersebut sudah ada
         for user in self.users:
               if user.get('nama_pelanggan') == username:
                  raise ValueError("Customer with this username already exists.")
         
         # Jika tidak ada customer dengan username yang sama, tambahkan customer baru
         self.users.append({'nama_pelanggan': username, 'password': password})
         print(Fore.GREEN + "Customer registered successfully!")
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")