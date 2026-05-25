"""
Controllers - Yestion Task Manager
Mengelola alur logika antara Model dan View (Controller layer dalam MVC)
"""

from models import Project, Task
import views


def _get_projects_map():
    """Helper: mapping project_id -> project_name"""
    return {p.id: p.name for p in Project.get_all()}


# ══════════════════════════════════════════════════════════════
#  PROJECT CONTROLLER (UC02)
# ══════════════════════════════════════════════════════════════

class ProjectController:

    @staticmethod
    def create():
        """UC02.1: Menambah Proyek"""
        name, desc = views.show_project_form()
        if not name:
            views.print_error("Nama proyek tidak boleh kosong!")
            views.press_enter()
            return
        project = Project.create(name, desc)
        views.print_success(f"Proyek \"{project.name}\" berhasil dibuat! (ID: {project.id})")
        views.press_enter()

    @staticmethod
    def list_all():
        """UC02.4: Melihat Daftar Proyek"""
        projects = Project.get_all()
        views.show_project_list(projects)
        views.press_enter()

    @staticmethod
    def update():
        """UC02.2: Mengubah Detail Proyek"""
        projects = Project.get_all()
        views.show_project_list(projects)
        if not projects:
            views.press_enter()
            return

        pid = views.ask_project_id()
        project = Project.get_by_id(pid)
        if not project:
            views.print_error("Proyek tidak ditemukan.")
            views.press_enter()
            return

        name, desc = views.show_project_edit_form(project)
        updated = Project.update(pid, name=name, description=desc)
        if updated:
            views.print_success(f"Proyek \"{updated.name}\" berhasil diperbarui!")
        else:
            views.print_error("Gagal memperbarui proyek.")
        views.press_enter()

    @staticmethod
    def delete():
        """UC02.3: Menghapus Proyek"""
        projects = Project.get_all()
        views.show_project_list(projects)
        if not projects:
            views.press_enter()
            return

        pid = views.ask_project_id()
        project = Project.get_by_id(pid)
        if not project:
            views.print_error("Proyek tidak ditemukan.")
            views.press_enter()
            return

        if views.show_delete_confirmation("Proyek", project.name):
            if Project.delete(pid):
                views.print_success(
                    f"Proyek \"{project.name}\" dan seluruh tugasnya berhasil dihapus."
                )
            else:
                views.print_error("Gagal menghapus proyek.")
        else:
            views.print_info("Penghapusan dibatalkan.")
        views.press_enter()


# ══════════════════════════════════════════════════════════════
#  TASK CONTROLLER (UC03 - UC06)
# ══════════════════════════════════════════════════════════════

