from flask_sqlalchemy import SQLAlchemy
# from models.user import UserModel
# from models.property import PropertyModel
# from models.revoked_tokens import RevokedTokensModel
db = SQLAlchemy()

# def seedData():
#     user = UserModel(email="user1@dwellingly.org", role="admin", firstname="user1", lastname="tester", password="1234", archived=0)
#     db.session.add(user)
#     user = UserModel(email="user2@dwellingly.org", role="admin", firstname="user2", lastname="tester", password="1234", archived=0)
#     db.session.add(user)
#     user = UserModel(email="user3@dwellingly.org", role="admin", firstname="user3", lastname="tester", password="1234", archived=0)
#     db.session.add(user)

#     newProperty = PropertyModel(name="test1", address="123 NE FLanders St", city="Portland", state="OR", zipcode="97207", tenants=3, dateAdded="2020-04-12", archived=0)
#     db.session.add(newProperty)

#     revokedToken = RevokedTokensModel(jti="855c5cb8-c871-4a61-b3d8-90249f979601")
#     db.session.add(revokedToken)