"""
Views - Yestion Task Manager
Mengelola tampilan terminal dan input pengguna (View layer dalam MVC)
"""

import os


# ══════════════════════════════════════════════════════════════
#  UTILITY DISPLAY
# ══════════════════════════════════════════════════════════════

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title):
    width = 60
    print()
    print("═" * width)
    print(f"  {title}")
    print("═" * width)


def print_subheader(title):
    print(f"\n── {title} ──")


def print_success(msg):
    print(f"\n  ✓ {msg}")


def print_error(msg):
    print(f"\n  ✗ {msg}")


def print_warning(msg):
    print(f"\n  ⚠ {msg}")


def print_info(msg):
    print(f"\n  ℹ {msg}")


def press_enter():
    input("\n  Tekan [Enter] untuk kembali...")


# ══════════════════════════════════════════════════════════════
#  MENU VIEWS
# ══════════════════════════════════════════════════════════════

def show_main_menu():
    clear_screen()
    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║         YESTION TASK MANAGER             ║")
    print("  ║     Kelola Tugas Kuliah Mahasiswa        ║")
    print("  ╚══════════════════════════════════════════╝")
    print()
    print("  [1] Manajemen Proyek")
    print("  [2] Manajemen Tugas")
    print("  [3] Pencarian & Filter Tugas")
    print("  [4] Peringatan Deadline")
    print("  [0] Keluar")
    print()
    return input("  Pilihan > ").strip()


def show_project_menu():
    clear_screen()
    print_header("MANAJEMEN PROYEK")
    print()
    print("  [1] Tambah Proyek        (UC02.1)")
    print("  [2] Lihat Daftar Proyek  (UC02.4)")
    print("  [3] Ubah Detail Proyek   (UC02.2)")
    print("  [4] Hapus Proyek         (UC02.3)")
    print("  [0] Kembali")
    print()
    return input("  Pilihan > ").strip()


def show_task_menu():
    clear_screen()
    print_header("MANAJEMEN TUGAS")
    print()
    print("  [1] Membuat Tugas         (UC03)")
    print("  [2] Lihat Tugas Proyek")
    print("  [3] Memodifikasi Tugas    (UC04)")
    print("  [4] Menghapus Tugas       (UC05)")
    print("  [5] Mengubah Status Tugas (UC06)")
    print("  [0] Kembali")
    print()
    return input("  Pilihan > ").strip()


def show_search_menu():
    clear_screen()
    print_header("PENCARIAN & FILTER TUGAS (UC07)")
    print()
    print("  [1] Cari berdasarkan Keyword   (UC07.1)")
    print("  [2] Filter berdasarkan Due Date (UC07.2)")
    print("  [3] Filter berdasarkan Prioritas(UC07.3)")
    print("  [0] Kembali")
    print()
    return input("  Pilihan > ").strip()


# ══════════════════════════════════════════════════════════════
#  PROJECT VIEWS
# ══════════════════════════════════════════════════════════════

def show_project_form():
    """Form pembuatan proyek baru (UC02.1)"""
    print_subheader("Tambah Proyek Baru")
    name = input("  Nama Proyek    : ").strip()
    desc = input("  Deskripsi      : ").strip()
    return name, desc


def show_project_list(projects):
    """Menampilkan daftar proyek (UC02.4)"""
    print_subheader("Daftar Proyek")
    if not projects:
        print_info("Belum ada proyek yang dibuat.")
        return

    print(f"\n  {'ID':<5} {'Nama Proyek':<25} {'Deskripsi':<25} {'Dibuat'}")
    print("  " + "─" * 75)
    for p in projects:
        print(f"  {p.id:<5} {p.name:<25} {p.description[:25]:<25} {p.created_at}")


def show_project_edit_form(project):
    """Form edit proyek (UC02.2)"""
    print_subheader(f"Ubah Proyek: {project.name}")
    print(f"  (Kosongkan untuk mempertahankan nilai saat ini)")
    name = input(f"  Nama baru     [{project.name}]: ").strip()
    desc = input(f"  Deskripsi baru [{project.description}]: ").strip()
    return name or None, desc or None


def show_delete_confirmation(entity_type, name):
    """Dialog konfirmasi penghapusan"""
    print_warning(f"Anda akan menghapus {entity_type}: \"{name}\"")
    confirm = input("  Yakin hapus? (y/n) > ").strip().lower()
    return confirm == "y"


def ask_project_id():
    """Input ID proyek"""
    try:
        return int(input("  Masukkan ID Proyek > ").strip())
    except ValueError:
        return None


# ══════════════════════════════════════════════════════════════
#  TASK VIEWS
# ══════════════════════════════════════════════════════════════

