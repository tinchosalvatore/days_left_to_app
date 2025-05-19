import datetime
from flask import render_template, request, redirect, url_for
from app import app
from db import db
from model import Event


# Ruta a la página principal
@app.route('/') # Nombre de la ruta
def index():
    events = Event.query.order_by(Event.date).all()
    return render_template('index.html', events=events)

# Ruta para añadir un evento
@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        name = request.form['name']
        date_str = request.form['date']
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        
        new_event = Event(name=name, date=date)
        db.session.add(new_event)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add.html')

# Ruta para buscar un evento
@app.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return redirect(url_for('index'))
    
    event = Event.query.filter(Event.name.like(f'%{query}%')).first()
    
    if event:
        days_remaining = event.days_remaining()
        
        return render_template('index.html', 
                              event=event, 
                              days_remaining=days_remaining,
                              query=query)
    
    return render_template('index.html', 
                          no_results=True, 
                          query=query)


# Ruta para la página de confirmación de eliminación
@app.route('/delete/<int:event_id>')
def delete(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('delete.html', event=event)

# Ruta para eliminar un evento
@app.route('/delete/<int:event_id>', methods=['POST'])
def delete_event(
event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('index'))