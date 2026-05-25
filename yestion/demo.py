#!/usr/bin/env python3
"""
Demo script: Seed data contoh dan tampilkan fitur-fitur Yestion
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from models import Project, Task, Database
from datetime import datetime, timedelta
import views


def seed_data():
    """Isi data contoh"""
    # Reset database
    if os.path.exists(os.path.join(os.path.dirname(__file__), "data.json")):
        os.remove(os.path.join(os.path.dirname(__file__), "data.json"))

    # Buat proyek
    p1 = Project.create("Jaringan Komputer", "Tugas Progjar Semester 4")
    p2 = Project.create("Matematika Diskrit", "Proyek Matdis")
    p3 = Project.create("PPL - Yestion", "Final Project PPL Kelas B")

    # Buat tugas dengan berbagai status, prioritas, dan deadline
    today = datetime.now()

    Task.create("TCP File Server", p1.id, "High",
                (today + timedelta(days=2)).strftime("%Y-%m-%d"),
                "https://drive.google.com/folder/tcp-server")
    Task.create("UDP Parser RFC 768", p1.id, "Medium",
                (today + timedelta(days=7)).strftime("%Y-%m-%d"))
    Task.create("HTTP BFS Crawler", p1.id, "Low",
                (today + timedelta(days=14)).strftime("%Y-%m-%d"))

    Task.create("Latihan Soal Graf", p2.id, "High",
                (today + timedelta(days=1)).strftime("%Y-%m-%d"))
    Task.create("Resume Kombinatorika", p2.id, "Medium",
                (today + timedelta(days=10)).strftime("%Y-%m-%d"))

    Task.create("Use Case Diagram", p3.id, "High",
                (today + timedelta(days=3)).strftime("%Y-%m-%d"),
                "https://drive.google.com/folder/ppl-ucd")
    Task.create("Activity Diagram", p3.id, "Medium",
                (today + timedelta(days=5)).strftime("%Y-%m-%d"))
    Task.create("Laporan Final", p3.id, "High",
                (today + timedelta(days=8)).strftime("%Y-%m-%d"))

    # Ubah beberapa status
    Task.update(2, status="In Progress")
    Task.update(6, status="Completed")

    return p1, p2, p3


def demo():
    print("\n" + "=" * 60)
    print("  DEMO: Yestion Task Manager (MVC Pattern)")
    print("=" * 60)

    print("\n[1] Seeding data contoh...")
    p1, p2, p3 = seed_data()
    views.print_success("3 proyek dan 8 tugas berhasil dibuat.")

    # Demo: Lihat daftar proyek (UC02.4)
    print("\n" + "-" * 60)
    print("[2] UC02.4 - Melihat Daftar Proyek")
    projects = Project.get_all()
    views.show_project_list(projects)

    # Demo: Lihat semua tugas
    print("\n" + "-" * 60)
    print("[3] Semua Tugas dalam Sistem")
    tasks = Task.get_all()
    pmap = {p.id: p.name for p in projects}
    views.show_task_list(tasks, pmap)

    # Demo: Search keyword (UC07.1)
    print("\n" + "-" * 60)
    print("[4] UC07.1 - Pencarian keyword: 'TCP'")
    results = Task.search_by_keyword("TCP")
    views.show_task_list(results, pmap)

    # Demo: Filter prioritas (UC07.3)
    print("\n" + "-" * 60)
    print("[5] UC07.3 - Filter prioritas: High")
    results = Task.filter_by_priority("High")
    views.show_task_list(results, pmap)

    # Demo: Deadline warning (UC08)
    print("\n" + "-" * 60)
    print("[6] UC08 - Peringatan Deadline (≤3 hari)")
    near = Task.get_near_deadline(days=3)
    views.show_deadline_warnings(near, pmap)

    # Demo: Ubah status (UC06)
    print("\n" + "-" * 60)
    print("[7] UC06 - Mengubah Status 'Latihan Soal Graf' → Completed")
    Task.update(4, status="Completed")
    task = Task.get_by_id(4)
    views.print_success(f"Status \"{task.name}\" → {task.status}")

    print("\n" + "=" * 60)
    print("  Demo selesai! Jalankan `python3 main.py` untuk mode interaktif.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    demo()