def show_task_form(projects):
    """Form pembuatan tugas baru (UC03)"""
    print_subheader("Membuat Tugas Baru")

    # UC03.1: Memilih Proyek (include)
    if not projects:
        print_error("Tidak ada proyek. Buat proyek terlebih dahulu.")
        return None

    print("\n  Proyek tersedia:")
    for p in projects:
        print(f"    [{p.id}] {p.name}")

    try:
        project_id = int(input("\n  Pilih ID Proyek > ").strip())
    except ValueError:
        print_error("ID tidak valid.")
        return None

    name = input("  Nama Tugas     : ").strip()
    if not name:
        print_error("Nama tugas tidak boleh kosong.")
        return None

    # Prioritas
    print("  Prioritas: [1] Low  [2] Medium  [3] High")
    pri_map = {"1": "Low", "2": "Medium", "3": "High"}
    pri_choice = input("  Pilih prioritas (default: 2) > ").strip()
    priority = pri_map.get(pri_choice, "Medium")

    # Due Date
    due_date = input("  Due Date (YYYY-MM-DD, kosongkan jika belum ada) : ").strip()
    if due_date and len(due_date) != 10:
        print_warning("Format tanggal tidak sesuai. Due date tidak disimpan.")
        due_date = None

    # UC03.2: Menautkan Google Drive (extend)
    gdrive = input("  URL Google Drive (opsional) : ").strip()

    return {
        "name": name,
        "project_id": project_id,
        "priority": priority,
        "due_date": due_date or None,
        "google_drive_url": gdrive,
    }


def show_task_list(tasks, projects_map):
    """Menampilkan daftar tugas"""
    if not tasks:
        print_info("Tidak ada tugas ditemukan.")
        return

    # Priority color indicator
    pri_icon = {"Low": "○", "Medium": "◐", "High": "●"}
    status_icon = {"Not Completed": "□", "In Progress": "◧", "Completed": "■"}

    print(
        f"\n  {'ID':<4} {'Tugas':<22} {'Proyek':<15} {'Status':<16} "
        f"{'Prioritas':<10} {'Due Date':<12} {'GDrive'}"
    )
    print("  " + "─" * 95)
    for t in tasks:
        proj_name = projects_map.get(t.project_id, "???")
        si = status_icon.get(t.status, " ")
        pi = pri_icon.get(t.priority, " ")
        due = t.due_date or "-"
        gd = "✓" if t.google_drive_url else "-"
        print(
            f"  {t.id:<4} {t.name[:22]:<22} {proj_name[:15]:<15} "
            f"{si} {t.status:<13} {pi} {t.priority:<7} {due:<12} {gd}"
        )


def show_task_edit_form(task):
    """Form edit tugas (UC04)"""
    print_subheader(f"Memodifikasi Tugas: {task.name}")
    print(f"  (Kosongkan untuk mempertahankan nilai saat ini)")

    name = input(f"  Nama baru      [{task.name}]: ").strip()

    print(f"  Prioritas saat ini: {task.priority}")
    print("  Prioritas baru: [1] Low  [2] Medium  [3] High  [Enter] Tetap")
    pri_map = {"1": "Low", "2": "Medium", "3": "High"}
    pri_choice = input("  > ").strip()
    priority = pri_map.get(pri_choice)

    due_date = input(f"  Due Date baru  [{task.due_date or '-'}]: ").strip()

    gdrive = input(f"  URL GDrive baru [{task.google_drive_url or '-'}]: ").strip()

    return {
        "name": name or None,
        "priority": priority,
        "due_date": due_date or None,
        "google_drive_url": gdrive or None,
    }


def show_status_change(task):
    """Form ubah status tugas (UC06)"""
    print_subheader(f"Mengubah Status: {task.name}")
    print(f"  Status saat ini: {task.status}\n")

    statuses = ["Not Completed", "In Progress", "Completed"]
    for i, s in enumerate(statuses, 1):
        marker = " ◄" if s == task.status else ""
        print(f"    [{i}] {s}{marker}")

    try:
        choice = int(input("\n  Pilih status baru > ").strip())
        if 1 <= choice <= 3:
            return statuses[choice - 1]
    except ValueError:
        pass
    return None


def ask_task_id():
    """Input ID tugas"""
    try:
        return int(input("  Masukkan ID Tugas > ").strip())
    except ValueError:
        return None


# ══════════════════════════════════════════════════════════════
#  SEARCH VIEWS (UC07)
# ══════════════════════════════════════════════════════════════

def ask_search_keyword():
    print_subheader("Pencarian Berdasarkan Keyword (UC07.1)")
    return input("  Masukkan keyword > ").strip()


def ask_filter_due_date():
    print_subheader("Filter Berdasarkan Due Date (UC07.2)")
    return input("  Masukkan tanggal (YYYY-MM-DD) > ").strip()


def ask_filter_priority():
    print_subheader("Filter Berdasarkan Prioritas (UC07.3)")
    print("  [1] Low   [2] Medium   [3] High")
    pri_map = {"1": "Low", "2": "Medium", "3": "High"}
    choice = input("  Pilih > ").strip()
    return pri_map.get(choice)


# ══════════════════════════════════════════════════════════════
#  DEADLINE WARNING VIEW (UC08)
# ══════════════════════════════════════════════════════════════

def show_deadline_warnings(tasks, projects_map):
    """Menampilkan peringatan deadline (UC08, UC11.2)"""
    print_header("PERINGATAN DEADLINE")
    if not tasks:
        print_success("Tidak ada tugas yang mendekati deadline. Aman!")
        return

    print_warning(f"{len(tasks)} tugas mendekati deadline!\n")
    for t in tasks:
        proj_name = projects_map.get(t.project_id, "???")
        print(f"  ⏰  [{t.priority}] {t.name}")
        print(f"      Proyek: {proj_name}  |  Deadline: {t.due_date}  |  Status: {t.status}")
        print()
