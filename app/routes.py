import requests
from app import db
from app.models.task import Task
from app.models.goal import Goal 
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


### WAVE 1 ###

@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        title_query = request.args.get("sort")
        #print(title_query)
        ### WAVE 2 ###
        if title_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())
        elif title_query == "asc":
            tasks = Task.query.order_by(Task.title.asc())
        ### end of WAVE 2 ###
        else:
            tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": False if task.completed_at == None else task.completed_at
            })
        return jsonify(tasks_response)

    if request.method == "POST":
        request_body = request.get_json()

        print(request_body)
        # return request_body

        if ("title" not in request_body) or ("description" not in request_body) or ("completed_at" not in request_body):
            return make_response({
                "details": "Invalid data"
            }, 400)
        else: 
            new_task = Task(
                title = request_body["title"],
                description = request_body["description"],
                completed_at = None   
            )
        
            db.session.add(new_task)
            db.session.commit()

            return make_response({
                "task": {
                    "id": new_task.id,
                    "title": new_task.title,
                    "description": new_task.description,
                    "is_complete": False if new_task.completed_at == None else True  
                }
            }, 201)
  

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    if request.method == "GET":
        return make_response({
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": False 
            }
        })
    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]

        db.session.commit()
        return make_response({
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": False 
            }
        }, 200)
    
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({
            "details": f'Task {task.id} "{task.title}" successfully deleted'
        })

#################### WAVE 3 ######################## 

@tasks_bp.route("/<task_id>/complete", methods=["PATCH"])
def mark_complete(task_id):
    

    if request.method == "PATCH":
        task = Task.query.get(task_id)

        if task is None:
            return make_response("", 404)

        if task.completed_at:
            task.completed_at = None
            is_complete = False 
        else:
            task.completed_at = datetime.today()
            is_complete = True
            path = "https://slack.com/api/chat.postMessage"
            api_key = app.config["SLACK_TOKEN"]


        db.session.commit()
        return make_response({
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_complete 
            }
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

        print(request_body)
        # return request_body

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

    if request.method == "GET":
        return make_response({
            "goal": {
                "id": goal.id,
                "title": goal.title
            }
        })
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