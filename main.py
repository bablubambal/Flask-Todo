from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#Starting the flask app
app = Flask(__name__)
#Configuring the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)
# db.create_all() => to create the table in the table
class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    description = db.Column(db.Text,nullable = False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return 'Todo List: '+str(self.id)
# title = "hello todo"
# description = "hi i am the description"
# db.session.add(Todo(title = title,description = description))
# db.session.commit()



@app.route("/",methods = ['GET','POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        new_todo = Todo(title=title, description=description)
        db.session.add(new_todo)
        db.session.commit()
        return redirect('/')
    else:
        all_todos = Todo.query.all()
        #print(all_todos)
        return  render_template('index.html', todos = all_todos)


@app.route("/delete/<int:id>")
def deletetodo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route("/edit/<int:id>", methods = ['GEt','POST'])
def edittodo(id):
    todo = Todo.query.get_or_404(id)
    print(todo)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.description = request.form['description']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html', todo = todo)

@app.route('/newtodo')
def newtodo():
    return render_template('newtodo.html')


if __name__ == "__main__":
    app.run(debug=True)