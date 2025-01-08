**Test API using Postman**

Add the base URL of your API (e.g., http://127.0.0.1:5000)

**For Registration Endpoint**
  Endpoint: POST /registration
  Method: POST
  URL: http://127.0.0.1:5000/registration
  On Body (JSON) provide username and password. eg.
    {
    "username": "testuser",
    "password": "password123"
    }
    Expected Response:
    {
    "message": "User Created Successfully"
    }
**For Login Endpoint**
  Endpoint: POST /login
  Purpose: Log in and receive a JWT token.
  Method: POST
  URL: http://127.0.0.1:5000/login
   On Body (JSON) provide username and password. same as registration eg.
    {
    "username": "testuser",
    "password": "password123"
    } 
    Expected Response:
    {
    "access_token": "your-jwt-token"
    }
     Copy the access_token for use in future requests.

 **Create Blog Endpoint**
     Endpoint: POST /create_blog
     Method: POST
    URL: http://127.0.0.1:5000/create_blog
    Headers:
    Authorization: Bearer <access_token>
    On Body (JSON):
      {
      "title": "My First Blog",
      "description": "This is a description of my first blog."
      }
      
      Expected Response:
      {
          "message": "Blog created successfully",
          "blog": {
              "id": 1,
              "title": "My First Blog",
              "description": "This is a description of my first blog.",
              "author": "testuser",
              "author_id": 1
          }
      }
**Update Blog Endpoint**
    Endpoint: PUT /update/<id>
    Method: PUT
    URL: http://127.0.0.1:5000/update/1
    Headers:
    Authorization: Bearer <access_token>
    Body (JSON)
      {
      "title": "Updated Blog Title",
      "description": "Updated description."
      }
      
    Expected Response:
      {
          "message": "Blog updated successfully",
          "blog": {
              "id": 1,
              "title": "Updated Blog Title",
              "description": "Updated description.",
              "author": "testuser",
              "author_id": 1
          }
      }
**Delete Blog Endpoint**
    Endpoint: DELETE /delete/<id>
    Method: DELETE
    URL: http://127.0.0.1:5000/delete/1
    Headers:
    Authorization: Bearer <access_token>
    
    Expected Response:
      {
    "message": "Blog deleted successfully"
      }

**Get All Blogs in homepage With Pagination**
    Endpoint: GET /homepage
    Method: GET
    URL: http://127.0.0.1:5000/homepage?page=1&per_page=3
    
    Expected Response:
        {
        "data": [
            {
                "id": 1,
                "title": "My First Blog",
                "description": "This is a description of my first blog.",
                "author": "testuser",
                "author_id": 1
            }
        ],
        "meta": {
            "current_page": 1,
            "per_page": 3,
            "total_items": 1,
            "total_pages": 1
        },
        "links": {
            "next": null,
            "prev": null
        }
    }

**Get Single Blog on Separate page**
    Endpoint: GET /single_blog/<id>
    Method: GET
    URL: http://127.0.0.1:5000/single_blog/1
    
    Expected Response
        {
        "blog": {
            "id": 1,
            "title": "My First Blog",
            "description": "This is a description of my first blog.",
            "author": "testuser",
            "author_id": 1
        }
      }

**Logout Endpoint**
    Endpoint: POST /logout
    Method: POST
    URL: http://127.0.0.1:5000/logout
    Headers:
    Authorization: Bearer <access_token>
    
    Expected Response
      {
      "message": "logged out Success"
      }
      




    

    

  
