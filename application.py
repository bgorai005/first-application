from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

application = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLite config
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(application)

# Model: Single-column table (id, name)
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Create table
with application.app_context():
    db.create_all()

# Routes
@application.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        if name:
            item = Item(name=name)
            db.session.add(item)
            db.session.commit()
        return redirect(url_for('index'))

    items = Item.query.all()
    return render_template('index.html', items=items)

@application.route('/update/<int:id>', methods=['POST'])
def update(id):
    item = Item.query.get_or_404(id)
    name = request.form['name']
    if name:
        item.name = name
        db.session.commit()
    return redirect(url_for('index'))

@application.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    application.run(debug=True)
