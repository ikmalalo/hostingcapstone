from collections import deque
from colorama import init, Fore
import mysql.connector
from mysql.connector import Error

class User:
   def __init__(self, username, password):
      self.username = username
      self.password = password

class Admin(User):
   def __init__(self, username, password):
      super().__init__(username, password)

   def delete_order(self, shop, customer_name):
      shop.delete_order(customer_name)

class Customer(User):
   def __init__(self, username, password):
      super().__init__(username, password)

   def place_order(self, laptop_name, quantity, shop):
      laptop_name = laptop_name.lower()
      for laptop in shop.barang:
         if laptop['nama'].lower() == laptop_name:
            if laptop['stock'] >= quantity:
                  order = (self.username, laptop_name, quantity)
                  shop.order_queue.append(order)
                  laptop['stock'] -= quantity
                  print(Fore.GREEN + f"Order placed by {self.username}: {quantity} {laptop_name.capitalize()}(s)")
            else:
                  raise ValueError(f"Insufficient stock for {laptop_name.capitalize()}") 
            return
      raise ValueError(f"Laptop '{laptop_name.capitalize()}' not found") 

class LaptopShop:
   def __init__(self):
      self.total_income = 0
      self.order_stack = deque()
      self.order_queue = deque()
      self.menu = []
      self.orders = []
      self.barang = self.fetch_laptops_from_database()

   def fetch_laptops_from_database(self):
      connection = self.connect_to_database()
      if connection:
         cursor = connection.cursor(dictionary=True)
         cursor.execute("SELECT * FROM barang;")
         barang = cursor.fetchall()
         connection.close()
         return barang
      else:
         print("Failed to connect to database")
         return []

   def connect_to_database(self):
      hostname = "izh.h.filess.io"
      database = "ReyTop_unlessblow"
      port = "3306"
      username = "ReyTop_unlessblow"
      password = "234f1036bad6ab5930d6d3a10a4868b88ebe3e18"

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
      laptop_found = False
      for laptop in self.barang:
         if laptop['name'].lower() == laptop_name.lower():
               laptop['price'] = new_price
               laptop['stock'] = new_stock
               laptop_found = True
               print(f"Laptop '{laptop_name}' updated successfully.")
               break
      
      if not laptop_found:
         print(f"Laptop '{laptop_name}' not found.")

   def add_new_laptop(self, laptop_name, price, stock, location):
      if location not in ['beginning', 'middle', 'end']:
         raise ValueError("Invalid location. Please choose 'beginning', 'middle', or 'end'.")

      if location == 'beginning':
         self.barang.insert(0, {"name": laptop_name, "price": price, "stock": stock})
      elif location == 'end':
         self.barang.append({"name": laptop_name, "price": price, "stock": stock})
      elif location == 'middle':
         middle_index = len(self.barang) // 2
         self.barang.insert(middle_index, {"name": laptop_name, "price": price, "stock": stock})

   def del_laptop(self, location=None):
      if location not in ['beginning', 'middle', 'end']:
         raise ValueError("Invalid location. Please choose 'beginning', 'middle', or 'end'.")

      if location == 'beginning':
         if self.barang:
               deleted_laptop = self.barang.pop(0)
         else:
               raise ValueError("No barang found to delete.")
      elif location == 'end':
         if self.barang:
               deleted_laptop = self.barang.pop()
         else:
               raise ValueError("No barang found to delete.")
      elif location == 'middle':
         if not self.barang:
               raise ValueError("No barang found to delete.")

         if len(self.barang) == 1:
               raise ValueError("There is only one laptop available. You cannot delete it from the middle.")

         laptop_to_delete = input("Enter the laptop name to delete: ")
         for laptop in self.barang:
               if laptop['name'] == laptop_to_delete:
                  self.barang.remove(laptop)
                  return
         raise ValueError(f"Laptop '{laptop_to_delete}' not found.")
      
   def display_order_history(self):
      return self.latops

   def display_menu_and_stock(self):
      return self.barang

   def update_menu_and_stock(self):
      return self.barang

   def display_orders(self):
      return self.order_queue

   def sort_menu_by_price(self):
      return sorted(self.barang, key=lambda x: x['price'])

   def sort_menu_by_stock(self):
      return sorted(self.barang, key=lambda x: x['stock'])

   def search_menu(self, keyword):
      results = []
      for laptop in self.barang:
         for key, value in laptop.items():
               if keyword.lower() in str(value).lower():
                  results.append(laptop)
                  break  
      return results
