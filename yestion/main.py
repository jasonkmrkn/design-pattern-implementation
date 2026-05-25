#!/usr/bin/env python3
"""
Yestion Task Manager - Main Application
Implementasi MVC Pattern untuk CLI

Struktur MVC:
  ┌─────────────────────────────────────────────────────┐
  │  main.py          → Router / Entry Point            │
  │  controllers.py   → Controller (logika alur)        │
  │  views.py         → View (tampilan terminal)        │
  │  models.py        → Model (data + business logic)   │
  │  data.json        → Simulasi Database               │
  └─────────────────────────────────────────────────────┘

Use Case Coverage:
  UC01  Registrasi           → (disimulasikan sebagai auto-login)
  UC02  Manajemen Proyek     → ProjectController
  UC03  Membuat Tugas        → TaskController.create
  UC04  Memodifikasi Tugas   → TaskController.update
  UC05  Menghapus Tugas      → TaskController.delete
  UC06  Mengubah Status      → TaskController.change_status
  UC07  Pencarian & Filter   → SearchController
  UC08  Peringatan Deadline  → NotificationController
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from controllers import (
    ProjectController,
    TaskController,
    SearchController,
    NotificationController,
)
import views


def handle_project_menu():
    while True:
        choice = views.show_project_menu()
        if choice == "1":
            ProjectController.create()
        elif choice == "2":
            ProjectController.list_all()
        elif choice == "3":
            ProjectController.update()
        elif choice == "4":
            ProjectController.delete()
        elif choice == "0":
            break


def handle_task_menu():
    while True:
        choice = views.show_task_menu()
        if choice == "1":
            TaskController.create()
        elif choice == "2":
            TaskController.list_by_project()
        elif choice == "3":
            TaskController.update()
        elif choice == "4":
            TaskController.delete()
        elif choice == "5":
            TaskController.change_status()
        elif choice == "0":
            break


def handle_search_menu():
    while True:
        choice = views.show_search_menu()
        if choice == "1":
            SearchController.by_keyword()
        elif choice == "2":
            SearchController.by_due_date()
        elif choice == "3":
            SearchController.by_priority()
        elif choice == "0":
            break


def main():
    # UC11.2: Peringatan deadline saat buka aplikasi
    NotificationController.login_warning()

    while True:
        choice = views.show_main_menu()
        if choice == "1":
            handle_project_menu()
        elif choice == "2":
            handle_task_menu()
        elif choice == "3":
            handle_search_menu()
        elif choice == "4":
            NotificationController.check_deadlines()
        elif choice == "0":
            views.clear_screen()
            print("\n  Terima kasih telah menggunakan Yestion! 👋\n")
            break


if __name__ == "__main__":
    main()
