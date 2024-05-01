from prettytable import PrettyTable
from colorama import Fore


def display_menu_and_stock(menu, order_type="pembelian", limit=20, start_index=0):
    try:
        if menu:
            print("Menu and Stock:")
            table = PrettyTable()
            table.field_names = ["ID", "Nama Barang", "Harga", "Stock", "Spek"]
            if start_index == 0:
                items_to_display = menu[:limit]
            else:
                items_to_display = menu[start_index:start_index+limit]
            for item in items_to_display:
                if order_type == "penyewaan":
                    harga = int(item['harga']) // 50
                else:
                    harga = item['harga']
                table.add_row([item['id_barang'], item['nama_barang'], harga, item['stock'], item['spek']])
            print(table)
            if len(menu) > limit + start_index:
                choice = input("Input '0' to view more items or press any other key to continue: ")
                if choice == '0':
                    display_menu_and_stock(menu, order_type, limit, start_index+limit)
        else:
            print(Fore.YELLOW + "No items found.")
    except Exception as e:
        print(Fore.RED + f"Invalid Input data.")

def display_pembelian_history(shop):
    try:
        connection = shop.connect_to_database()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT pembelian.id_pembelian, pembelian.tanggal_pembelian, pembelian.total_harga, 
                SUM(transaksi.total_barang) AS total_barang
                FROM pembelian
                INNER JOIN transaksi ON pembelian.id_pembelian = transaksi.id_transaksi
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
                    total_barang = int(order["total_barang"])
                    table.add_row([id_pembelian, tanggal_pembelian, total_harga, total_barang])
                print(table)
            else:
                print(Fore.YELLOW + "No pembelian history found.")
        else:
            print(Fore.RED + "Failed to connect to database")
    except Exception as e:
        print(Fore.RED + f"Invalid Input data.")

def display_penyewaan_history(shop):
    try:
        connection = shop.connect_to_database()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT penyewaan.id_penyewaan, penyewaan.tanggal_minjam, penyewaan.jaminan, penyewaan.tanggal_kembali, penyewaan.total_harga, 
                transaksi.total_barang AS total_barang
                FROM penyewaan
                INNER JOIN transaksi ON penyewaan.id_transaksi = transaksi.id_transaksi
            """)
            penyewaan_history = cursor.fetchall()
            connection.close()
            if penyewaan_history:
                table = PrettyTable()
                table.field_names = ["id_penyewaan", "tanggal_minjam", "tanggal_kembali", "jaminan", "total_harga", "total_barang"]
                for order in penyewaan_history:
                    id_penyewaan = order["id_penyewaan"]
                    tanggal_minjam = order["tanggal_minjam"]
                    jaminan = order["jaminan"]
                    tanggal_kembali = (order["tanggal_kembali"])
                    total_harga = order["total_harga"]
                    total_barang = int(order["total_barang"])
                    table.add_row([id_penyewaan, tanggal_minjam, tanggal_kembali, jaminan, total_harga, total_barang])  
                print(table)
            else:
                print(Fore.YELLOW + "No penyewaan history found.")
        else:
            print(Fore.RED + "Failed to connect to database")
    except Exception as e:
        print(Fore.RED + f"Invalid Input data.")

