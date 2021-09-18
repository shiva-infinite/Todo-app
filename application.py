from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os


application= Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['UPLOAD_FOLDER1'] = "/Users/sandy/FLASK2021/uploads"
application.config['UPLOAD_FOLDER2'] = "/Users/sandy/FLASK2021/uploads2"
db = SQLAlchemy(application)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@application.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo)

@application.route('/show')
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

@application.route("/uploader" , methods=['GET', 'POST'])
def uploader():
    count = 0
    if (count < 3):
        if request.method=='POST':
            f = request.files['file1']
            f.save(os.path.join(application.config['UPLOAD_FOLDER1'], secure_filename(f.filename)))
            count = count + 1
            return "Uploaded successfully!"
    else:
        if request.method=='POST':
            f = request.files['file1']
            f.save(os.path.join(application.config['UPLOAD_FOLDER2'], secure_filename(f.filename)))
            return "Uploaded successfully!"


if __name__ == "__main__":
    application.run(debug=True, port=8000)
