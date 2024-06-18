from models import db, Workspace, WorkspaceDetails, Question
import datetime

def get_question(question_data):
    question_text = question_data.get('text')
    question = Question.query.filter_by(text=question_text).first()
    if question:
        return {
            'question_desc': question.text,
            'correct_answer': 'Some answer',  # This needs to be dynamically retrieved or computed
            'question_id_if_in_database': question.id,
            'feedback_from_AI_json': {
                'feedback': 'Good job! You have written the correct query',
                'AI_rating': 5
            },
            'question_level': 1
        }
    else:
        # Here you would generate the question using AI and save it to the database
        new_question = Question(text=question_text, topic=question_data.get('topic'))
        db.session.add(new_question)
        db.session.commit()
        return {
            'question_desc': new_question.text,
            'correct_answer': 'Generated answer',  # Replace with actual answer
            'question_id_if_in_database': new_question.id,
            'feedback_from_AI_json': {
                'feedback': 'Generated feedback',
                'AI_rating': 5
            },
            'question_level': 1
        }

def save_last_access_time(workspace_id):
    workspace = Workspace.query.get(workspace_id)
    workspace.last_access_date = datetime.datetime.utcnow()
    db.session.commit()

def generate_graph_data(workspace_id):
    details = WorkspaceDetails.query.filter_by(workspace_id=workspace_id).all()
    num_questions_attempted = len(details)
    num_questions_correct = sum(1 for detail in details if detail.correct_boolean)
    # Assuming we have a topic rating calculation logic
    topic_rating = sum(detail.AI_rating for detail in details if detail.AI_rating) / len(details)
    return {
        'num_questions_attempted': num_questions_attempted,
        'num_questions_correct': num_questions_correct,
        'topic_rating': topic_rating
    }
