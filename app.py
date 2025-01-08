from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy 
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, get_jwt


app = Flask(__name__)

app.config["SECRET_KEY"] = "MY-SECRET-KEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog_db.sqlite"
db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

# Store blacklisted tokens
blacklisted_tokens = set()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    author = db.Column(db.String(100), db.ForeignKey('user.username'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def blog_dic(self):
        return{
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "author": self.author,
            "author_id": self.author_id,
        }

# Initializing database
with app.app_context():
    db.create_all()

# function to check if token is blacklisted
@jwt.token_in_blocklist_loader
def check_if_token_is_blacklisted(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blacklisted_tokens

class Registration(Resource):
    def post(self):
        try:
            data = request.get_json() 
            print("Request Data:", data)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return {'message' : 'Missing username or password'}, 400
            if User.query.filter_by(username=username).first():
                return {'message' : 'Username already exists'}, 400
            
            # Create new user
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return {'message' : 'User Created Successfully'}, 200

        except Exception as e:
            return {'error': str(e)}, 500

class UserLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            username = data['username']
            password = data['password']

            user = User.query.filter_by(username=username).first()

            if user and user.password == password:
                access_token =  create_access_token(identity=str(user.id))
                return {'access_token' : access_token}, 200
            return {'message' : 'Invalid username or password'}, 401
        
        except Exception as e:
            return {'error': str(e)}, 500

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        # add token to the blocklist
        blacklisted_tokens.add(jti)
        return {'message': 'logged out Success'}, 200
        
# Blog Create
class CreateBlogAPI(Resource):
    @jwt_required()
    def post(self):
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            title = data['title']
            description = data['description']
            
            if not title or not description:
                return {"message": " Enter Title and Description"}, 400

            user = User.query.get(current_user_id)
            if not user:
                return {"message": "User not found"}, 404
            blog = Blog(title=title, description=description, author=user.username, author_id=user.id)
            db.session.add(blog)
            db.session.commit()
            return {"message": "Blog created successfully", "post": blog.blog_dic()}, 201
            
        except Exception as e:
            return {'error': str(e)}, 500

# Blog Update
class UpdateBlogAPI(Resource):
    @jwt_required()
    def put(self, id):
        try:
            current_user_id = get_jwt_identity()
            blog = Blog.query.get(id)
            if not blog:
                return {"message": "Blog not found"}, 404
            if blog.author_id != int(current_user_id):
                return {"message": "You don't have permission to edit"}, 403
            data = request.get_json()
            blog.title = data.get("title", blog.title)
            blog.content = data.get("description", blog.description)
            db.session.commit()
            return {"message": "Blog updated successfully", "post": blog.blog_dic()}, 200
        except Exception as e:
            return {'error': str(e)}, 500
    
# Blog Delete
class DeleteBlogAPI(Resource):
    @jwt_required()
    def delete(self, id):
        try:
            current_user_id = get_jwt_identity()
            blog = Blog.query.get(id)
            if not blog:
                return {"message": "Post not found"}, 404
            if blog.author_id != int(current_user_id):
                return {"message": "You don't have permission to delete"}, 403
            db.session.delete(blog)
            db.session.commit()
            return {"message": "Blog deleted successfully"}, 200
        except Exception as e:
            return {'error': str(e)}, 500

# All Blogs
class AllBlogs(Resource):
    def get(self):
        try:
            page = int(request.args.get('page', 1))
            per_page = int(request.args.get('per_page', 3))
            blogs_query = Blog.query.paginate(page=page, per_page=per_page)
            blogs = [blog.blog_dic() for blog in blogs_query.items]

            response = {
                "data": blogs,
                "meta": {
                "current_page": page,
                "per_page": per_page,
                "total_items": blogs_query.total,
                "total_pages": blogs_query.pages
            },
              "links": {
                "next": f"{request.base_url}?page={page + 1}&per_page={per_page}" if blogs_query.has_next else None,
                "prev": f"{request.base_url}?page={page - 1}&per_page={per_page}" if blogs_query.has_prev else None
            }
            }
            return response, 200
        except Exception as e:
            return {'error': str(e)}, 500
            

# Single Blog Page
class SingleBlogPage(Resource):
    def get(self, id):
        blog = Blog.query.get(id)
        if not blog:
            return {"message": "Post not found"}, 404
        return {"post": blog.blog_dic()}, 200

# Routing resources
api.add_resource(Registration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(AllBlogs, '/homepage')
api.add_resource(CreateBlogAPI, "/create_blog")
api.add_resource(UpdateBlogAPI, "/update/<int:id>")
api.add_resource(DeleteBlogAPI, "/delete/<int:id>")
api.add_resource(SingleBlogPage, "/single_blog/<int:id>")

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return {'message': 'Resource not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'message': 'Internal server error'}, 500


if __name__ == "__main__":
    app.run(debug=True)