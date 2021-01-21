from flask import Flask #, request
from flask_restful import Api,Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)   #wrapping the app in api 
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
db=SQLAlchemy(app)

class VideoModel(db.Model):  #creating the schema
    id=db.Column(db.Integer,primary_key=True)  #setting id as the pk
    name=db.Column(db.String(100),nullable=False)  #column name with string size of 100 chars and null values disabled
    likes=db.Column(db.Integer,nullable=False) 
    views=db.Column(db.Integer,nullable=False) 

    def __repr__(self):    #string representation of the object(instance)
        return f"Video(name={name},views={views},likes={likes})"
#each row in the table is going to be an instance of the VideoModel

#db.create_all()   # to intiallize the tables/schema(after the database is intiallized comment this line)



video_put_arg = reqparse.RequestParser()
video_put_arg.add_argument('name',type=str,help='Name of the video required',required=True)  #help msg is returned if that respective args is not present.
video_put_arg.add_argument('views',type=str,help='Views of the video required',required=True)
video_put_arg.add_argument('likes',type=str,help='Likes of the video required',required=True)

#for updating, all fields are not necessary... only the fields you want to update and the id of the video is required :)
video_patch_arg = reqparse.RequestParser()
video_patch_arg.add_argument('name',type=str,help='Name of the video required')  #help msg is returned if that respective args is not present.
video_patch_arg.add_argument('views',type=str,help='Views of the video required')
video_patch_arg.add_argument('likes',type=str,help='Likes of the video required')


resource_fields={                    #defining the structure for the instance of VideoModel(a row in it) to be serialized.
    'id':fields.Integer,
    'name':fields.String,
    'likes':fields.Integer,
    'views':fields.Integer,
}

class Video(Resource):
    @marshal_with(resource_fields) #when we return the instance of VideoModel to 'result' serialize it w.r.t to the format(fields) provided in resource_fields (i.e converts the instance to a dict). 
    def get(self,video_id):
        result=VideoModel.query.filter_by(id=video_id).first()    #this return the valid column as an instance of the VideoModel
        # print(not result)
        if not result:
            abort(404,message='Video with this id doesnt exist')
        return result  #result will be a dict value now

    @marshal_with(resource_fields)
    def put(self,video_id):
        args=video_put_arg.parse_args()  #args is a dict    video_put_args.parse_args() will verify if all specified fields are present else trigger the help messasge.
        result=VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409,message='Video id already exist!')   #if video id already exist in db then abort.

        video=VideoModel(id=video_id,name=args['name'],views=args['views'],likes=args['likes'])
        db.session.add(video)  #adding the instance to the db.
        db.session.commit()  #commit the changes made in the db persistent
        return video,201   #using marshal_with the video instance is serialized to a dict.    

    #for updating the db
    @marshal_with(resource_fields)
    def patch(self,video_id):
        args=video_patch_arg.parse_args()  #args is a dict
        result=VideoModel.query.filter_by(id=video_id).first()    #this return the valid column as an instance of the VideoModel
        if not result:
            abort(404,message='Video with this id doesnt exist')
        
        if args['name']:
            result.name=args['name']
        if args['likes']:
            result.likes=args['likes']
        if args['views']:
            result.views=args['views']

        #db.session.add(result)  #no need of re-adding an instance (add is only requied the first time insertion of the instance). 
        db.session.commit()

        return result

    def delete(self,video_id):
        VideoModel.query.filter_by(id=video_id).delete()        
        db.session.commit()
        return '',204



api.add_resource(Video,'/video/<int:video_id>')  #adding resource to the api and setting the route
if (__name__ == '__main__'):
    app.run(debug=True)
