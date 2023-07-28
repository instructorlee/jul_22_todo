import random
from datetime import datetime
from app import app
from flask import Flask, render_template, session, redirect, request

from app.models.todo_model import Todo

# import session
@app.route("/")
def home():
    return render_template(
        '/todo/home.html', 
        todos=Todo.get_all()
        )

@app.route("/todo/<int:id>")
def view_todo(id):
    return render_template("todo/view.html", todo=Todo.get_by_id(id))

@app.route("/todo/add")
def get_add_todo_form():
    return render_template("todo/add.html")

# import redirect and request
@app.route("/todo/add", methods=['POST'])
def add_todo():
    
    new_todo = request.form

    Todo.create(new_todo)

    return redirect('/') # always redirect when methods == POST

@app.route("/todo/reset")
def reset():
    session.clear()
    return redirect("/")

@app.route("/todo/update/<int:id>")
def get_update_todo_form(id):
    return render_template(
        "todo/update.html",
        todo=Todo.get_by_id(id)
    )

@app.route("/todo/update", methods=['POST'])
def update_todo():

    form = request.form

    if form.get('id', None) is None:
        return redirect('/error')

    Todo.update(form)

    return redirect('/')
