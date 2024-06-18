from flask import Blueprint, request, jsonify, url_for
from models import db, Workspace, WorkspaceDetails, Question, Topic
from workspace_service import get_question, save_last_access_time, generate_graph_data
from flask_login import login_required, current_user

workspace_bp = Blueprint("workspace_bp", __name__)


@workspace_bp.route("/workspace/<int:workspace_id>", methods=["GET"])
@login_required
def show_workspace(workspace_id):
    workspace = Workspace.query.get_or_404(workspace_id)
    return jsonify(workspace)


@workspace_bp.route("/workspace/<int:workspace_id>/details", methods=["GET"])
@login_required
def show_workspace_details(workspace_id):
    details = WorkspaceDetails.query.filter_by(workspace_id=workspace_id).all()
    return jsonify(details)


@workspace_bp.route("/workspace/<int:workspace_id>/last_access", methods=["PUT"])
@login_required
def update_last_access(workspace_id):
    save_last_access_time(workspace_id)
    return jsonify({"message": "Last access time updated"})


@workspace_bp.route("/workspace/<int:workspace_id>/progress", methods=["GET"])
@login_required
def get_progress_data(workspace_id):
    data = generate_graph_data(workspace_id)
    return jsonify(data)


@workspace_bp.route("/question", methods=["GET"])
@login_required
def get_or_generate_question():
    question_data = request.json
    question = get_question(question_data)
    return jsonify(question)


# New endpoint to create a workspace
@workspace_bp.route("/create_workspace", methods=["POST"])
@login_required
def create_workspace():
    data = request.get_json()
    print(data)
    topic_id = data.get("topic_id")
    print(topic_id)

    if topic_id is None:
        return jsonify({"error": "Topic ID is required"}), 400

    # # Check if workspace already exists for the user and topic
    # existing_workspace = Workspace.query.filter(
    #     Workspace.user_id == current_user.id,
    #     Workspace.workspace_topics.any(topic_id)
    # ).first()

    # if existing_workspace:
    #     workspace_id = existing_workspace.id
    # else:
    new_workspace = Workspace(user_id=current_user.id, workspace_topics= topic_id)
    db.session.add(new_workspace)
    db.session.commit()
    workspace_id = new_workspace.id

    return jsonify({
        'redirect': url_for('set_topic', workspace_id=workspace_id, topic_index=topic_id)
    })


# New endpoint to get questions by topic
@workspace_bp.route("/topics/<int:topic_id>/questions", methods=["GET"])
@login_required
def get_questions_by_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    questions = Question.query.filter_by(topic_id=topic_id).all()
    questions_list = [{"id": q.id, "text": q.text} for q in questions]
    return jsonify({"topic": topic.name, "questions": questions_list})

@workspace_bp.route("/workspaces", methods=["GET"])
@login_required
def get_user_workspaces():
    user_workspaces = Workspace.query.filter_by(user_id=current_user.id).all()
    # workspaces_data = [
    #     {
    #         "id": workspace.id,
    #         "topics": [topic.id for topic in workspace.workspace_topics],
    #     }
    #     for workspace in user_workspaces
    # ]
    workspaces_data = []
    for workspace in user_workspaces:
        print(workspace.id)
        workspaces_data.append({
            "id": workspace.id,
            "topics": workspace.workspace_topics,
        })
    print(workspaces_data)
    return jsonify(workspaces_data)
