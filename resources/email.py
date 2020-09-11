from flask import Flask, current_app
from flask_restful import Resource, reqparse
from flask_mail import Message
from resources.admin_required import admin_required
from models.user import UserModel

class Email(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('userid')
    parser.add_argument('title') 
    parser.add_argument('body') 

    @admin_required
    def post(self):
        data = Email.parser.parse_args()

        if not data.userid or not data.title or not data.body:
            return {'Message': 'Bad Request'}, 400

        #TODO add feature to send to multiple emails
    
        message = Message(data.title, sender="noreply@codeforpdx.org", body=data.body )
        
        user = UserModel.find_by_id(data.userid)
        if user.email:
            message.recipients = [user.email] 
        else:
            return {'Message': 'Bad Request'}, 400

        current_app.mail.send(message)
        return {"Message": "Message Sent"}


    @staticmethod
    def send_reset_password_msg(user):
        pass
