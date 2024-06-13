from app import app, db
from models import User, Question

with app.app_context():
    db.create_all()
    
    # Add initial questions if not already present
    if not Question.query.first():
        questions = [
            Question(text="How confident are you with SELECT statements?", topic="SELECT"),
            Question(text="How confident are you with JOIN operations?", topic="JOIN"),
            Question(text="How much experience do you have with SQL?", topic="Experience"),
            # Add more questions as needed
        ]
        db.session.bulk_save_objects(questions)
        db.session.commit()

    # Add a default user for testing
    if not User.query.filter_by(username='testuser').first():
        user = User(username='testuser')
        user.set_password('testpassword')
        db.session.add(user)
        db.session.commit()
