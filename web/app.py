from flask import Flask, render_template, request, redirect
from vsearch import search4letters

app = Flask(__name__)

@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',the_title='Witamy na stronie search4letters')

@app.route('/search4', methods=['POST'])
def results_page() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    result = ",".join(list(search4letters(phrase,letters)))
    with open('log.txt','a') as f:
        print(phrase, letters, result, sep='|', file=f)
    return render_template('results.html',the_title='Oto Twoje wyniki', the_phrase=phrase, the_letters=letters, the_results=result)

@app.route('/log', methods=['GET'])
def log_page() ->'html':
    with open('log.txt','r') as f:
        result = [x.split('|') for x in f.readlines()]
        return render_template('log.html',the_title='Tutaj są Twoje logi', logs=result)

@app.route('/log/clear', methods=['GET'])
def log_page_clear() ->'html':
    with open('log.txt','w') as f:
        pass
    return redirect('/log')


if __name__ == '__main__':
    app.run(debug=True)