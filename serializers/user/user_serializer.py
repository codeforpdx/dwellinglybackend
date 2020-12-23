
from schemas import UserSchema
 
class UserSerializer:
   @staticmethod
   def serialize(user):
       return UserSchema().dump(user)
 
   exclude=("hash_digest","password","lastActive")