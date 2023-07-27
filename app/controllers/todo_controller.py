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
    # loop through the todo's find the one with the same id
    # found_todo = None
    # for todo in session['todos']:
    #     if todo['id'] == id:
    #         found_todo = todo['id']
            
    found_todo = [todo for todo in session["todos"] if todo["id"] == id][0]

    return render_template("todo/view.html", todo=found_todo)

@app.route("/todo/add")
def get_add_todo_form():
    return render_template("todo/add.html")

# import redirect and request
@app.route("/todo/add", methods=['POST'])
def add_todo():
    
    new_todo = request.form

    todos = session.get("todos") # get todos from session

    todos.append( # add new todo
        {
            "id": random.randint(1, 1000000),
            "text": new_todo["text"],
            "description": new_todo["description"],
            "created_at": datetime.now(),
        }
    )

    session["todos"] = todos # save todos

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

@app.route("/todo/update", methods=["POST"])
def update_todo():

    form = request.form

    if form.get('id', None) is None:
        return redirect('/error')

    Todo.update(form)

    return redirect('/')