class TaskController:

    @staticmethod
    def create():
        """UC03: Membuat Tugas (+ UC03.1 include, UC03.2 extend)"""
        projects = Project.get_all()
        data = views.show_task_form(projects)
        if not data:
            views.press_enter()
            return

        # Validasi: proyek harus ada (UC03.1)
        project = Project.get_by_id(data["project_id"])
        if not project:
            views.print_error("Proyek tidak ditemukan.")
            views.press_enter()
            return

        task = Task.create(
            name=data["name"],
            project_id=data["project_id"],
            priority=data["priority"],
            due_date=data["due_date"],
            google_drive_url=data["google_drive_url"],
        )
        views.print_success(
            f"Tugas \"{task.name}\" berhasil ditambahkan ke proyek \"{project.name}\"! "
            f"(ID: {task.id})"
        )
        views.press_enter()

    @staticmethod
    def list_by_project():
        """Lihat tugas berdasarkan proyek"""
        projects = Project.get_all()
        views.show_project_list(projects)
        if not projects:
            views.press_enter()
            return

        pid = views.ask_project_id()
        project = Project.get_by_id(pid)
        if not project:
            views.print_error("Proyek tidak ditemukan.")
            views.press_enter()
            return

        tasks = Task.get_by_project(pid)
        views.print_subheader(f"Tugas dalam Proyek: {project.name}")
        views.show_task_list(tasks, _get_projects_map())
        views.press_enter()

    @staticmethod
    def update():
        """UC04: Memodifikasi Tugas"""
        tasks = Task.get_all()
        views.show_task_list(tasks, _get_projects_map())
        if not tasks:
            views.press_enter()
            return

        tid = views.ask_task_id()
        task = Task.get_by_id(tid)
        if not task:
            views.print_error("Tugas tidak ditemukan.")
            views.press_enter()
            return

        updates = views.show_task_edit_form(task)
        # Hapus key yang None agar tidak overwrite
        updates = {k: v for k, v in updates.items() if v is not None}
        if updates:
            updated = Task.update(tid, **updates)
            if updated:
                views.print_success(f"Tugas \"{updated.name}\" berhasil diperbarui!")
            else:
                views.print_error("Gagal memperbarui tugas.")
        else:
            views.print_info("Tidak ada perubahan.")
        views.press_enter()

    @staticmethod
    def delete():
        """UC05: Menghapus Tugas"""
        tasks = Task.get_all()
        views.show_task_list(tasks, _get_projects_map())
        if not tasks:
            views.press_enter()
            return

        tid = views.ask_task_id()
        task = Task.get_by_id(tid)
        if not task:
            views.print_error("Tugas tidak ditemukan.")
            views.press_enter()
            return

        if views.show_delete_confirmation("Tugas", task.name):
            if Task.delete(tid):
                views.print_success(f"Tugas \"{task.name}\" berhasil dihapus.")
            else:
                views.print_error("Gagal menghapus tugas.")
        else:
            views.print_info("Penghapusan dibatalkan.")
        views.press_enter()

    @staticmethod
    def change_status():
        """UC06: Mengubah Status Tugas"""
        tasks = Task.get_all()
        views.show_task_list(tasks, _get_projects_map())
        if not tasks:
            views.press_enter()
            return

        tid = views.ask_task_id()
        task = Task.get_by_id(tid)
        if not task:
            views.print_error("Tugas tidak ditemukan.")
            views.press_enter()
            return

        new_status = views.show_status_change(task)
        if new_status and new_status != task.status:
            updated = Task.update(tid, status=new_status)
            if updated:
                views.print_success(
                    f"Status \"{updated.name}\" diubah: {task.status} → {new_status}"
                )
            else:
                views.print_error("Gagal mengubah status.")
        elif new_status == task.status:
            views.print_info("Status tidak berubah.")
        else:
            views.print_error("Pilihan tidak valid.")
        views.press_enter()


# ══════════════════════════════════════════════════════════════
#  SEARCH CONTROLLER (UC07)
# ══════════════════════════════════════════════════════════════

class SearchController:

    @staticmethod
    def by_keyword():
        """UC07.1: Mencari Berdasarkan Keyword"""
        keyword = views.ask_search_keyword()
        if not keyword:
            views.print_error("Keyword tidak boleh kosong.")
            views.press_enter()
            return
        tasks = Task.search_by_keyword(keyword)
        views.print_subheader(f"Hasil pencarian: \"{keyword}\"")
        views.show_task_list(tasks, _get_projects_map())
        views.press_enter()

    @staticmethod
    def by_due_date():
        """UC07.2: Filter Berdasarkan Due Date"""
        date_str = views.ask_filter_due_date()
        if not date_str:
            views.print_error("Tanggal tidak boleh kosong.")
            views.press_enter()
            return
        tasks = Task.filter_by_due_date(date_str)
        views.print_subheader(f"Tugas dengan deadline: {date_str}")
        views.show_task_list(tasks, _get_projects_map())
        views.press_enter()

    @staticmethod
    def by_priority():
        """UC07.3: Filter Berdasarkan Prioritas"""
        priority = views.ask_filter_priority()
        if not priority:
            views.print_error("Pilihan tidak valid.")
            views.press_enter()
            return
        tasks = Task.filter_by_priority(priority)
        views.print_subheader(f"Tugas prioritas: {priority}")
        views.show_task_list(tasks, _get_projects_map())
        views.press_enter()


# ══════════════════════════════════════════════════════════════
#  NOTIFICATION CONTROLLER (UC08)
# ══════════════════════════════════════════════════════════════

class NotificationController:

    @staticmethod
    def check_deadlines():
        """UC08 + UC11.2: Peringatan deadline via terminal"""
        tasks = Task.get_near_deadline(days=3)
        views.show_deadline_warnings(tasks, _get_projects_map())
        views.press_enter()

    @staticmethod
    def login_warning():
        """UC11.2: Notifikasi saat login/masuk aplikasi"""
        tasks = Task.get_near_deadline(days=3)
        if tasks:
            pmap = _get_projects_map()
            print()
            views.print_warning(f"⏰ {len(tasks)} tugas mendekati deadline!")
            for t in tasks:
                proj = pmap.get(t.project_id, "???")
                print(f"     • {t.name} ({proj}) — deadline {t.due_date}")
            print()
