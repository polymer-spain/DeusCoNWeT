import sys
import os
sys.path.insert(1, 'api_handlers/')
from  mongoDB import User, Session, UserComponent, Token, SocialUser


MODE = os.getenv('VERSION', 'test')

if MODE == "test":
  User.drop_collection()
  Session.drop_collection()
  UserComponent.drop_collection()
  Token.drop_collection()
  SocialUser.drop_collection()
