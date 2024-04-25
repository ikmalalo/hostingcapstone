from Model.model import Admin, Customer, LaptopShop
from VIew.view import display_menu_and_stock
from Controller.controller import customer_actions, admin_actions
from prettytable import PrettyTable
from colorama import Fore, Style

def main():
    shop = LaptopShop()
    while True:
        print_menu_main()
        choice = input(Fore.BLUE + "Enter your role (admin/customer): ").lower()
        
        if choice == '1':
            admin_actions(shop)
        elif choice == '2':
            customer_actions(shop)
        elif choice == '3':
            break
        else:
            print("Invalid role. Please choose 'admin' or 'customer'.")
        
def print_menu_main():
    table = PrettyTable()
    table.field_names = ["Number", "Role"]
    table.add_row(["1.", Fore.BLUE + "🛠 Admin"])
    table.add_row(["2.", Fore.GREEN + "👨‍💻 Customer"])
    table.add_row(["3.", Fore.RED + "❌ Exit"])

    print(Fore.YELLOW + "Welcome to the Perusahaan Reytop !")
    print(table)
    print(Style.RESET_ALL) 

if __name__ == "__main__":
    main()
