from flask import request
from flask_restful import Resource
from models import db, Feedback

class FeedbackResource(Resource):
    def get(self, id=None):
        if id:
            feedback = Feedback.query.get_or_404(id)
            return feedback.serialize(), 200
        else:
            feedbacks = Feedback.query.all()
            return [feedback.serialize() for feedback in feedbacks], 200

    def post(self):
        data = request.get_json()
        new_feedback = Feedback(
            rating=data['rating'],
            comment=data['comment'],
            order_id=data['order_id']
        )
        db.session.add(new_feedback)
        db.session.commit()
        return new_feedback.serialize(), 201

    def put(self, id):
        feedback = Feedback.query.get_or_404(id)
        data = request.get_json()
        feedback.rating = data.get('rating', feedback.rating)
        feedback.comment = data.get('comment', feedback.comment)
        db.session.commit()
        return feedback.serialize(), 200

    def delete(self, id):
        feedback = Feedback.query.get_or_404(id)
        db.session.delete(feedback)
        db.session.commit()
        return {'message': 'Feedback deleted successfully'}, 200
