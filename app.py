from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import part1

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
#SQLALCHEMY_TRACK_MODIFICATIONS = False

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.String(200), nullable=True)
    positive = db.Column(db.Integer, nullable=True)
    negative = db.Column(db.Integer, nullable=True)
    neutral = db.Column(db.Integer, nullable=True)
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        #print(task_content)
        resrev,pos,neg,neu=part1.getmov(task_content)

        new_task = Todo(content=task_content,rating=resrev,positive=pos,negative=neg,neutral=neu)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error storing to DataBase'

    else:
        tasks = Todo.query.all()
        return render_template('index.html',tasks=tasks)

@app.route('/chart/<int:id>')
def chart(id):
    if request.method == 'GET':

        task= Todo.query.get_or_404(id)
        print(task.id)
        return render_template('chart.html',task=task)

    else:
        return 'not post'

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


if __name__ == "__main__":
    app.run(debug=True)
