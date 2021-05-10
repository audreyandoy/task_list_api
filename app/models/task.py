from app import db 
from app.models.goal import Goal

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String)
    description = db.Column(db.String, nullable = False)
    completed_at = db.Column(db.DateTime, nullable=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=True)

    def to_dict(self):

        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at != None
        }

        if self.goal_id:
            task_dict["goal_id"] = self.goal_id 

        return task_dict 
