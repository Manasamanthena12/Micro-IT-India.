from flask import Flask, render_template, request, jsonify, session, redirect
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Use an environment variable for the database URI, default to SQLite for local development
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quiz.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    question = db.Column(db.String(500))
    options = db.Column(db.String(500))  # Comma-separated options
    correct_answer = db.Column(db.String(200))

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    category = db.Column(db.String(100))
    score = db.Column(db.Integer)

# Initialize Database with Sample Questions
def init_db():
    db.drop_all()
    db.create_all()
    
    # Sample Questions (10 per category)
    questions = [
        # General Knowledge
        Question(
            category="General Knowledge",
            question="What is the capital of France?",
            options="Paris,London,Berlin,Madrid",
            correct_answer="Paris"
        ),
        Question(
            category="General Knowledge",
            question="Which planet is known as the Red Planet?",
            options="Mars,Venus,Jupiter,Mercury",
            correct_answer="Mars"
        ),
        Question(
            category="General Knowledge",
            question="Who painted the Mona Lisa?",
            options="Leonardo da Vinci,Pablo Picasso,Vincent van Gogh,Claude Monet",
            correct_answer="Leonardo da Vinci"
        ),
        Question(
            category="General Knowledge",
            question="What is the largest ocean?",
            options="Pacific,Atlantic,Indian,Arctic",
            correct_answer="Pacific"
        ),
        Question(
            category="General Knowledge",
            question="Which country hosted the 2016 Olympics?",
            options="Brazil,China,UK,USA",
            correct_answer="Brazil"
        ),
        Question(
            category="General Knowledge",
            question="What is the chemical symbol for Gold?",
            options="Au,Ag,Fe,Cu",
            correct_answer="Au"
        ),
        Question(
            category="General Knowledge",
            question="Which animal is known as man's best friend?",
            options="Dog,Cat,Horse,Rabbit",
            correct_answer="Dog"
        ),
        Question(
            category="General Knowledge",
            question="What is the tallest mountain in the world?",
            options="Everest,K2,Kilimanjaro,Denali",
            correct_answer="Everest"
        ),
        Question(
            category="General Knowledge",
            question="Which gas is most abundant in Earth's atmosphere?",
            options="Nitrogen,Oxygen,Carbon Dioxide,Argon",
            correct_answer="Nitrogen"
        ),
        Question(
            category="General Knowledge",
            question="Who wrote 'Romeo and Juliet'?",
            options="William Shakespeare,Charles Dickens,Jane Austen,Mark Twain",
            correct_answer="William Shakespeare"
        ),
        
        # Indian Constitution
        Question(
            category="Indian Constitution",
            question="Who is known as the Father of the Indian Constitution?",
            options="Mahatma Gandhi,B.R. Ambedkar,Jawaharlal Nehru,Sardar Patel",
            correct_answer="B.R. Ambedkar"
        ),
        Question(
            category="Indian Constitution",
            question="When was the Indian Constitution adopted?",
            options="26 Nov 1949,15 Aug 1947,26 Jan 1950,1 Jan 1948",
            correct_answer="26 Nov 1949"
        ),
        Question(
            category="Indian Constitution",
            question="How many Fundamental Rights are there?",
            options="6,7,8,9",
            correct_answer="6"
        ),
        Question(
            category="Indian Constitution",
            question="Which article deals with the Right to Equality?",
            options="Article 14-18,Article 19-22,Article 23-24,Article 25-28",
            correct_answer="Article 14-18"
        ),
        Question(
            category="Indian Constitution",
            question="Who is the head of state in India?",
            options="Prime Minister,President,Chief Justice,Governor",
            correct_answer="President"
        ),
        Question(
            category="Indian Constitution",
            question="What is the minimum age to become President of India?",
            options="25,30,35,40",
            correct_answer="35"
        ),
        Question(
            category="Indian Constitution",
            question="Which part of the Constitution deals with Fundamental Duties?",
            options="Part IVA,Part III,Part V,Part VI",
            correct_answer="Part IVA"
        ),
        Question(
            category="Indian Constitution",
            question="How many schedules are in the Indian Constitution?",
            options="10,12,14,16",
            correct_answer="12"
        ),
        Question(
            category="Indian Constitution",
            question="Which amendment introduced the GST?",
            options="101st,99th,97th,95th",
            correct_answer="101st"
        ),
        Question(
            category="Indian Constitution",
            question="Who appoints the Chief Justice of India?",
            options="President,Prime Minister,Parliament,Supreme Court",
            correct_answer="President"
        ),
        
        # Programming (Python)
        Question(
            category="Programming-Python",
            question="What is the output of print(2**3)?",
            options="6,8,9,12",
            correct_answer="8"
        ),
        Question(
            category="Programming-Python",
            question="Which keyword defines a function in Python?",
            options="def,func,function,lambda",
            correct_answer="def"
        ),
        Question(
            category="Programming-Python",
            question="What is the default value of a variable in Python?",
            options="0,None,null,undefined",
            correct_answer="None"
        ),
        Question(
            category="Programming-Python",
            question="How do you create a list?",
            options="[],{},(),<>",
            correct_answer="[]"
        ),
        Question(
            category="Programming-Python",
            question="What does 'len()' function do?",
            options="Returns length,Returns type,Returns id,Returns value",
            correct_answer="Returns length"
        ),
        Question(
            category="Programming-Python",
            question="Which module is used for regular expressions?",
            options="re,regex,regexp,pattern",
            correct_answer="re"
        ),
        Question(
            category="Programming-Python",
            question="What is the output of 'True and False'?",
            options="True,False,Error,None",
            correct_answer="False"
        ),
        Question(
            category="Programming-Python",
            question="How do you comment a single line?",
            options="#,//,/*,<!--",
            correct_answer="#"
        ),
        Question(
            category="Programming-Python",
            question="What is the purpose of 'pass' statement?",
            options="Exit loop,Do nothing,Continue,Return value",
            correct_answer="Do nothing"
        ),
        Question(
            category="Programming-Python",
            question="Which data type is immutable?",
            options="List,Dictionary,Tuple,Set",
            correct_answer="Tuple"
        ),
        
        # Programming (JavaScript)
        Question(
            category="Programming-JavaScript",
            question="What is the output of 'typeof null'?",
            options="object,null,undefined,string",
            correct_answer="object"
        ),
        Question(
            category="Programming-JavaScript",
            question="How do you declare a variable?",
            options="var,let,const,All of the above",
            correct_answer="All of the above"
        ),
        Question(
            category="Programming-JavaScript",
            question="What does '=== 'check?",
            options="Value only,Type only,Value and type,None",
            correct_answer="Value and type"
        ),
        Question(
            category="Programming-JavaScript",
            question="Which method adds an element to the end of an array?",
            options="push(),pop(),shift(),unshift()",
            correct_answer="push()"
        ),
        Question(
            category="Programming-JavaScript",
            question="What is a closure?",
            options="Function with lexical scope,Loop,Class,Module",
            correct_answer="Function with lexical scope"
        ),
        Question(
            category="Programming-JavaScript",
            question="What does 'NaN' stand for?",
            options="Not a Number,Null and None,New Array Number,Not assigned Number",
            correct_answer="Not a Number"
        ),
        Question(
            category="Programming-JavaScript",
            question="How do you create an object?",
            options="{},[],(),<>",
            correct_answer="{}"
        ),
        Question(
            category="Programming-JavaScript",
            question="What is the event loop?",
            options="Manages asynchronous calls,Loops through arrays,Handles DOM events,Controls CSS",
            correct_answer="Manages asynchronous calls"
        ),
        Question(
            category="Programming-JavaScript",
            question="Which keyword stops a loop?",
            options="break,continue,return,exit",
            correct_answer="break"
        ),
        Question(
            category="Programming-JavaScript",
            question="What is 'this' in a method?",
            options="Current object,Global object,Function,Null",
            correct_answer="Current object"
        ),
        
        # Programming (C)
        Question(
            category="Programming-C",
            question="What is the size of an int in C (on a 32-bit system)?",
            options="2 bytes,4 bytes,8 bytes,1 byte",
            correct_answer="4 bytes"
        ),
        Question(
            category="Programming-C",
            question="Which keyword is used to define a constant?",
            options="const,define,static,final",
            correct_answer="const"
        ),
        Question(
            category="Programming-C",
            question="What does 'printf' do?",
            options="Reads input,Prints output,Declares a variable,Loops",
            correct_answer="Prints output"
        ),
        Question(
            category="Programming-C",
            question="How do you declare a pointer?",
            options="*ptr,ptr*,&ptr,ptr&",
            correct_answer="*ptr"
        ),
        Question(
            category="Programming-C",
            question="What is the output of '5 % 2'?",
            options="2,1,0,3",
            correct_answer="1"
        ),
        Question(
            category="Programming-C",
            question="Which header file is needed for 'scanf'?",
            options="stdio.h,stdlib.h,math.h,string.h",
            correct_answer="stdio.h"
        ),
        Question(
            category="Programming-C",
            question="What does 'break' do in a loop?",
            options="Exits loop,Continues loop,Restarts loop,Pauses loop",
            correct_answer="Exits loop"
        ),
        Question(
            category="Programming-C",
            question="What is the default return type of 'main'?",
            options="void,int,float,double",
            correct_answer="int"
        ),
        Question(
            category="Programming-C",
            question="Which operator is used for dereferencing a pointer?",
            options="*,&,%$,",
            correct_answer="*"
        ),
        Question(
            category="Programming-C",
            question="What is the output of '++i' if i=5?",
            options="5,6,4,7",
            correct_answer="6"
        ),
        
        # Programming (C++)
        Question(
            category="Programming-C++",
            question="Which keyword is used for inheritance?",
            options="extends,public,private,protected",
            correct_answer="public"
        ),
        Question(
            category="Programming-C++",
            question="What is the output of 'cout << 5/2'?",
            options="2.5,2,3,1",
            correct_answer="2"
        ),
        Question(
            category="Programming-C++",
            question="Which library is needed for 'cout'?",
            options="iostream,stdio.h,cmath,string",
            correct_answer="iostream"
        ),
        Question(
            category="Programming-C++",
            question="What does 'new' operator do?",
            options="Declares variable,Allocates memory,Deallocates memory,Loops",
            correct_answer="Allocates memory"
        ),
        Question(
            category="Programming-C++",
            question="What is a class in C++?",
            options="Loop,Function,Blueprint for objects,Variable",
            correct_answer="Blueprint for objects"
        ),
        Question(
            category="Programming-C++",
            question="What is the access modifier for private members?",
            options="public,private,protected,static",
            correct_answer="private"
        ),
        Question(
            category="Programming-C++",
            question="What does 'virtual' keyword do?",
            options="Enables polymorphism,Declares variable,Loops,Includes file",
            correct_answer="Enables polymorphism"
        ),
        Question(
            category="Programming-C++",
            question="Which container is used for dynamic arrays?",
            options="vector,array,list,queue",
            correct_answer="vector"
        ),
        Question(
            category="Programming-C++",
            question="What is the output of 'sizeof(char)'?",
            options="1 byte,2 bytes,4 bytes,8 bytes",
            correct_answer="1 byte"
        ),
        Question(
            category="Programming-C++",
            question="What does 'delete' operator do?",
            options="Allocates memory,Deallocates memory,Declares variable,Loops",
            correct_answer="Deallocates memory"
        ),
        
        # Programming (Java)
        Question(
            category="Programming-Java",
            question="Which keyword creates a new object?",
            options="new,create,alloc,object",
            correct_answer="new"
        ),
        Question(
            category="Programming-Java",
            question="What is the parent class of all classes in Java?",
            options="Object,Class,Main,System",
            correct_answer="Object"
        ),
        Question(
            category="Programming-Java",
            question="What does 'public static void main' do?",
            options="Declares variable,Entry point,Loops,Prints output",
            correct_answer="Entry point"
        ),
        Question(
            category="Programming-Java",
            question="Which keyword is used for inheritance?",
            options="extends,implements,super,this",
            correct_answer="extends"
        ),
        Question(
            category="Programming-Java",
            question="What is the default value of an int?",
            options="0,null,-1,undefined",
            correct_answer="0"
        ),
        Question(
            category="Programming-Java",
            question="Which collection stores key-value pairs?",
            options="ArrayList,HashMap,HashSet,Queue",
            correct_answer="HashMap"
        ),
        Question(
            category="Programming-Java",
            question="What does 'final' keyword do?",
            options="Makes variable constant,Loops,Declares function,Includes file",
            correct_answer="Makes variable constant"
        ),
        Question(
            category="Programming-Java",
            question="What is the output of '5/2' in Java?",
            options="2.5,2,3,1",
            correct_answer="2"
        ),
        Question(
            category="Programming-Java",
            question="Which keyword handles exceptions?",
            options="try,catch,throw,throws",
            correct_answer="try"
        ),
        Question(
            category="Programming-Java",
            question="What is JVM?",
            options="Java Virtual Machine,Java Variable Manager,Java Version Manager,Java Visual Machine",
            correct_answer="Java Virtual Machine"
        ),
        
        # Programming (HTML)
        Question(
            category="Programming-HTML",
            question="What does HTML stand for?",
            options="HyperText Markup Language,HighText Markup Language,HyperTool Markup Language,HomeText Markup Language",
            correct_answer="HyperText Markup Language"
        ),
        Question(
            category="Programming-HTML",
            question="Which tag creates a paragraph?",
            options="<p>,<div>,<span>,<h1>",
            correct_answer="<p>"
        ),
        Question(
            category="Programming-HTML",
            question="What is the correct tag for a hyperlink?",
            options="<a>,<link>,<href>,<url>",
            correct_answer="<a>"
        ),
        Question(
            category="Programming-HTML",
            question="Which attribute specifies the URL of a link?",
            options="href,src,link,url",
            correct_answer="href"
        ),
        Question(
            category="Programming-HTML",
            question="What does the <br> tag do?",
            options="Creates a line break,Bolds text,Italicizes text,Underlines text",
            correct_answer="Creates a line break"
        ),
        Question(
            category="Programming-HTML",
            question="Which tag is used for an image?",
            options="<img>,<picture>,<image>,<src>",
            correct_answer="<img>"
        ),
        Question(
            category="Programming-HTML",
            question="What does the <title> tag do?",
            options="Sets page title,Creates heading,Bolds text,Links CSS",
            correct_answer="Sets page title"
        ),
        Question(
            category="Programming-HTML",
            question="Which tag creates a numbered list?",
            options="<ol>,<ul>,<li>,<dl>",
            correct_answer="<ol>"
        ),
        Question(
            category="Programming-HTML",
            question="What is the default method of a form?",
            options="GET,POST,PUT,DELETE",
            correct_answer="GET"
        ),
        Question(
            category="Programming-HTML",
            question="Which tag defines a table row?",
            options="<tr>,<td>,<th>,<table>",
            correct_answer="<tr>"
        ),
        
        # Programming (CSS)
        Question(
            category="Programming-CSS",
            question="What does CSS stand for?",
            options="Cascading Style Sheets,Creative Style Sheets,Central Style Sheets,Colorful Style Sheets",
            correct_answer="Cascading Style Sheets"
        ),
        Question(
            category="Programming-CSS",
            question="How do you select an element by ID?",
            options="#id,.id,id,id()",
            correct_answer="#id"
        ),
        Question(
            category="Programming-CSS",
            question="Which property sets text color?",
            options="color,background-color,font-color,text-color",
            correct_answer="color"
        ),
        Question(
            category="Programming-CSS",
            question="What does 'margin: 0 auto' do?",
            options="Centers element,Sets margin to 0,Aligns text,Removes padding",
            correct_answer="Centers element"
        ),
        Question(
            category="Programming-CSS",
            question="Which property sets the font size?",
            options="font-size,text-size,size,font",
            correct_answer="font-size"
        ),
        Question(
            category="Programming-CSS",
            question="What is the default value of 'position'?",
            options="static,relative,absolute,fixed",
            correct_answer="static"
        ),
        Question(
            category="Programming-CSS",
            question="Which property adds space inside an element?",
            options="padding,margin,border,spacing",
            correct_answer="padding"
        ),
        Question(
            category="Programming-CSS",
            question="How do you apply a style to all <p> elements?",
            options="p,.p,#p,p()",
            correct_answer="p"
        ),
        Question(
            category="Programming-CSS",
            question="What does 'display: none' do?",
            options="Hides element,Shows element,Aligns element,Rotates element",
            correct_answer="Hides element"
        ),
        Question(
            category="Programming-CSS",
            question="Which property sets the background color?",
            options="background-color,color,background,bg-color",
            correct_answer="background-color"
        ),
        
        # Puzzles
        Question(
            category="Puzzles",
            question="If a plane crashes on the border of two countries, where do they bury the survivors?",
            options="Country A,Country B,You don't bury survivors,Border",
            correct_answer="You don't bury survivors"
        ),
        Question(
            category="Puzzles",
            question="How many months have 28 days?",
            options="1,12,6,3",
            correct_answer="12"
        ),
        Question(
            category="Puzzles",
            question="What has keys but can't open locks?",
            options="Piano,Keyboard,Map,Book",
            correct_answer="Piano"
        ),
        Question(
            category="Puzzles",
            question="I speak without a mouth and hear without ears. What am I?",
            options="Echo,Shadow,Ghost,Wind",
            correct_answer="Echo"
        ),
        Question(
            category="Puzzles",
            question="What gets wetter as it dries?",
            options="Towel,Sponge,Umbrella,Cloth",
            correct_answer="Towel"
        ),
        Question(
            category="Puzzles",
            question="What has a neck but no head?",
            options="Shirt,Bottle,Jar,Glass",
            correct_answer="Shirt"
        ),
        Question(
            category="Puzzles",
            question="What comes once in a minute, twice in a moment?",
            options="M,O,N,T",
            correct_answer="M"
        ),
        Question(
            category="Puzzles",
            question="What has cities but no houses?",
            options="Map,Globe,Atlas,All of the above",
            correct_answer="Map"
        ),
        Question(
            category="Puzzles",
            question="What can travel around the world while staying in a corner?",
            options="Stamp,Letter,Email,Passport",
            correct_answer="Stamp"
        ),
        Question(
            category="Puzzles",
            question="What has one eye but cannot see?",
            options="Needle,Cyclone,Camera,Clock",
            correct_answer="Needle"
        ),
        
        # Mathematical Questions
        Question(
            category="Mathematical Questions",
            question="What is 2 + 2 * 2?",
            options="6,8,10,12",
            correct_answer="6"
        ),
        Question(
            category="Mathematical Questions",
            question="What is the square root of 16?",
            options="2,4,8,16",
            correct_answer="4"
        ),
        Question(
            category="Mathematical Questions",
            question="What is 5 factorial?",
            options="120,60,20,25",
            correct_answer="120"
        ),
        Question(
            category="Mathematical Questions",
            question="What is 10% of 200?",
            options="10,20,30,40",
            correct_answer="20"
        ),
        Question(
            category="Mathematical Questions",
            question="Solve: 2x + 3 = 7",
            options="x=1,x=2,x=3,x=4",
            correct_answer="x=2"
        ),
        Question(
            category="Mathematical Questions",
            question="What is the value of π (pi) to two decimals?",
            options="3.14,3.16,3.12,3.18",
            correct_answer="3.14"
        ),
        Question(
            category="Mathematical Questions",
            question="What is 7^2?",
            options="14,21,49,56",
            correct_answer="49"
        ),
        Question(
            category="Mathematical Questions",
            question="What is the sum of angles in a triangle?",
            options="90°,180°,270°,360°",
            correct_answer="180°"
        ),
        Question(
            category="Mathematical Questions",
            question="What is 15 divided by 3?",
            options="3,4,5,6",
            correct_answer="5"
        ),
        Question(
            category="Mathematical Questions",
            question="What is the LCM of 6 and 8?",
            options="12,24,36,48",
            correct_answer="24"
        ),
    ]
    db.session.bulk_save_objects(questions)
    db.session.commit()

