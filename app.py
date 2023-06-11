from surveys import satisfaction_survey
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


responses = []
"""List of answers from survey"""
@app.route('/')
def survey():
    """The starting page of the survey"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('survey.html', title=title, instructions=instructions)

@app.route('/questions/<int:question_number>')
def question(question_number):
    """Shows the question and choices on the pages"""
    question = satisfaction_survey.questions[question_number].question
    answers = satisfaction_survey.questions[question_number].choices
    total_questions = satisfaction_survey.questions

    #Checks if all questions are answered
    if len(responses) == len(total_questions):
        return redirect('/thank-you')
    
    #Checks if questions are within the range
    if question_number != len(responses):
        flash('You are skipping questions, not allowed')
        return redirect(f'/questions/{len(responses)}')



    return render_template('question.html', question=question, answers=answers, question_number=question_number)

@app.route('/answer', methods=["POST"])
def answer():
    """Appends the answer from the form and redirects to the next question"""
    answer = request.form.get('answer')
    responses.append(answer)
    next_question = len(responses)

    """When the user finishes answering all the questions, show a thank you page"""
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank-you')
    return redirect(f'/questions/{next_question}')

@app.route('/thank-you')
def thank_you():
    """Show a thank you page"""
    return render_template('thankyou.html')

