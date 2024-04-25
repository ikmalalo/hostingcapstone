from colorama import Fore, Style
from Model.model import Admin, Customer
from VIew.view import display_menu_and_stock,display_order_history

def customer_actions(shop):
   customer_username = input("Enter your username: ")
   customer_password = input("Enter your password: ")
   customer = Customer(customer_username, customer_password)
   while True:
      print_menu_customer()
      customer_choice = input("Enter your choice: ")
      try:
         if customer_choice == '1':
            display_menu_and_stock(shop.display_menu_and_stock())
         elif customer_choice == '2':
            display_menu_and_stock(shop.sort_menu_by_price())
         elif customer_choice == '3':
            display_menu_and_stock(shop.sort_menu_by_stock())
         elif customer_choice == '4':
            keyword = input("Enter the keyword to search: ")
            display_menu_and_stock(shop.search_menu(keyword))
         elif customer_choice == '5':
            display_menu_and_stock(shop.display_menu_and_stock())
            laptop_name = input("Enter the laptop that been ordered: ")
            quantity = int(input("Enter the quantity: "))
            try:
               customer.place_order(laptop_name, quantity, shop)
            except ValueError as e:
               print(Fore.RED + str(e)) 
         elif customer_choice == '0':
            break
         else:
            print(Fore.RED + "Invalid choice. Please try again.")
      except Exception as e:
         print(Fore.RED + f"An error occurred: {str(e)}")


def admin_actions(shop):
   admin_username = input( Fore.GREEN + "Enter your username: ")
   admin_password = input("Enter your password: ")
   admin = Admin(admin_username, admin_password)
   while True:
      print_menu_admin()
      admin_choice = input("Enter your choice: ")
      if admin_choice == '1':
         display_menu_and_stock(shop.display_menu_and_stock())
      elif admin_choice == '2':
         laptop_name = input("Enter new laptop name: ")
         price = int(input("Enter price: "))
         stock = int(input("Enter stock: "))
         location = input("Enter location (beginning, middle, or end): ")
         try:
               shop.add_new_laptop(laptop_name, price, stock, location)  
         except ValueError as e:
               print(Fore.RED + str(e))
      elif admin_choice == '3':
         try:
            display_menu_and_stock(shop.display_menu_and_stock())
            laptop_name = input("Enter the name of the laptop to update: ")
            new_price = int(input("Enter the new price: "))
            new_stock = int(input("Enter the new stock: "))
            try:
               shop.update_laptop(laptop_name, new_price, new_stock)
            except ValueError as e:
               print(Fore.RED + str(e))
         except ValueError as e:
               print(Fore.RED + str(e))
      elif admin_choice == '4':
         display_menu_and_stock(shop.display_menu_and_stock())
         location = input("Enter location (beginning, middle, or end): ")
         try:
               shop.del_laptop(location)  
         except ValueError as e:
               print(Fore.RED + str(e))
      elif admin_choice == '5':
         order_history = display_order_history(shop)
         print("Order History:")
         print(order_history)
      elif admin_choice == '0':
         break
      else:
         print(Fore.RED + "Invalid choice. Please try again.")




def print_menu_customer():
   print(Fore.BLUE + "Customer Options")
   print(Fore.BLUE + "1. Display Menu and Stock")
   print(Fore.BLUE + "2. Sort Menu by Price")
   print(Fore.BLUE + "3. Sort Menu by Stock")
   print(Fore.BLUE + "4. Search Menu ")
   print(Fore.BLUE + "5. Place Order")
   print(Fore.BLUE + "0. Exit")

def print_menu_admin():
   print(Fore.BLUE + "Admin Options")
   print(Fore.BLUE + "1. Display Menu and Stock")
   print(Fore.BLUE + "2. Add New Laptop")
   print(Fore.BLUE + "3. Update Laptop")
   print(Fore.BLUE + "4. Delete Laptop")
   print(Fore.BLUE + "5. Display Orders History")
   print(Fore.BLUE + "0. Exit")
