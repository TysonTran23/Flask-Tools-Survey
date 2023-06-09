from surveys import satisfaction_survey
from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


responses = []

@app.route('/')
def survey():
    """The starting page of the survey"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('survey.html', title=title, instructions=instructions)

@app.route('/questions/<int:question_number>')
def question(question_number):
    question = satisfaction_survey.questions[question_number].question
    answers = satisfaction_survey.questions[question_number].choices
    return render_template('question.html', question=question, answers=answers, question_number=question_number)

@app.route('/answer', methods=["POST"])
def answer():
    answer = request.form.get('answer')
    responses.append(answer)
    next_question = len(responses)

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank-you')
    return redirect(f'/questions/{next_question}')

@app.route('/thank-you')
def thank_you():
    return render_template('thankyou.html')

