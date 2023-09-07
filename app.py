from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Veritabanı yapılandırması
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

# Notlar veritabanı modeli
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Note {self.id}>'

# Ana sayfa
@app.route('/')
def index():
    notes = Note.query.all()
    return render_template('index.html', notes=notes)

# Not ekleme
@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    category = request.form['category']
    note = Note(title=title, content=content, category=category)
    
    # Uygulama bağlamını oluşturun
    with app.app_context():
        db.session.add(note)
        db.session.commit()
    
    return redirect('/')

# Not düzenleme
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    note = Note.query.get(id)
    if request.method == 'POST':
        note.title = request.form['title']
        note.content = request.form['content']
        note.category = request.form['category']
        
        # Uygulama bağlamını oluşturun
        with app.app_context():
            db.session.commit()
        
        return redirect('/')
    return render_template('edit.html', note=note)

# Not silme
@app.route('/delete/<int:id>')
def delete_note(id):
    note = Note.query.get(id)
    
    # Uygulama bağlamını oluşturun
    with app.app_context():
        db.session.delete(note)
        db.session.commit()
    
    return redirect('/')

if __name__ == '__main__':
    # Uygulama bağlamını oluşturun
    with app.app_context():
        db.create_all()
    app.run(debug=True)
