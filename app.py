import sqlite3
import requests # DeepSeek-пен байланысу үшін қажет
import smtplib # Email жіберу үшін
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, g, jsonify
import threading
app = Flask(__name__)
DATABASE = 'hope_light.db'


DEEPSEEK_API_KEY = "sk-71f366ac9de246808f01f673a48514ba" 
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "qplayzx@gmail.com"      
SENDER_PASSWORD = "glym xpcw lujs zsqa"     
PSYCHOLOGIST_EMAIL = "umsyn-bolatovna-777@mail.ru" 



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('init-db')
def init_db_command():
    init_db()
    print('Деректер қоры инициализацияланды.')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/urgent-help', methods=['GET', 'POST'])
def urgent_help():
    
    if request.method == 'POST':
        message_body = request.form['message']
        
      
        try:
          
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = PSYCHOLOGIST_EMAIL
            msg['Subject'] = "SOS: ОҚУШЫҒА ЖЕДЕЛ КӨМЕК ҚАЖЕТ! (Аноним)"
            
            body = f"Сайттан анонимді SOS хабарлама келді:\n\nХабарлама: {message_body}\n\n---\nБұл автоматты хабарлама."
            msg.attach(MIMEText(body, 'plain'))
            def send_async_email(msg_obj):
                try:
                    # Используем SSL и порт 465 (самый надежный вариант)
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.login(SENDER_EMAIL, SENDER_PASSWORD)
                    server.sendmail(SENDER_EMAIL, PSYCHOLOGIST_EMAIL, msg_obj.as_string())
                    server.quit()
                    print("Письмо успешно отправлено в фоне.")
                except Exception as e:
                    print(f"Ошибка при отправке письма: {e}")

            # Запускаем отправку в отдельном потоке
            email_thread = threading.Thread(target=send_async_email, args=(msg,))
            email_thread.start()
            # --- КОНЕЦ ИСПРАВЛЕНИЯ ---
            
            # Сразу перенаправляем пользователя, не дожидаясь отправки
            return redirect(url_for('urgent_success'))
            
        except Exception as e:
            print(f"Email Error: {e}")
    
            return render_template('urgent_error.html', error=str(e))

    return render_template('urgent_help.html')

@app.route('/urgent-success')
def urgent_success():
    return render_template('urgent_success.html')


@app.route('/emotional-support')
def emotional_support():
    return render_template('emotional_support.html')

@app.route('/psychological-support')
def psychological_support():
    return render_template('psychological_support.html')

@app.route('/mood-diary', methods=['GET', 'POST'])
def mood_diary():
    db = get_db()
    if request.method == 'POST':
        mood = request.form['mood']
        notes = request.form['notes']
        if mood:
            db.execute('INSERT INTO mood_entries (mood, notes) VALUES (?, ?)', (mood, notes))
            db.commit()
            return redirect(url_for('mood_diary'))
    entries = db.execute('SELECT * FROM mood_entries ORDER BY created_at DESC').fetchall()
    return render_template('mood_diary.html', entries=entries)

@app.route('/support-wall', methods=['GET', 'POST'])
def support_wall():
    db = get_db()
    if request.method == 'POST':
        author = request.form['author_name']
        post_text = request.form['post_text']
        if not author:
            author = "Аноним"
        if post_text:
            db.execute('INSERT INTO support_posts (author_name, post_text) VALUES (?, ?)', (author, post_text))
            db.commit()
            return redirect(url_for('support_wall'))
    posts = db.execute('SELECT * FROM support_posts ORDER BY created_at DESC').fetchall()
    return render_template('support_wall.html', posts=posts)

@app.route('/light-candle/<int:post_id>', methods=['POST'])
def light_candle(post_id):
    db = get_db()
    db.execute('UPDATE support_posts SET candle_count = candle_count + 1 WHERE id = ?', (post_id,))
    db.commit()
    return redirect(url_for('support_wall'))

@app.route('/q-and-a', methods=['GET', 'POST'])
def q_and_a():
    db = get_db()
    if request.method == 'POST':
        question_text = request.form['question']
        if question_text:
            db.execute('INSERT INTO questions (question_text) VALUES (?)', (question_text,))
            db.commit()
            return redirect(url_for('q_and_a'))
    questions = db.execute('SELECT * FROM questions ORDER BY created_at DESC').fetchall()
    return render_template('q_and_a.html', questions=questions)

@app.route('/appointment', methods=['GET', 'POST'])
def appointment():
    if request.method == 'POST':
        student_name = request.form['student_name']
        contact_info = request.form['contact_info']
        preferred_time = request.form['preferred_time']
        db = get_db()
        db.execute('INSERT INTO appointments (student_name, contact_info, preferred_time) VALUES (?, ?, ?)',
                     (student_name, contact_info, preferred_time))
        db.commit()
        return redirect(url_for('appointment_success'))
    return render_template('appointment.html')

@app.route('/appointment-success')
def appointment_success():
    return render_template('appointment_success.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    # ... (DeepSeek чат коды өзгеріссіз қалады) ...
    data = request.json
    user_message = data.get('message')
    if not user_message:
        return jsonify({'error': 'Хабарлама бос'}), 400

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    system_prompt = """
    Сенің атың - "Үміт". Сен мектеп оқушыларына арналған эмоциялық қолдау сайтындағы виртуалды көмекшісің.
    Тілің: Қазақ тілі.
    Сөйлеу мәнерің: Жылы, түсіністікпен қарайтын, қолдау көрсететін дос немесе мейірімді психолог сияқты.
    Мақсатың: Оқушының көңіл-күйін тыңдау, жақсы кеңес беру, стрессті азайту.
    Маңызды ереже: Егер оқушы өзіне қол жұмсау (суицид) немесе ауыр депрессия туралы айтса, бірден мектеп психологына баруға кеңес бер және оны жалғыз қалдырмауға тырыс.
    Жауаптарың тым ұзын болмасын, оқушыға жеңіл болсын.
    """
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }
    try:
        response = requests.post(DEEPSEEK_URL, headers=headers, json=payload)
        if response.status_code != 200:
            print(f"DeepSeek API Error: {response.status_code}")
        response.raise_for_status()
        api_data = response.json()
        bot_reply = api_data['choices'][0]['message']['content']
        return jsonify({'reply': bot_reply})
    except Exception as e:
        print(f"Жалпы қате: {e}")
        return jsonify({'reply': 'Кешіріңіз, қазір байланыс нашар болып тұр. Біраздан соң қайта жазып көріңізші. ❤️'}), 500

if __name__ == '__main__':
    app.run(debug=True)


