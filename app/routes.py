import requests
from app import db
from app.models.task import Task
from app.models.goal import Goal 
import os
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


### WAVE 1 ###

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        title_query = request.args.get("sort")
        if title_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        elif title_query == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        else:
            tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append(task.to_dict())
        return jsonify(tasks_response)

    if request.method == "POST":
        request_body = request.get_json()

        if ("title" not in request_body) or ("description" not in request_body) or ("completed_at" not in request_body):
            return make_response({
                "details": "Invalid data"
            }, 400)
        else: 

            new_task = Task(
                title = request_body["title"],
                description = request_body["description"],
                completed_at = request_body["completed_at"] if "completed_at" in request_body else None
            )
        
            db.session.add(new_task)
            db.session.commit()

            return make_response({
                "task": new_task.to_dict()
            }, 201)

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)


    if request.method == "GET":

        return make_response({
            "task": task.to_dict()
        })

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]

        db.session.commit()
        return make_response({
            "task": task.to_dict()
        }, 200)
    
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({
            "details": f'Task {task.id} "{task.title}" successfully deleted'
        })

#################### WAVE 3 ######################## 

def slack_message_complete(message):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        "Authorization": f"Bearer {os.environ.get('SLACK_TOKEN')}"
    }
    params = { 
                'channel': "general",
                'text': message
    }

    print("sending message")
    message = requests.post(url, data=params, headers=headers)
    return message.json()


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    
    if request.method == "PATCH":
        task = Task.query.get(task_id)

        if task is None:
            return make_response("", 404)
        
        task.completed_at = datetime.today()
        slack_message_complete(f"Someone just completed the task {task.title}")

        db.session.commit()

        return make_response({"task": task.to_dict()}, 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    
    if request.method == "PATCH":
        task = Task.query.get(task_id)

        if task is None:
            return make_response("", 404)
        
        task.completed_at = None
        is_complete = False

        db.session.commit()
        return make_response({
            "task": task.to_dict()
        }, 200)

#################### WAVE 5 ######################## 

@goals_bp.route("", methods=["GET", "POST"])
def handle_goals():
    if request.method == "GET":
        goals = Goal.query.all()
        goals_response = []
        for goal in goals:
            goals_response.append({
                "id": goal.id,
                "title": goal.title
            })
        return jsonify(goals_response)

    if request.method == "POST":
        request_body = request.get_json()

        if ("title" not in request_body):
            return make_response({
                "details": "Invalid data"
            }, 400)
        else: 
            new_goal = Goal(
                title = request_body["title"] 
            )
        
            db.session.add(new_goal)
            db.session.commit()

            return make_response({
                "goal": {
                    "id": new_goal.id,
                    "title": new_goal.title,
                }
            }, 201)

@goals_bp.route("/<goal_id>", methods=["GET", "PUT", "DELETE"])
def handle_one_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal is None:
        return make_response("", 404)

    tasks = Task.query.join(Goal).filter(Task.goal_id == goal_id).all()
    task_list = []

    for task in tasks:
        task_list.append({
            task.to_dict()
        })

    if request.method == "GET":
        return make_response({
            "goal": {
                "id": goal.id,
                "title": goal.title
            }
        }, 200)

    elif request.method == "PUT":
        form_data = request.get_json()

        goal.title = form_data["title"]

        db.session.commit()
        return make_response({
            "goal": {
                "id": goal.id,
                "title": goal.title
            }
        }, 200)
    
    elif request.method == "DELETE":
        db.session.delete(goal)
        db.session.commit()
        return make_response({
            "details": f'Goal {goal.id} "{goal.title}" successfully deleted'
        })

#################### WAVE 6 ######################## 
@goals_bp.route("/<goal_id>/tasks", methods=["GET", "POST"])
def get_tasks_for_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if goal is None:
        return make_response("", 404)

    tasks = Task.query.join(Goal).filter(Task.goal_id == goal_id).all()
    task_list = []
    if tasks:
        for task in tasks:
            task_list.append(task.to_dict())

    if request.method == "GET":
        return make_response({
                "id": goal.id,
                "title": goal.title,
                "tasks": task_list 
        }, 200)
    
    elif request.method == "POST":
        form_data = request.get_json()
        goal.tasks = []

        task_ids = form_data["task_ids"]
        for task_id in task_ids:
            task = Task.query.get(task_id)
            goal.tasks.append(task)

        db.session.commit()

        return {
            "id": goal.id, 
            "task_ids": task_ids
        }



    
    

