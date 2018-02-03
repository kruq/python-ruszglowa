from flask import Flask, render_template, request, redirect
from vsearch import search4letters
import mysql.connector

app = Flask(__name__)

dbconfig = {
        'host': '127.0.0.1',
        'user': 'darek',
        'password': 'darek',
        'database': 'test',
    }

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',the_title='Witamy na stronie search4letters')

@app.route('/search4', methods=['POST'])
def results_page() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    result = ",".join(list(search4letters(phrase,letters)))

    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    sql = """insert into vsearch 
            (phrase, letters, result, browser)
            value
            (%s, %s, %s, %s)
        """
    cursor.execute(sql, (phrase, letters, result, request.user_agent.browser))
    conn.commit()
    cursor.close()
    conn.close()
    return render_template('results.html',the_title='Oto Twoje wyniki', the_phrase=phrase, the_letters=letters, the_results=result)

@app.route('/log', methods=['GET'])
def log_page() ->'html':
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    sql = 'select * from vsearch'
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('log.html',the_title='Tutaj są Twoje logi', logs=result)

@app.route('/log/clear', methods=['GET'])
def log_page_clear() ->'html':
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    sql = 'truncate vsearch'
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/log')


if __name__ == '__main__':
    app.run(debug=True)