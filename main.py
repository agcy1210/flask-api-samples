from flask import Flask, request
from flask_restful import Api, Resource, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

# define where to save db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/database.db'
db = SQLAlchemy(app)

# api


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"name: {name}, likes: {likes}, views: {views}"


# api
class HelloWorldApi(Resource):
    def get(self, name, age):
        return {"name": f"Hello {name}", "age": age}

    def post(self):
        return {"data": "Hello World Posted"}


resource_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "views": fields.Integer,
    "likes": fields.Integer
}


class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not found video with that id")
        return result

    @marshal_with(resource_fields)
    def post(self, video_id):
        body = request.form
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video id already taken")

        video = VideoModel(id=video_id, name=body['name'], likes=body['likes'], views=body['views'])
        db.session.add(video)
        db.session.commit()

        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        body = request.form
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, 'Video doesnot exist with given id')

        if "name" in body:
            result.name = body['name']
        if "views" in body:
            result.views = body['views']
        if "likes" in body:
            result.likes = body['likes']

        db.session.commit()

        return result

    def delete(self, video_id):
        return '', 204
        # 204 ->  deleted successfully


api.add_resource(HelloWorldApi, "/hello/<string:name>/<int:age>")
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
