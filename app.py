from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from dotenv import load_dotenv
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Ключ для сессий

# Загрузка переменных окружения из файла .env
load_dotenv()

# Функция для записи данных пользователя в файл .env
def save_user_data(email, password):
    with open('.env', 'a') as file:
        file.write(f"{email}:{password}\n")

# Функция для проверки данных пользователя
def check_user_data(email, password):
    with open('.env', 'r') as file:
        for line in file:
            stored_email, stored_password = line.strip().split(':')
            if email == stored_email and password == stored_password:
                return True
    return False

# Функция для проверки существования логина
def is_email_registered(email):
    with open('.env', 'r') as file:
        for line in file:
            stored_email, _ = line.strip().split(':')
            if email == stored_email:
                return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    if is_email_registered(email):
        flash('Email already registered. Please use a different email.', 'error')
        return redirect(url_for('index'))
    save_user_data(email, password)
    flash('Registration successful. Please log in.', 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if check_user_data(email, password):
        session['user'] = email
        return redirect(url_for('projects'))
    else:
        flash('Invalid email or password.', 'error')
        return redirect(url_for('index'))

@app.route('/projects')
def projects():
    if 'user' not in session:
        return redirect(url_for('index'))
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d')  # Год-месяц-день
    formatted_time = now.strftime('%H:%M:%S')  # Часы:минуты:секунды
    day_of_week = now.strftime('%A')  # День недели (например, Monday)

    return render_template(
        'projects.html',
        date=formatted_date,
        time=formatted_time,
        day_of_week=day_of_week
    )

@app.route('/projects_page')
def projects_page():
    return render_template('projects_page.html')

@app.route('/admin_page')
def admin_page():
    return render_template('admin_page.html')

@app.route('/list_all_users')
def list_all_users():
    return render_template('list_all_users.html')

@app.route('/all_tasks')
def all_tasks():
    return render_template('all_tasks.html')

@app.route('/add_user')
def add_user():
    return render_template('add_user.html')

@app.route('/user_del')
def user_del():
    return render_template('user_del.html')

@app.route('/list_user_project')
def list_user_project():
    return render_template('list_user_project.html')

@app.route('/task_users_manager')
def task_users_manager():
    return render_template('task_users_manager.html')

@app.route('/report_users')
def report_users():
    return render_template('report_users.html')

@app.route('/list_tasks_see')
def list_tasks_see():
    return render_template('list_tasks_see.html')

@app.route('/add_task')
def add_task():
    return render_template('add_task.html')

@app.route('/deadline_task')
def deadline_task():
    return render_template('deadline_task.html')

@app.route('/save_task_file')
def save_task_file():
    return render_template('save_task_file.html')

@app.route('/change_task_status')
def change_task_status():
    return render_template('change_task_status.html')

@app.route('/save_report')
def save_report():
    return render_template('save_report.html')

@app.route('/del_task')
def del_task():
    return render_template('del_task.html')

# Директории для пользователей и архива
USERS_FOLDER = 'Users'
ARCHIVE_FOLDER = 'Archive'

os.makedirs(USERS_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

@app.route('/save_profile', methods=['POST'])
def save_profile():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized access!'}), 401

    user_email = session['user']
    user_folder = os.path.join(USERS_FOLDER, user_email)
    os.makedirs(user_folder, exist_ok=True)

    # Сохраняем фото профиля
    profile_photo = request.files.get('profile_photo')
    if profile_photo:
        photo_path = os.path.join(user_folder, 'profile_photo.jpg')
        profile_photo.save(photo_path)

    # Сохраняем данные пользователя
    user_data = {
        'email': user_email,
        'last_name': request.form.get('last_name'),
        'first_name': request.form.get('first_name'),
        'birthdate': request.form.get('birthdate'),
        'phone': request.form.get('phone'),
        'profile_photo': photo_path
    }
    user_data_path = os.path.join(user_folder, 'user_data.json')
    with open(user_data_path, 'w', encoding='utf-8') as file:
        json.dump(user_data, file, ensure_ascii=False, indent=4)

    return jsonify({'message': 'Profile saved successfully!', 'data': user_data})

@app.route('/delete_profile', methods=['POST'])
def delete_profile():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized access!'}), 401

    user_email = session['user']
    user_folder = os.path.join(USERS_FOLDER, user_email)
    archive_folder = os.path.join(ARCHIVE_FOLDER, user_email)

    if os.path.exists(user_folder):
        os.rename(user_folder, archive_folder)
        return jsonify({'message': f'Profile archived successfully at {archive_folder}.'})
    else:
        return jsonify({'error': 'Profile not found!'}), 404

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
