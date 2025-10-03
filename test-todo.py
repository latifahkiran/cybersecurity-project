# test_todo.py
import todo

def test_add_task():
    todo.tasks.clear()  # pastikan kosong dulu
    todo.add_task("Belajar GitHub Actions")
    assert "Belajar GitHub Actions" in todo.get_tasks()

def test_get_tasks():
    todo.tasks.clear()
    todo.add_task("Mengerjakan Tugas")
    tasks = todo.get_tasks()
    assert len(tasks) == 1
    assert tasks[0] == "Mengerjakan Tugas"
