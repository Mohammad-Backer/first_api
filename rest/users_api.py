from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Users(Resource):

    def get(self):
        data = pd.read_csv('users.csv')
        return {'data':data.to_dict()} , 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('userId', required = True)
        parser.add_argument('name', required = True)
        parser.add_argument('city', required = True)

        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            return {
                'message':'user already exists'
            }, 401

        else:

            new_data = pd.DataFrame(
                {
                    'userId':args['userId'],
                    'name':args['name'],
                    'city':args['city'],
                    'locations':[[]]
                }
            )

            data = data.append(new_data, ignore_index=True)
            data.to_csv('users.csv',index=False)

            return {'data':data.to_dict()}, 200

    def put(self):

        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('userId', required=True)  # add args
        parser.add_argument('location', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('users.csv')
        
        if args['userId'] in list(data['userId']):
            # evaluate strings of lists to lists
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )
            # select our user
            user_data = data[data['userId'] == args['userId']]

            # update user's locations
            user_data['locations'] = user_data['locations'].values[0] \
                .append(args['location'])
            
            # save back to CSV
            data.to_csv('users.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the userId does not exist
            return {
                'message': f"'{args['userId']}' user not found."
            }, 404

    def delete(self):
        data = pd.read_csv('users.csv')
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required = True)
        args = parser.parse_args()

        if args['userId'] in list(data['userId']):
            data = data.set_index('userId')
            data = data.drop(args['userId'], axis=0)
            data.to_csv('users.csv',index=True)
            return{
                "data: ":data.to_dict()
            }, 200

        else:
            return{
                "message: ":f"user {args['userId']} is not found"
            }, 404


api.add_resource(Users, '/users')


if __name__ == '__main__':
    app.run()

