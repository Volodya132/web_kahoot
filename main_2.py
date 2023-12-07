from flask import Flask, render_template, request, redirect, url_for, session
from SQLAgent import SQLAgent

app = Flask(__name__)
app.secret_key = '123'
DB_NAME = "quizz.db"


@app.route("/")
def index():
    sql_agent = SQLAgent(DB_NAME)
    quizzes = sql_agent.get_quizzes()

    return render_template("index.html", quizzes=quizzes)

@app.route("/quizzes/<int:quizz_id>")
def quizz(quizz_id):
    sql_agent = SQLAgent(DB_NAME)
    questions = sql_agent.get_questions(quizz_id)

    session["questions"] = questions
    session["current_question"] = 0
    session["count_of_correct_answers"] = 0
    return redirect(url_for("question", quizz_id=quizz_id))


@app.route("/quizzes/<int:quizz_id>/question")
def question(quizz_id):
    db = SQLAgent(DB_NAME)
    question_index = session["current_question"]
    questions = session.get('questions', [])

    count_of_questions = len(questions)

    if question_index >= count_of_questions:
       return redirect(url_for("result", quizz_id=quizz_id))
    q= questions[question_index]
    options = db.get_options_for_question(q[0])

    return render_template('question.html', question=q, options=options, quizz_id=quizz_id)


@app.route("/quizzes/<int:quizz_id>/answer", methods=['POST'])
def answer_func(quizz_id):
    print(request.form)
    session['current_question'] += 1
    return redirect(url_for('question', quizz_id=quizz_id))

@app.route("/quizzes/<int:quizz_id>/result")
def result(quizz_id):
    return render_template('result.html')



app.run(debug=True)
