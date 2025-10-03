# file: todo.py

def tampilkan_menu():
    print("\n=== TO-DO LIST ===")
    print("1. Tambah tugas")
    print("2. Lihat semua tugas")
    print("3. Hapus tugas")
    print("4. Keluar")

def tambah_tugas(tugas_list):
    tugas = input("Masukkan tugas baru: ")
    tugas_list.append(tugas)
    print(f"Tugas '{tugas}' berhasil ditambahkan!")

def lihat_tugas(tugas_list):
    if not tugas_list:
        print("Belum ada tugas.")
    else:
        print("\nDaftar tugas:")
        for i, t in enumerate(tugas_list, start=1):
            print(f"{i}. {t}")

def hapus_tugas(tugas_list):
    lihat_tugas(tugas_list)
    if tugas_list:
        try:
            nomor = int(input("Masukkan nomor tugas yang ingin dihapus: "))
            if 1 <= nomor <= len(tugas_list):
                terhapus = tugas_list.pop(nomor - 1)
                print(f"Tugas '{terhapus}' berhasil dihapus!")
            else:
                print("Nomor tidak valid.")
        except ValueError:
            print("Input harus angka.")

if __name__ == "__main__":
    daftar_tugas = []
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (1-4): ")

        if pilihan == "1":
            tambah_tugas(daftar_tugas)
        elif pilihan == "2":
            lihat_tugas(daftar_tugas)
        elif pilihan == "3":
            hapus_tugas(daftar_tugas)
        elif pilihan == "4":
            print("Keluar dari program. Sampai jumpa!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")
