
import os
import subprocess
import pickle
import sqlite3

tasks = []

def add_task(task):
    tasks.append(task)

def get_tasks():
    return tasks

# ====== 1) eval (danger: remote code execution) ======
def insecure_eval(user_input):
    return eval(user_input)   # WARNING: berbahaya

# ====== 2) subprocess.run dengan shell=True (danger: command injection) ======
def run_command(cmd):
    subprocess.run(cmd, shell=True)   # WARNING: berbahaya jika cmd berasal dari user

# ====== 3) pickle.loads (danger: insecure deserialization) ======
def insecure_deserialize(data_bytes):
    return pickle.loads(data_bytes)   # WARNING: berbahaya jika data tidak dipercaya

# ====== 4) SQL dibuat dengan string formatting (danger: SQL injection) ======
def add_task_db(username, task):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    # vulnerable: membangun query langsung dari input user
    query = f"INSERT INTO tasks (user, task) VALUES ('{username}', '{task}')"
    cur.execute(query)
    conn.commit()
    conn.close()

def interactive_mode():
    # GitHub Actions sets GITHUB_ACTIONS=true when running workflows
    return os.getenv("GITHUB_ACTIONS") != "true"

if __name__ == "__main__":
    # Contoh operasi non-interaktif (selalu jalan)
    add_task("Belajar Python")
    add_task("Mengerjakan Tugas")
    print("Daftar tugas (non-interaktif):")
    for i, t in enumerate(get_tasks(), 1):
        print(i, t)

    # Bagian interaktif hanya akan dieksekusi kalau tidak di CI
    if interactive_mode():
        # Lokal: aman untuk demo, tetapi potensi berbahaya tergantung input
        expr = input("Masukkan ekspresi Python (contoh eval): ")
        try:
            print("Eval =>", insecure_eval(expr))
        except Exception as e:
            print("Eval error:", e)

        cmd = input("Masukkan perintah shell untuk dijalankan (contoh): ")
        try:
            run_command(cmd)
        except Exception as e:
            print("Run command error:", e)

        # contoh deserialize (jangan gunakan data tak dipercaya)
        # dan contoh panggil add_task_db (jangan gunakan input mentah)
    else:
        # Di CI: skip bagian interaktif agar workflow tidak hang/gagal
        print("CI detected — skipping interactive input.")
