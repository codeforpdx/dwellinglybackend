from flask import Flask
from flask_restful import Resource, reqparse
from flask_mail import Message
from flask_jwt_extended import jwt_required, get_jwt_claims
import app
from models.user import UserModel

class Email(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('userid')
    parser.add_argument('title') 
    parser.add_argument('body') 

    @jwt_required
    def post(self):
        check if is_admin exist if not discontinue function
        claims = get_jwt_claims() 
        
        if not claims['is_admin']:
            return {'Message', "Admin Access Required"}, 401

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

        app.mail.send(message)
        return {"Message": "Message Sent"}




        

