from flask import Flask, render_template, url_for, request, redirect
import sqlite3
import menu


app = Flask(__name__)
conn = sqlite3.connect('database.db')
c = conn.cursor()

menu.setupDB()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_name = request.form['name'].strip()
        task_email = request.form['email'].strip()
        

        try:
            menu.addUser(task_name,task_email)
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = menu.printAll()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<string:name>')
def delete(name):
    nameToDelete = name
    print(nameToDelete)
    try:
        menu.deleteUser(nameToDelete)
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        borrower = request.form['borrower'].strip()
        lender = request.form['lender'].strip()
        amount = request.form['amount']
        

        try:
            menu.addDebts(borrower,lender,amount)
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        return redirect('/')

@app.route('/pay', methods=['POST', 'GET'])
def makePayment():
    if request.method == 'POST':
        borrower = request.form['borrower'].strip()
        lender = request.form['lender'].strip()
        amount = request.form['amount']
        

        try:
            menu.makePayment(borrower,lender,amount)
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)