from flask import Flask, render_template, redirect, url_for, request, flash, send_file, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
import sqlite3
import json
import requests
from models import db, bcrypt, login_manager, User, Answer, Workspace, WorkspaceDetails, ChatWorkspace, ChatHistory
from assess import create_system_prompt, assess_query
import openai
from localStoragePy import localStoragePy
from flask_migrate import Migrate
from workspace_routes import workspace_bp
from openai import OpenAI
from flask_cors import CORS
# from defined_prompts import initial_assessment_prompt

from setopenai import setupopenai
setupopenai()

# Initialize the OpenAI client
client = OpenAI()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})  # Enable CORS for your frontend's origin
app.config['SECRET_KEY'] = 'd1056c7caffd817f811eb140761c7a50'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test_rybf_user:sv03qDGkwfnxR3gJMHzXeIwAJAQx72v1@dpg-cpkiq7a0si5c73crc8m0-a.singapore-postgres.render.com/test_rybf'
migrate = Migrate()
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate.init_app(app, db)

app.register_blueprint(workspace_bp, url_prefix='/workspace')

def load_questions_from_json(file_path):
    with open(file_path, 'r') as file:
        questions = json.load(file)
    return questions

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('topics'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('topics'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('initial_assessment'))
    return render_template('register.html')

@app.route('/initial_assessment', methods=['GET', 'POST'])
@login_required
def initial_assessment():
    questions = load_questions_from_json('questions.json')
    if request.method == 'POST':
        for question in questions:
            answer_text = request.form[f'question-{question["id"]}']
            rating = int(answer_text)  # Assuming answers are ratings for simplicity
            answer = Answer(user_id=current_user.id, question_id=question["id"], answer=answer_text, rating=rating)
            db.session.add(answer)
        db.session.commit()
        
        # Calculate user rating and set level
        total_rating = sum([answer.rating for answer in Answer.query.filter_by(user_id=current_user.id).all()])
        current_user.rating = total_rating
        if total_rating < 10:
            current_user.level = 'beginner'
        elif total_rating < 20:
            current_user.level = 'intermediate'
        else:
            current_user.level = 'advanced'
        
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('initial_assessment.html', questions=questions)

@app.route('/topics', methods=['GET', 'POST'])
@login_required
def topics():
    if request.method == 'POST':
        print("reached")
        localStorage = localStoragePy('sql_tutor')
        data = request.get_json()
        topic_index = int(data.get('topic_index'))
        print(topic_index)
        questions = load_questions_from_json('questions.json')
        selected_topic_questions = questions['topics'][topic_index]['questions']
        localStorage.setItem('selected_topic_questions', selected_topic_questions)
        return jsonify({'redirect': url_for('index')})
    else:
        questions = load_questions_from_json('questions.json')
        topics = [topic['name'] for topic in questions['topics']]
        return render_template('topics.html', topics=topics)

# # In-memory storage for chat history
# chat_history = []

# @app.route('/api/send_message', methods=['POST'])
# def send_message():
#     data = request.json
#     user_message = data.get('message')

#     if not user_message:
#         return jsonify({'error': 'No message provided'}), 400

#     # Add user message to chat history
#     chat_history.append({'role': 'user', 'content': user_message})

#     # Prepare the chat history for OpenAI
#     conversation = [{'role': msg['role'], 'content': msg['content']} for msg in chat_history]
#     print(conversation)
#     try:
#         completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=conversation
#     )
#         print(completion)
#         # Get the response from OpenAI
#         ai_message = completion.choices[0].message.content

#         # Add AI response to chat history
#         chat_history.append({'role': 'assistant', 'content': ai_message})
#         print(ai_message)

#         return jsonify({'message': ai_message})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @app.route('/api/chat_history', methods=['GET'])
# def get_chat_history():
#     return jsonify({'history': chat_history})

# In-memory storage for chat history
chat_history = []

def generate_question(conversation, question_type):
    if question_type == 'mcq':
        prompt = f"{conversation}\n\nPlease generate a {question_type} question in the following format with markdown with explanations for each options, just follow the format dont generate the same question, generate a sql query based question, also in question type it should be mcq or suggestions:\n\n" \
             "{\n  \"question\": \"The formation of new states in India falls under which of the following articles of the Constitution:\",\n" \
             "  \"type\": \ {question_type} \,\n" \
             "  \"options\": {\n" \
             "    \"A\": {\n" \
             "      \"value\": \"Article 3\",\n" \
             "      \"explanation\": \"**Context:** Hyderabad, one of the bustling metropolitan cities of the country, ceased to be the common capital of Telangana and Andhra Pradesh from Sunday as per the Andhra Pradesh Reorganisation Act, 2014.\\n\\n**Formation of new states:**\\nThe formation of new states in India falls under Article 3 of the Constitution. Parliament holds the power to create new states through legislation. However, such a bill can only be introduced on the recommendation of the President. Before recommending a bill that affects state boundaries or names, the President must consult the respective state legislatures. Parliament can enact laws to create new states with a simple majority.\",\n" \
             "      \"isCorrectOption\": true\n" \
             "    },\n" \
             "    \"B\": {\n" \
             "      \"value\": \"Article 12\",\n" \
             "      \"explanation\": null,\n" \
             "      \"isCorrectOption\": false\n" \
             "    },\n" \
             "    \"C\": {\n" \
             "      \"value\": \"Article 1\",\n" \
             "      \"explanation\": null,\n" \
             "      \"isCorrectOption\": false\n" \
             "    },\n" \
             "    \"D\": {\n" \
             "      \"value\": \"Article 15\",\n" \
             "      \"explanation\": null,\n" \
             "      \"isCorrectOption\": false\n" \
             "    }\n" \
             "  }\n" \
             " \"correctAnswer\": \ here comes the correct option, also make sure there is one correct answer} \,\n" \
             "}"
    else:
        prompt = f"{conversation}\n\nPlease generate a descriptive question in the following format with markdown, just follow the format dont generate the same question, generate a sql query based question.\n\n" \
             "{\n  \"question\": \"here will be a sql topic question you will generate\",\n" \
              "}"
        
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{'role': 'system', 'content': 'You are an assistant.'},
                  {'role': 'user', 'content': prompt}]
    )
    # print(response.choices[0].message.content)
    return response.choices[0].message.content

