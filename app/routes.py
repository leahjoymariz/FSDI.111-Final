from flask import  Flask, render_template, request
from datetime import datetime
import requests

app = Flask(__name__)
BACKEND_URL = "http://127.0.0.1:5000"



@app.get("/")
def index():
    timestamp = datetime.now().strftime("%F %H:%M:%S")
    return render_template("index.html", ts=timestamp)


@app.get("/about")
def about_me():
    me = {
        "first_name": ";Leah",
        "last_name": "Duco",
        "hobbies": "Cooking",
    }
    return render_template("about.html", about=me)


@app.get("/tasks")
def display_all_tasks():
    url = "%s/%s" % (BACKEND_URL, "tasks")
    resp = requests.get(url)
    if resp.status_code == 200:
        task_data = resp.json()
        return render_template("task_list.html", tasks=task_data["tasks"])
    return render_template("error.html", err_code=resp.status_code), resp.status_code


@app.get("/tasks/edit/<int:pk>")
def get_edit_form(pk):
    url = "%s/tasks/%s" % (BACKEND_URL, pk)
    resp = requests.get(url)
    if resp.status_code == 200:
        task_data = resp.json()
        return render_template("edit.html", task=task_data["task"])
    return render_template("error.html", err_code=resp.status_code), resp.status_code


@app.post("/tasks/edit/<int:pk>")
def update_task(pk):
    url = "%s/tasks/%s" % (BACKEND_URL, pk)
    form_data = request.form
    task_data = {
        "summary": form_data.get("summary"),
        "description": form_data.get("description"),
        "is_done": form_data.get("is_done")
    }
    resp = requests.put(url, json=task_data)
    if resp.status_code == 204:
        return render_template("success.html", msg="Task updated")
    return render_template("error.html", err_code=resp.status_code), resp.status_code


@app.get("/tasks/new")
def get_create_form():
    return render_template("new.html")
