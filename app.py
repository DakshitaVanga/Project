from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
db = SQLAlchemy(app)

class Todos(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable= False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Name %r>' %self.id

@app.route('/')
def index():
	title = "Dakshita's Todo List"
	return render_template("index.html",title=title)

@app.route('/about')
def about():
	todos = ["yoga", "leetcode", "dance", "run"]
	return render_template("about.html", todos = todos)

@app.route('/todos', methods=['POST', 'GET'])
def todos():
	title = "My Todo List"
	if request.method =="POST":
		todo_name = request.form['name']
		new_todo = Todos(name=todo_name)

		try:
			db.session.add(new_todo)
			db.session.commit()
			return redirect('/todos')
		except:
			return "There was an error adding your todo"

	else:
		todos = Todos.query.order_by(Todos.date_created)
		return render_template("todos.html", title=title, todos=todos)

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
	todo_to_update = Todos.query.get_or_404(id)
	
	if request.method =="POST":
		todo_to_update.name = request.form['name']

		try:
			db.session.commit()
			return redirect('/todos')
		except:
			return "There was an error updating your todo"

	else:
		return render_template("update.html", todo_to_update=todo_to_update)	

@app.route('/delete/<int:id>')
def delete(id):
	todo_to_delete = Todos.query.get_or_404(id)
	try:
		db.session.delete(todo_to_delete)
		db.session.commit()
		return redirect('/todos')
	except:
		return "There was an error deleting your todo"

	

if __name__=='__main__':
	app.run(debug=True)