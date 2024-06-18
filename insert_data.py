from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db, Topic, Question

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://test_rybf_user:sv03qDGkwfnxR3gJMHzXeIwAJAQx72v1@dpg-cpkiq7a0si5c73crc8m0-a.singapore-postgres.render.com/test_rybf"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def insert_data():
    with app.app_context():
        # Create tables (if they do not exist already)
        db.create_all()

        # Define topics and questions data
        topics_data = [
            # {
            #     "name": "Basic SQL",
            #     "questions": [
            #         {"id": 1, "text": "What is SQL?", "topic_id": [1]},
            #         {"id": 2, "text": "What is a primary key?", "topic_id": [1]},
            #         {"id": 3, "text": "Explain the SELECT statement.", "topic_id": [1]},
            #         {"id": 4, "text": "What is a foreign key?", "topic_id": [1]},
            #         {
            #             "id": 5,
            #             "text": "Explain the INSERT INTO statement.",
            #             "topic_id": [1],
            #         },
            #         {"id": 6, "text": "What is a database?", "topic_id": [1]},
            #         {"id": 7, "text": "What is a table in SQL?", "topic_id": [1]},
            #         {"id": 8, "text": "Explain the DELETE statement.", "topic_id": [1]},
            #         {"id": 9, "text": "What is a JOIN in SQL?", "topic_id": [1]},
            #         {"id": 10, "text": "What is normalization?", "topic_id": [1]},
            #         {
            #             "id": 11,
            #             "text": "Explain the UPDATE statement.",
            #             "topic_id": [1],
            #         },
            #         {"id": 12, "text": "What is a unique key?", "topic_id": [1]},
            #     ],
            # },
            {
                "name": "Advanced SQL",
                "questions": [
                    {"id": 13, "text": "Explain the GROUP BY clause.", "topic_id": [2]},
                    {"id": 14, "text": "What is a subquery?", "topic_id": [2]},
                    {"id": 15, "text": "Explain the HAVING clause.", "topic_id": [2]},
                    {"id": 16, "text": "What are indexes?", "topic_id": [2]},
                    {"id": 17, "text": "What is a view?", "topic_id": [2]},
                    {"id": 18, "text": "Explain the UNION operator.", "topic_id": [2]},
                    {"id": 19, "text": "What is a trigger?", "topic_id": [2]},
                    {"id": 20, "text": "What is a stored procedure?", "topic_id": [2]},
                    {"id": 21, "text": "Explain the CASE statement.", "topic_id": [2]},
                    {"id": 22, "text": "What is a cursor?", "topic_id": [2]},
                    {"id": 23, "text": "Explain the EXISTS operator.", "topic_id": [2]},
                    {"id": 24, "text": "What are transactions?", "topic_id": [2]},
                ],
            },
            {
                "name": "SQL Performance",
                "questions": [
                    {"id": 25, "text": "How to optimize a SQL query?", "topic_id": [3]},
                    {
                        "id": 26,
                        "text": "What is query execution plan?",
                        "topic_id": [3],
                    },
                    {
                        "id": 27,
                        "text": "Explain the concept of indexing.",
                        "topic_id": [3],
                    },
                    {"id": 28, "text": "What is query optimization?", "topic_id": [3]},
                    {"id": 29, "text": "What are SQL hints?", "topic_id": [3]},
                    {"id": 30, "text": "Explain partitioning.", "topic_id": [3]},
                    {"id": 31, "text": "What is sharding?", "topic_id": [3]},
                    {
                        "id": 32,
                        "text": "How does indexing improve performance?",
                        "topic_id": [3],
                    },
                    {
                        "id": 33,
                        "text": "What is the cost-based optimizer?",
                        "topic_id": [3],
                    },
                    {"id": 34, "text": "What are statistics in SQL?", "topic_id": [3]},
                    {"id": 35, "text": "What is caching in SQL?", "topic_id": [3]},
                    {
                        "id": 36,
                        "text": "Explain the concept of materialized views.",
                        "topic_id": [3],
                    },
                ],
            },
            {
                "name": "Database Design",
                "questions": [
                    {"id": 37, "text": "What is database design?", "topic_id": [4]},
                    {"id": 38, "text": "Explain ER diagrams.", "topic_id": [4]},
                    {"id": 39, "text": "What is normalization?", "topic_id": [4]},
                    {
                        "id": 40,
                        "text": "Explain the concept of denormalization.",
                        "topic_id": [4],
                    },
                    {"id": 41, "text": "What is a schema?", "topic_id": [4]},
                    {
                        "id": 42,
                        "text": "Explain the concept of data modeling.",
                        "topic_id": [4],
                    },
                    {"id": 43, "text": "What is a relational model?", "topic_id": [4]},
                    {
                        "id": 44,
                        "text": "What are keys in database design?",
                        "topic_id": [4],
                    },
                    {
                        "id": 45,
                        "text": "Explain the concept of relationships in SQL.",
                        "topic_id": [4],
                    },
                    {"id": 46, "text": "What is a star schema?", "topic_id": [4]},
                    {"id": 47, "text": "What is a snowflake schema?", "topic_id": [4]},
                    {"id": 48, "text": "What are OLAP and OLTP?", "topic_id": [4]},
                ],
            },
            {
                "name": "SQL Security",
                "questions": [
                    {"id": 49, "text": "What is SQL injection?", "topic_id": [5]},
                    {
                        "id": 50,
                        "text": "How to prevent SQL injection?",
                        "topic_id": [5],
                    },
                    {"id": 51, "text": "What are SQL permissions?", "topic_id": [5]},
                    {
                        "id": 52,
                        "text": "Explain the concept of role-based access control.",
                        "topic_id": [5],
                    },
                    {
                        "id": 53,
                        "text": "What is data encryption in SQL?",
                        "topic_id": [5],
                    },
                    {
                        "id": 54,
                        "text": "What is TDE (Transparent Data Encryption)?",
                        "topic_id": [5],
                    },
                    {
                        "id": 55,
                        "text": "Explain the concept of SQL auditing.",
                        "topic_id": [5],
                    },
                    {"id": 56, "text": "What is a SQL firewall?", "topic_id": [5]},
                    {
                        "id": 57,
                        "text": "Explain the concept of data masking.",
                        "topic_id": [5],
                    },
                    {"id": 58, "text": "What is SQL authentication?", "topic_id": [5]},
                    {
                        "id": 59,
                        "text": "What is the principle of least privilege?",
                        "topic_id": [5],
                    },
                    {
                        "id": 60,
                        "text": "How to secure a SQL database?",
                        "topic_id": [5],
                    },
                ],
            },
        ]

        # Insert topics and questions into database
        # for topic_data in topics_data:
        #     topic = Topic(name=topic_data["name"])
        #     db.session.add(topic)
        #     db.session.commit()  # Commit topic to get topic.id
        for idx, topic_data in enumerate(topics_data):
            topic = Topic(id=idx + 2, name=topic_data['name'])
            db.session.add(topic)
            db.session.commit()
            for question_data in topic_data["questions"]:
                question = Question(
                    id=question_data["id"],
                    text=question_data["text"],
                    topic_id=topic.id,
                )
                db.session.add(question)

        db.session.commit()


if __name__ == "__main__":
    insert_data()
