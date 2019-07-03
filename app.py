from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
#dev
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://redrambles:meemoo@localhost/flasktodo'
#prod
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qjpypinjfxhicu:d7092e1dc722bc9571e73683f4e867768296e954c88559f3fd49c3d778a650e7@ec2-174-129-209-212.compute-1.amazonaws.com:5432/d6441pv7926urp'
db = SQLAlchemy(app)

# Create database table 'Todo' and insert 'id' and 'content' columns
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # return "Hello you submitted this form"
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks )

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Unable to delete task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    # If this is a post request, you are updating a task and hitting Submit
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit() 
            return redirect('/')
        except:
            return "There was a problem updating this task"
    # This is a get request - you just want to get to the update page
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)