@app.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Add user message to chat history
    chat_history.append({'role': 'user', 'content': user_message})

    # Prepare the chat history for OpenAI
    conversation = [{'role': msg['role'], 'content': msg['content']} for msg in chat_history]

    try:
        # Call OpenAI API to generate a response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )

        # Get the response from OpenAI
        ai_message = response.choices[0].message.content

        # Add AI response to chat history
        chat_history.append({'role': 'assistant', 'content': ai_message})

        # Include suggestive buttons for question type selection
        suggestive_buttons = ['Generate MCQ', 'Generate Descriptive Question']

        return jsonify({
            'message': ai_message,
            'suggestions': suggestive_buttons
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_question', methods=['POST'])
def generate_question_endpoint():
    data = request.json
    question_type = data.get('question_type', 'descriptive')

    # Prepare the chat history for OpenAI
    conversation = [{'role': msg['role'], 'content': msg['content']} for msg in chat_history]

    try:
        question = generate_question(conversation, question_type)
        print(question)

        return jsonify({
            'question': question,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def evaluate_answer(question, selected_answer):
    prompt = f"Question: {question}\nSelected Answer: {selected_answer}\n\nIs the selected answer correct? Provide a detailed explanation."

    response = client.chat.completions.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()

@app.route('/api/chat_history', methods=['GET'])
def get_chat_history():
    return jsonify({'history': chat_history})

@app.route('/set_topic')
@login_required
def set_topic():
    localStorage = localStoragePy('sql_tutor')
    print(request.values.get('topic_index'))
    workspace_id = request.values.get('workspace_id')
    topic_index = request.values.get('topic_index')
    questions = load_questions_from_json('questions.json')
    topic_index = int(topic_index)
    print(topic_index)
    print(questions['topics'][topic_index])
    selected_topic_questions = questions['topics'][topic_index]['questions']
    
    localStorage.setItem('selected_topic_questions', selected_topic_questions)
    # return render_template('index.html', questions_json=selected_topic_questions, workspace_id=workspace_id, topic_index=topic_index)
    return redirect(url_for('index', questions_json=selected_topic_questions, workspace_id=workspace_id, topic_index=topic_index))
@app.route('/index')
@login_required
def index():
    questions = session.get('selected_topic_questions', [])
    questions_json = json.dumps(questions)  # Convert to JSON string
    workspace_id = request.values.get('workspace_id')
    topic_index= request.values.get('topic_index')
    return render_template('index.html', questions_json=questions_json, workspace_id=workspace_id, topic_index=topic_index)


@app.route('/generate_overall_feedback', methods=['POST'])
def generate_overall_feedback():
    data = request.get_json()
    feedbacks = data['feedbacks']
    combined_feedback = "\n\n".join(feedbacks)
    
    overall_feedback_prompt = f"Provide an overall feedback for the following SQL query feedbacks:\n{combined_feedback}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=overall_feedback_prompt,
        max_tokens=150
    )
    overall_feedback = response.choices[0].text.strip()
    
    return jsonify({'overall_feedback': overall_feedback})

@app.route('/download-db')
@login_required
def download_db():
    return send_file('sample_databases/your_sqlite_file.db', as_attachment=True)

@app.route('/submit-query', methods=['POST'])
@login_required
def submit_query():
    data = request.get_json()
    print(data)
    question = data['question']
    query = data['query']
    
    # Send the query and question ID to asses.py for processing
    prompt = create_system_prompt(question, query)
    response = assess_query(prompt)
    return {'feedback': response}

@app.route('/assess', methods=['POST'])
def assess():
    data = request.get_json()
    question_id = data['question_id']
    query = data['query']
    feedback = assess_query(question_id, query)
    
    return jsonify({'feedback': feedback})

@app.route('/evaluate_answer', methods=['POST'])
def evaluate_answer():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    # Here you will call OpenAI API to evaluate the answer
    prompt = f"Evaluate the following solution and provide a score out of 10. Just provide the number and no statement as i need to use it in progress bar Question: {question} Answer: {answer}"
    conversation_history = [
    {"role": "system", "content": prompt}]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    assistant_reply = completion.choices[0].message.content  # Extract suggestions from assistant_reply if available
    print(assistant_reply)
    # if assistant_reply.suggestions:
    #     suggestions = assistant_reply.suggestions
    # conversation_history.append({"role": "assistant", "content": assistant_reply.content, "suggestions": suggestions})
    return jsonify({"score": assistant_reply})
    # response = client.chat.completions.create(
    #     engine="text-davinci-003",
    #     prompt=prompt,
    #     max_tokens=50
    # )
    
    # # Extract the score from OpenAI response
    # score = response.choices[0].text.strip()

    # return jsonify({'score': score})
@app.route('/api/create_workspace', methods=['POST'])
def create_workspace():
    data = request.json
    new_workspace = ChatWorkspace(name=data['name'])
    db.session.add(new_workspace)
    db.session.commit()
    return jsonify({"id": new_workspace.id, "name": new_workspace.name})

@app.route('/api/get_workspaces', methods=['GET'])
def get_workspaces():
    workspaces =ChatWorkspace.query.all()
    return jsonify([{"id": ws.id, "name": ws.name} for ws in workspaces])

@app.route('/api/chat_history', methods=['GET'])
def chat_history():
    workspace_id = request.args.get('workspace')
    history = ChatHistory.query.filter_by(workspace_id=workspace_id).all()
    return jsonify({"history": [{"sender": h.sender, "text": h.text, "type": h.type} for h in history]})


if __name__ == '__main__':
    app.run(debug=True)
