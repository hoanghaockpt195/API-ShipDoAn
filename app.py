from flask import Flask
import mlab
from flask_restful import Resource,Api
from resouce.food_res import FoodRest,FoodRestInfo,FoodRestList,UserRestList, UserRestFacebookList,UserRest, OrderRestList,  OrderRest,UserINFRest
from flask_jwt import JWT, jwt_required
from model.food import Food
from model.user import User
from model.order import Order
mlab.connect()

app = Flask(__name__)
api = Api(app)
app.config["SECRET_KEY"]="SHIP DO AN DEM"
# user = User(username = "khanh", password = "pham")
# user.save()

api.add_resource(FoodRestList,"/food")
api.add_resource(FoodRest,"/food/<food_id>")
api.add_resource(FoodRestInfo,"/food/info/<food_id>")
api.add_resource(UserRestList,"/users")
api.add_resource(UserINFRest,"/userinfo")

api.add_resource(UserRestFacebookList,"/users/facbook")
api.add_resource(UserRest,"/users/spend/<user_id>")
api.add_resource(OrderRestList,"/order")
api.add_resource(OrderRest,"/order/<order_id>")


class LoginCredentials(Resource):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def authenticate(username, password):
        for user in User.objects().filter(username=username):
            if user.password == password:
                return LoginCredentials(str(user.id), user.username, user.password)

    def identity(payload):
        user_id = payload["identity"]
        user = User.objects().with_id(user_id)
        if (user_id is not None):
            return LoginCredentials(str(user.id), user.username, user.password)

    jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)

@app.route('/')
def hello_world():
    return 'Hello to ship do an nhanh app'


@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    return response

if __name__ == '__main__':
    app.run()
