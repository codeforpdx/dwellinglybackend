from flask import Flask
from flask_restful import Resource, reqparse
from flask_mail import Message
from flask_jwt_extended import jwt_required, get_jwt_claims


class Email(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('recipient')
    parser.add_argument('title') 
    parser.add_argument('body') 

    # @jwt_required
    @app.mail
    def post(self):
        #check if is_admin exist if not discontinue function
        # claims = get_jwt_claims() 
        
        # if not claims['is_admin']:
        #     return {'Message', "Admin Access Required"}, 401

        data = Email.parser.parse_args()

        if not data.recipient or not data.title or not data.body:
            return {'Message': 'Bad Request'}, 400
        
        #TODO parse recipients to ensure it is a valid email
        #TODO add feature to send to multiple people

        message = Message(data.title)
        message.recipients = data.recipient
        message.body = data.body
        mail.send(messsage)

        return {"Message": "Message Sent"}




        

