import os
from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename


application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
application.config["IMAGE_UPLOADS"] = "/Users/sandy/FLASK2021/uploads"
application.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
application.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024
db = SQLAlchemy(application)

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in application.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

def allowed_image_filesize(filesize):

    if int(filesize) <= application.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"




@application.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = (request.form['title'])
        desc = (request.form['desc'])
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)


@application.route("/show")
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@application.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@application.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@application.route("/upload_image", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            print(image)

            return redirect(request.url)


    return render_template("public/upload_image.html")


if __name__ == "__main__":
    application.run(debug=True, port=8000)     