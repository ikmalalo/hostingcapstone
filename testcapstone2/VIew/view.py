from prettytable import PrettyTable
from colorama import Fore

def display_menu_and_stock(barang, order_type="pembelian"):
    from prettytable import PrettyTable
    from colorama import Fore

    table = PrettyTable()
    table.field_names = [Fore.BLUE + "id_barang", Fore.BLUE + "nama_barang", Fore.BLUE + "harga", Fore.BLUE + "Stock"]

    for laptop in barang:
        try:
            id_barang = laptop.get('id_barang', 'ID not available')
            name = laptop['nama_barang']
            price = laptop.get('harga', 'Price not available')
            stock = laptop.get('stock', 'Stock not available')

            if order_type == "penyewaan":
                price /= 50

            table.add_row([Fore.BLUE + str(id_barang), Fore.BLUE + name, Fore.BLUE + str(price), Fore.BLUE + str(stock)])
        except KeyError as e:
            print(f"Error: Missing key in laptop data - {e}")

    print(table.get_string().capitalize())

def display_pembelian_history(shop):
    try:
        connection = shop.connect_to_database()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT pembelian.id_pembelian, pembelian.tanggal_pembelian, pembelian.total_harga, 
                SUM(transaksi.total_barang) AS total_barang
                FROM pembelian
                INNER JOIN transaksi ON pembelian.id_pembelian = transaksi.id_pembelian
                GROUP BY pembelian.id_pembelian;
            """)
            pembelian_history = cursor.fetchall()
            connection.close()
            if pembelian_history:
                table = PrettyTable()
                table.field_names = ["id_pembelian", "tanggal_pembelian", "total_harga", "total_barang"]
                for order in pembelian_history:
                    id_pembelian = order["id_pembelian"]
                    tanggal_pembelian = order["tanggal_pembelian"]
                    total_harga = order["total_harga"]
                    total_barang = order["total_barang"]
                    table.add_row([id_pembelian, tanggal_pembelian, total_harga, total_barang])
                print(table)
            else:
                print(Fore.YELLOW + "No pembelian history found.")
        else:
            print(Fore.RED + "Failed to connect to database")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")

def display_penyewaan_history(shop):
    try:
        connection = shop.connect_to_database()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT penyewaan.total_harga, 
                SUM(transaksi.total_barang) AS total_barang
                FROM penyewaan
                INNER JOIN transaksi ON penyewaan.id_penyewaan = transaksi.id_penyewaan
                GROUP BY penyewaan.id_penyewaan;
            """)
            penyewaan_history = cursor.fetchall()
            connection.close()
            if penyewaan_history:
                table = PrettyTable()
                table.field_names = ["id_penyewaan", "tanggal_penyewaan", "total_harga", "total_barang"]
                for order in penyewaan_history:
                    id_penyewaan = order["id_penyewaan"]
                    tanggal_penyewaan = order["tanggal_penyewaan"]
                    total_harga = order["total_harga"]
                    total_barang = order["total_barang"]
                    table.add_row([id_penyewaan, tanggal_penyewaan, total_harga, total_barang])
                print(table)
            else:
                print(Fore.YELLOW + "No penyewaan history found.")
        else:
            print(Fore.RED + "Failed to connect to database")
    except Exception as e:
        print(Fore.RED + f"An error occurred: {str(e)}")

# def display_menu_by_ascending(shop):
#     try:
#         connection = shop.connect_to_database()
#         if connection:
#             cursor = connection.cursor(dictionary=True)
#             cursor.execute("SELECT * FROM barang ORDER BY harga ASC;")
#             sorted_menu = cursor.fetchall()
#             connection.close()
#             return sorted_menu
#         else:
#             print("Failed to connect to database")
#             return []
#     except Exception as e:
#         print(Fore.RED + f"An error occurred: {str(e)}")
#         return []

# def display_menu_by_descending(shop):
#     try:
#         connection = shop.connect_to_database()
#         if connection:
#             cursor = connection.cursor(dictionary=True)
#             cursor.execute("SELECT * FROM barang ORDER BY harga DESC;")
#             sorted_menu = cursor.fetchall()
#             connection.close()
#             return sorted_menu
#         else:
#             print("Failed to connect to database")
#             return []
#     except Exception as e:
#         print(Fore.RED + f"An error occurred: {str(e)}")
#         return []
    

# def display_order_history(shop):
#     try:
#         connection = shop.connect_to_database()
#         if connection:
#             cursor = connection.cursor(dictionary=True)
#             cursor.execute("""
#                 SELECT pembelian.id_pembelian, pembelian.tanggal_pembelian, pembelian.total_harga, 
#                 SUM(transaksi.total_barang) AS total_barang
#                 FROM pembelian
#                 INNER JOIN transaksi ON pembelian.id_pembelian = transaksi.id_pembelian
#                 GROUP BY pembelian.id_pembelian;
#             """)
#             order_history = cursor.fetchall()
#             connection.close()
#             if order_history:
#                 table = PrettyTable()
#                 table.field_names = ["id_pembelian", "tanggal_pembelian", "total_harga", "total_barang"]
#                 for order in order_history:
#                     id_pembelian = order["id_pembelian"]
#                     tanggal_pembelian = order["tanggal_pembelian"]
#                     total_harga = order["total_harga"]
#                     total_barang = order["total_barang"]
#                     table.add_row([id_pembelian, tanggal_pembelian, total_harga, total_barang])
#                 print(table)
#             else:
#                 print(Fore.YELLOW + "No order history found.")
#         else:
#             print(Fore.RED + "Failed to connect to database")
#     except Exception as e:
#         print(Fore.RED + f"An error occurred: {str(e)}")







