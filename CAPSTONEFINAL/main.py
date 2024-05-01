from Model.model import  LaptopShop, SingletonLogger
from Controller.controller import customer_actions, admin_actions
from prettytable import PrettyTable 
from colorama import Fore, Style

def mainsingleton():
    SingletonLogger1 =SingletonLogger.get_instance()
    SingletonLogger2 =SingletonLogger.get_instance()
    
    if SingletonLogger1 is SingletonLogger2:
        print("Instance Checking for Singleton")
        
    SingletonLogger2.log("this is logged using a singleton logging system")
    

def main():
    shop = LaptopShop()
    try:
        while True:
            print_menu_main()
            choice = input(Fore.BLUE + "Enter your choice: ").lower() 
            if choice == '1':
                login_menu(shop)
            elif choice == '2':
                register_menu(shop)
            elif choice == '3':
                break
            else:
                print(Fore.RED + "Invalid choice. Please choose again.")
    except ValueError as e:
        print(Fore.RED + f"Invalid Input data.")
    except Exception as e:
        print(Fore.RED + f"Invalid Input data.")
    except KeyboardInterrupt:
        print(Fore.RED + "Program interrupted by the user.")
        main()

def print_menu_main():
    table = PrettyTable()
    table.field_names = ["Number", "Option"]
    table.add_row(["1.", "Login"])
    table.add_row(["2.", "Register"])
    table.add_row(["3.", "Exit"])

    print(Fore.YELLOW + "Welcome to Perusahaan Reytop! 💻")
    print(table)
    print(Style.RESET_ALL) 

def login_menu(shop):
    print(Fore.YELLOW + "Login Menu")
    role = input("Enter your role (Admin/Customer): ").capitalize()

    if role == 'Admin':
        try:
            admin_actions(shop)
        except ValueError as e:
            print(Fore.RED + f"Invalid Input data.")
        except KeyboardInterrupt:
            print(Fore.RED + "Program interrupted by the user.")
        except Exception as e:
            print(Fore.RED + f"Invalid Input data.")
    elif role == 'Customer':
        try:
            customer_actions(shop)
        except ValueError as e:
            print(Fore.RED + f"Invalid Input data.")
        except KeyboardInterrupt:
            print(Fore.RED + "Program interrupted by the user.")
        except Exception as e:
            print(Fore.RED + f"Invalid Input data.")
    else:
        print(Fore.RED + "Invalid role. Please choose 'Admin' or 'Customer'.")

def register_menu(shop):
    print(Fore.YELLOW + "Register Menu")
    role = input("Enter your role (Admin/Customer): ").capitalize()
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if role == 'Admin':
        jobdesk = input("Enter your jobdesk: ")
        try:
            shop.add_new_admin(username, password, jobdesk)
        except ValueError as e:
            print(Fore.RED + f"Invalid Input data.")
    elif role == 'Customer':
        email = input("Enter your email: ")
        nohp = input("Enter your phone number: ")
        try:
            shop.add_new_customer(username, password, email, nohp)
        except ValueError as e:
            print(Fore.RED + f"Invalid Input data.")
        except KeyboardInterrupt:
            print(Fore.RED + "Program interrupted by the user.")
        except Exception as e:
            print(Fore.RED + f"Invalid Input data.")
    else:
        print(Fore.RED + "Invalid role. Please choose 'Admin' or 'Customer'.")


if __name__ == "__main__":
    main()