@app.route('/')
def index():
    categories = [
        "General Knowledge",
        "Indian Constitution",
        "Programming",
        "Puzzles",
        "Mathematical Questions"
    ]
    return render_template('index.html', categories=categories)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    try:
        print("Received POST request to /start_quiz")  # Log request
        print("Form data:", request.form)  # Log form data
        category = request.form['category']
        # For Programming, use sub_category; otherwise, use category
        sub_category = request.form.get('sub_category', category) if category == "Programming" else category
        print(f"Category: {category}, Sub-category: {sub_category}")  # Log values
        session['category'] = sub_category
        session['score'] = 0
        session['question_index'] = 0
        session['user_answers'] = {}  # Store user answers for navigation
        session['quiz_finished'] = False

        # Get 10 random questions
        questions = Question.query.filter_by(category=sub_category).all()
        if not questions:
            print(f"No questions found for category: {sub_category}")
            return jsonify({'error': 'No questions available for this category'}), 400

        # Ensure 10 questions
        if len(questions) < 10:
            questions = questions * (10 // len(questions) + 1)
        random.shuffle(questions)
        session['questions'] = [{
            'id': q.id,
            'question': q.question,
            'options': q.options.split(','),
            'correct_answer': q.correct_answer
        } for q in questions[:10]]

        print("Questions stored in session:", session['questions'])  # Log questions
        return jsonify({'redirect': '/quiz'})
    except KeyError as e:
        print(f"Error: Missing form field {str(e)}")  # Log missing field
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Log unexpected errors
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/quiz')
def quiz():
    if 'questions' not in session:
        print("No questions in session, redirecting to /")
        return redirect('/')
    return render_template('quiz.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    index = session.get('question_index', 0)
    if session.get('quiz_finished', False):
        print("Quiz finished, redirecting to result")
        return jsonify({'finished': True})
    if index >= len(session['questions']):
        session['quiz_finished'] = True
        print("Quiz finished, all questions answered")
        return jsonify({'finished': True})
    question = session['questions'][index]
    user_answer = session['user_answers'].get(str(index), '')
    return jsonify({
        'question': question['question'],
        'options': question['options'],
        'index': index + 1,
        'total': len(session['questions']),
        'user_answer': user_answer
    })

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    try:
        index = session.get('question_index', 0)
        user_answer = request.form.get('answer', '')
        print(f"Submitting answer for question {index + 1}: {user_answer}")
        
        if user_answer:  # Only score if an answer is provided
            correct_answer = session['questions'][index]['correct_answer']
            print(f"User answer: {user_answer}, Correct answer: {correct_answer}")
            if user_answer == correct_answer and str(index) not in session['user_answers']:
                session['score'] += 10
            session['user_answers'][str(index)] = user_answer
            session.modified = True
        
        return jsonify({'correct': user_answer == correct_answer if user_answer else False})
    except KeyError as e:
        print(f"Error in submit_answer: Missing form field {str(e)}")
        return jsonify({'error': f'Missing field: {str(e)}'}), 400

@app.route('/set_question_index', methods=['POST'])
def set_question_index():
    try:
        new_index = int(request.form['index']) - 1
        if 0 <= new_index < len(session['questions']):
            session['question_index'] = new_index
            session.modified = True
            print(f"Set question index to {new_index + 1}")
            return jsonify({'success': True})
        return jsonify({'error': 'Invalid question index'}), 400
    except Exception as e:
        print(f"Error setting index: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/finish_quiz', methods=['POST'])
def finish_quiz():
    try:
        score = Score(
            user="anonymous",
            category=session['category'],
            score=session['score']
        )
        db.session.add(score)
        db.session.commit()
        print(f"Quiz completed, score: {session['score']}, category: {session['category']}")
        session['quiz_finished'] = True
        return jsonify({'redirect': '/result'})
    except Exception as e:
        print(f"Error finishing quiz: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/result')
def result():
    score = session.get('score', 0)
    category = session.get('category', '')
    print(f"Rendering result: score={score}, category={category}")
    session.clear()
    return render_template('result.html', score=score, category=category)

@app.route('/leaderboard')
def leaderboard():
    scores = Score.query.order_by(Score.score.desc()).limit(10).all()
    return render_template('leaderboard.html', scores=scores)

@app.errorhandler(404)
def page_not_found(e):
    print(f"404 error: {str(e)}")  # Log 404 errors
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        init_db()
    port = int(os.getenv('PORT', 5000))
    app.run(host='127.0.0.1', port=port, debug=True)