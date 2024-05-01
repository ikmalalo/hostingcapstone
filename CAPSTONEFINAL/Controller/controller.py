from colorama import Fore
from Model.model import Admin, Customer
from View.view import display_menu_and_stock, display_pembelian_history, display_penyewaan_history
import pwinput

def customer_actions(shop): 
    while True:
        try:
            customer_username = input("Enter your username: ")
            customer_password = pwinput.pwinput(prompt="Enter your password: ")
            customer = Customer(customer_username, customer_password, shop)
            while True:
                print_menu_customer()
                customer_choice = input("Enter your choice: ")
                try:
                    if customer_choice == '1':
                        display_menu_and_stock(shop.display_menu_and_stock())
                    elif customer_choice == '2':
                        try:
                            menu = shop.display_menu_and_stock()
                            display_menu_and_stock(menu)
                            sorting_order = input("Enter sorting order: 'asc' for ascending or 'desc' for descending: ")
                            if sorting_order.lower() == 'asc' or sorting_order.lower() == 'desc':
                                shop.sort_menu(sorting_order)
                                menu = shop.display_menu_and_stock()  
                                display_menu_and_stock(menu)
                            else:
                                raise ValueError("Invalid sorting order. Please enter 'asc' for ascending or 'desc' for descending.")
                        except ValueError as e:
                            print(Fore.RED + f"Invalid Input data.")
                    elif customer_choice == '3':
                        keyword = input("Enter the keyword to search: ")
                        display_menu_and_stock(shop.search_menu(keyword))
                    elif customer_choice == '4':
                        display_menu_and_stock(shop.display_menu_and_stock())
                        order_type = input("Enter order type (pembelian or penyewaan): ")
                        id_barang = input("Enter the ID of the laptop that you want to order: ")
                        quantity = int(input("Enter the quantity: "))
                        if order_type not in ["pembelian", "penyewaan"]:
                            raise ValueError("Invalid order type. Please choose 'pembelian' or 'penyewaan'.")
                        if order_type == "penyewaan":
                            display_menu_and_stock(shop.display_menu_and_stock("penyewaan"), order_type="penyewaan")
                            days = int(input("Enter the number of days for rental: "))
                            customer.place_order(order_type, id_barang, quantity, days)
                        else:
                            customer.place_order(order_type, id_barang, quantity)
                    elif customer_choice == '0':
                        return
                    else:
                        print(Fore.RED + "Invalid choice. Please try again.")
                except KeyboardInterrupt:
                    print(Fore.RED + "Program interrupted by the user.")
                except Exception as e:
                    print(Fore.RED + f"Invalid Input data.")
        except KeyboardInterrupt:
            print(Fore.RED + "Program interrupted by the user.")
        except Exception as e:
            print(Fore.RED + f"Invalid Input data.")


def admin_actions(shop):
    while True:
        try:
            admin_username = input(Fore.GREEN + "Enter your username: ")
            admin_password = pwinput.pwinput(prompt="Enter your password: ")
            admin = Admin(admin_username, admin_password, shop)
            while True:
                print_menu_admin()
                admin_choice = input("Enter your choice: ")
                try:
                    if admin_choice == '1':
                        display_menu_and_stock(shop.display_menu_and_stock())
                    elif admin_choice == '2':
                        laptop_name = input("Enter new laptop name: ")
                        price = int(input("Enter price: "))
                        stock = int(input("Enter stock: "))
                        spek = input("Enter laptop spec : ")
                        try:
                            shop.add_new_laptop(laptop_name, price, stock, spek)
                        except ValueError as e:
                            print(Fore.RED + f"Invalid Input data.")
                    elif admin_choice == '3':
                        try:
                            display_menu_and_stock(shop.display_menu_and_stock())
                            laptop_name = input("Enter the ID of the laptop to update: ")
                            new_price = int(input("Enter the new price: "))
                            new_stock = int(input("Enter the new stock: "))
                            new_spek = (input("Enter the new spec: "))
                            try:
                                shop.update_laptop(laptop_name, new_price, new_stock, new_spek)
                            except ValueError as e:
                                print(Fore.RED + f"Invalid Input data.")
                        except ValueError as e:
                            print(Fore.RED + f"Invalid Input data.")
                    elif admin_choice == '4':
                        display_menu_and_stock(shop.display_menu_and_stock())
                        deleteLaptop = input("Enter the laptop ID to delete: ")
                        try:
                            shop.del_laptop(deleteLaptop)
                        except ValueError as e:
                            print(Fore.RED + f"Invalid Input data.")
                    elif admin_choice == '5':
                        print("1. Display Pembelian History")
                        print("2. Display Penyewaan History")
                        history_choice = input("Enter your choice: ")
                        if history_choice == '1':
                            display_pembelian_history(shop)
                        elif history_choice == '2':
                            display_penyewaan_history(shop)
                        else:
                            print(Fore.RED + "Invalid choice. Please try again.")

                    elif admin_choice == '0':
                        return
                    else:
                        print(Fore.RED + "Invalid choice. Please try again.")
                except KeyboardInterrupt:
                        print(Fore.RED + "Program interrupted by the user.")
                except Exception as e:
                    print(Fore.RED + f"Invalid Input data.")
        except KeyboardInterrupt:
            print(Fore.RED + "Program interrupted by the user.")
        except Exception as e:
            print(Fore.RED + f"Invalid Input data.")



def print_menu_customer():
    print(Fore.BLUE + "Customer Options")
    print(Fore.BLUE + "1. Display Menu and Stock")
    print(Fore.BLUE + "2. Sort Menu by Price")
    print(Fore.BLUE + "3. Search Menu ")
    print(Fore.BLUE + "4. Place Order")
    print(Fore.BLUE + "0. Exit")


def print_menu_admin():
    print(Fore.BLUE + "Admin Options")
    print(Fore.BLUE + "1. Display Menu and Stock")
    print(Fore.BLUE + "2. Add New Laptop")
    print(Fore.BLUE + "3. Update Laptop")
    print(Fore.BLUE + "4. Delete Laptop")
    print(Fore.BLUE + "5. Display Orders History")
    print(Fore.BLUE + "0. Exit")
