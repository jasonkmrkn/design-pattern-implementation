"""
Models - Yestion Task Manager
Mengelola data dan business logic (Model layer dalam MVC)
"""

import json
import os
from datetime import datetime, timedelta

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


class Database:
    """Simulasi database menggunakan JSON file"""

    @staticmethod
    def load():
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        return {"projects": [], "tasks": [], "next_project_id": 1, "next_task_id": 1}

    @staticmethod
    def save(data):
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2, default=str)


class Project:
    """Model untuk entitas Proyek"""

    def __init__(self, id=None, name="", description="", created_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return Project(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            created_at=data.get("created_at", ""),
        )

    # ---------- CRUD Operations ----------

    @staticmethod
    def create(name, description):
        db = Database.load()
        project = Project(
            id=db["next_project_id"], name=name, description=description
        )
        db["projects"].append(project.to_dict())
        db["next_project_id"] += 1
        Database.save(db)
        return project

    @staticmethod
    def get_all():
        db = Database.load()
        return [Project.from_dict(p) for p in db["projects"]]

    @staticmethod
    def get_by_id(project_id):
        db = Database.load()
        for p in db["projects"]:
            if p["id"] == project_id:
                return Project.from_dict(p)
        return None

    @staticmethod
    def update(project_id, name=None, description=None):
        db = Database.load()
        for p in db["projects"]:
            if p["id"] == project_id:
                if name is not None:
                    p["name"] = name
                if description is not None:
                    p["description"] = description
                Database.save(db)
                return Project.from_dict(p)
        return None

    @staticmethod
    def delete(project_id):
        db = Database.load()
        original_len = len(db["projects"])
        db["projects"] = [p for p in db["projects"] if p["id"] != project_id]
        # Cascade delete: hapus semua task terkait
        db["tasks"] = [t for t in db["tasks"] if t["project_id"] != project_id]
        Database.save(db)
        return len(db["projects"]) < original_len


class Task:
    """Model untuk entitas Tugas"""

    STATUSES = ["Not Completed", "In Progress", "Completed"]
    PRIORITIES = ["Low", "Medium", "High"]

    def __init__(
        self,
        id=None,
        name="",
        project_id=None,
        status="Not Completed",
        priority="Medium",
        due_date=None,
        google_drive_url="",
        created_at=None,
    ):
        self.id = id
        self.name = name
        self.project_id = project_id
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.google_drive_url = google_drive_url
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "project_id": self.project_id,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date,
            "google_drive_url": self.google_drive_url,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            id=data["id"],
            name=data["name"],
            project_id=data["project_id"],
            status=data["status"],
            priority=data["priority"],
            due_date=data.get("due_date"),
            google_drive_url=data.get("google_drive_url", ""),
            created_at=data.get("created_at", ""),
        )

    def is_near_deadline(self, days=3):
        """Cek apakah tugas mendekati deadline (dalam N hari)"""
        if not self.due_date:
            return False
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d")
            remaining = (due - datetime.now()).days
            return 0 <= remaining <= days and self.status != "Completed"
        except ValueError:
            return False

    # ---------- CRUD Operations ----------

    @staticmethod
    def create(name, project_id, priority="Medium", due_date=None, google_drive_url=""):
        db = Database.load()
        task = Task(
            id=db["next_task_id"],
            name=name,
            project_id=project_id,
            priority=priority,
            due_date=due_date,
            google_drive_url=google_drive_url,
        )
        db["tasks"].append(task.to_dict())
        db["next_task_id"] += 1
        Database.save(db)
        return task

    @staticmethod
    def get_all():
        db = Database.load()
        return [Task.from_dict(t) for t in db["tasks"]]

    @staticmethod
    def get_by_project(project_id):
        db = Database.load()
        return [Task.from_dict(t) for t in db["tasks"] if t["project_id"] == project_id]

    @staticmethod
    def get_by_id(task_id):
        db = Database.load()
        for t in db["tasks"]:
            if t["id"] == task_id:
                return Task.from_dict(t)
        return None

    @staticmethod
    def update(task_id, **kwargs):
        db = Database.load()
        for t in db["tasks"]:
            if t["id"] == task_id:
                for key, value in kwargs.items():
                    if key in t and value is not None:
                        t[key] = value
                Database.save(db)
                return Task.from_dict(t)
        return None

    @staticmethod
    def delete(task_id):
        db = Database.load()
        original_len = len(db["tasks"])
        db["tasks"] = [t for t in db["tasks"] if t["id"] != task_id]
        Database.save(db)
        return len(db["tasks"]) < original_len

    # ---------- Search & Filter (UC07) ----------

    @staticmethod
    def search_by_keyword(keyword):
        db = Database.load()
        keyword_lower = keyword.lower()
        results = []
        for t in db["tasks"]:
            if keyword_lower in t["name"].lower():
                results.append(Task.from_dict(t))
                continue
            # Cari juga berdasarkan nama proyek
            for p in db["projects"]:
                if p["id"] == t["project_id"] and keyword_lower in p["name"].lower():
                    results.append(Task.from_dict(t))
                    break
        return results

    @staticmethod
    def filter_by_due_date(date_str):
        db = Database.load()
        return [Task.from_dict(t) for t in db["tasks"] if t.get("due_date") == date_str]

    @staticmethod
    def filter_by_priority(priority):
        db = Database.load()
        return [Task.from_dict(t) for t in db["tasks"] if t["priority"] == priority]

    @staticmethod
    def get_near_deadline(days=3):
        tasks = Task.get_all()
        return [t for t in tasks if t.is_near_deadline(days)]
