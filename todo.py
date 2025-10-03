import os
import subprocess
import pickle
import sqlite3

tasks = []

def add_task(task):
    tasks.append(task)

def get_tasks():
    return tasks

# ===== 1) eval (remote code execution) =====
def insecure_eval(user_input):
    # WARNING: menjalankan string sebagai kode python
    return eval(user_input)

# ===== 2) subprocess.run(..., shell=True) (command injection) =====
def run_command(cmd):
    # WARNING: shell=True + input raw => command injection risk
    subprocess.run(cmd, shell=True)

# ===== 3) pickle.loads (insecure deserialization) =====
def insecure_deserialize(data_bytes):
    # WARNING: loading pickle dari sumber tak dipercaya bisa mengeksekusi kode
    return pickle.loads(data_bytes)

# ===== 4) SQL built via f-string (SQL injection) =====
def add_task_db(username, task):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    # WARNING: memasukkan input langsung ke query -> SQL injection risk
    query = f"INSERT INTO tasks (user, task) VALUES ('{username}', '{task}')"
    cur.execute(query)
    conn.commit()
    conn.close()

# deteksi environment CI (GitHub Actions)
def interactive_mode():
    # GitHub Actions sets GITHUB_ACTIONS=true for workflows
    return os.getenv("GITHUB_ACTIONS") != "true"

if __name__ == "__main__":
    # selalu jalan (non-interaktif)
    add_task("Belajar Python")
    add_task("Mengerjakan Tugas")
    print("Daftar tugas (non-interaktif):")
    for i, t in enumerate(get_tasks(), 1):
        print(i, t)

    # Bagian interaktif hanya untuk penggunaan lokal (tidak dijalankan di CI)
    if interactive_mode():
        # LOCAL: demo berbahaya (jangan gunakan di production)
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

        # contoh deserialize (tidak dianjurkan)
        # contoh panggil add_task_db (jangan gunakan input mentah)
    else:
        # Di CI: jangan minta input
        print("CI detected — skipping interactive input.")
