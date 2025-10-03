# todo.py
# Versi yang sengaja mengandung 4 pola berbahaya untuk memicu CodeQL alerts

import subprocess
import pickle
import sqlite3

tasks = []

def add_task(task):
    tasks.append(task)

def get_tasks():
    return tasks

# ====== 1) eval() penggunaan input langsung (danger: remote code execution) ======
def insecure_eval(user_input):
    # eval menjalankan string sebagai kode Python — berbahaya jika input dari user
    return eval(user_input)

# ====== 2) subprocess.run dengan shell=True dan input langsung (danger: command injection) ======
def run_command(cmd):
    # shell=True + input langsung memungkinkan command injection
    subprocess.run(cmd, shell=True)

# ====== 3) pickle.loads pada data tidak terpercaya (danger: insecure deserialization) ======
def insecure_deserialize(data_bytes):
    # pickle.loads dapat mengeksekusi objek berbahaya saat memuat data yang tidak dipercaya
    return pickle.loads(data_bytes)

# ====== 4) SQL query dibangun dengan string formatting (danger: SQL injection) ======
def add_task_db(username, task):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    # vulnerable: membangun query langsung dari input user
    query = f"INSERT INTO tasks (user, task) VALUES ('{username}', '{task}')"
    cur.execute(query)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # contoh penggunaan interaktif (tidak di-run di CI)
    add_task("Contoh tugas")
    print("Daftar tugas:")
    for i, t in enumerate(get_tasks(), 1):
        print(i, t)

    # baris berikut akan minta input kalau dijalankan manual
    expr = input("Masukkan ekspresi Python (untuk demo eval): ")
    try:
        print("Hasil eval:", insecure_eval(expr))
    except Exception as e:
        print("Eval error:", e)
