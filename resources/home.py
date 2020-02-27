from flask import Flask
from flask_restful import Resource

class Home(Resource):
    def get(self):
        return "Dwellingly is up and Running"
