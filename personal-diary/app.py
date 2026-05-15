from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta

app = Flask(__name__)
FILE_NAME = 'entries.json'

def load_entries():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_entries(entries):
    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

entries = load_entries()

@app.route('/')
def index():
    return render_template('index.html', entries=entries)

@app.route('/entry/<int:entry_id>')
def detail(entry_id):
    for entry in entries:
        if entry['id'] == entry_id:
            return render_template('detail.html', entry=entry)
    return "Запись не найдена", 404

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_id = 1 if not entries else max(e['id'] for e in entries) + 1
        new_entry = {
            'id': new_id,
            'title': title,
            'content': content,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        entries.append(new_entry)
        save_entries(entries)
        return redirect('/')
    return render_template('add.html')

@app.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
def edit(entry_id):
    for i, entry in enumerate(entries):
        if entry['id'] == entry_id:
            if request.method == 'POST':
                entries[i]['title'] = request.form['title']
                entries[i]['content'] = request.form['content']
                save_entries(entries)
                return redirect('/')
            return render_template('edit.html', entry=entry)
    return "Запись не найдена", 404

@app.route('/delete/<int:entry_id>', methods=['POST'])
def delete(entry_id):
    global entries
    entries = [e for e in entries if e['id'] != entry_id]
    save_entries(entries)
    return redirect('/')

@app.route('/search')
def search():
    q = request.args.get('q', '').lower()
    filtered = [e for e in entries if q in e['title'].lower()] if q else entries
    return render_template('index.html', entries=filtered)

@app.route('/filter/week')
def filter_week():
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    filtered = [e for e in entries if datetime.strptime(e['date'], '%Y-%m-%d').date() >= week_ago]
    return render_template('index.html', entries=filtered)

if __name__ == '__main__':
    app.run(debug=True)