# accuknox

**Installation**

1. Make sure you have `Python 3` installed on your system.
  
Inside project root directory, run following commands:

**Dependency installation:**

      pip install -r requirements.txt

**For to start server:**

      python manage.py runserver


**API for signup:**

      POST : http://127.0.0.1:8000/social-network/signup/

payload = {
    "username":"accuknox",
    "email":"accuknox@gmail.com",
    "password":"accuknox@123"
}


**API for login and get the token:**

      POST : http://127.0.0.1:8000/api/login/

payload = {
    "email":"accuknox@gmail.com",
    "password":"accuknox@123"
}

Response : {
    "token": "a2cddcf9676b5c0bc38e11755542db6f569ac390"
}


**API for send friend request:**

      POST: http://127.0.0.1:8000/social-network/friend-request/

payload = {
    "to_user": 2
}
Authorization : Token <first_user_token_id>

Response : {
    "id": 1,
    "timestamp": "2024-06-14T09:58:10.719929Z",
    "status": "pending",
    "from_user": 1,
    "to_user": 2
}

**API for Respond to friend request:**

      POST: http://127.0.0.1:8000/social-network/friend-request/1/

payload = {
    "status": "accepted"  // or "rejected"
}

Authorization : Token <second_user_token_id>

{
    "id": 1,
    "timestamp": "2024-06-14T09:58:10.719929Z",
    "status": "accepted",
    "from_user": 1,
    "to_user": 2
}

**API for search users:**

      GET: http://127.0.0.1:8000/social-network/search/?search=a

Authorization : Token <token_id>

Response : [
    {
        "id": 1,
        "username": "balukolapaneni371@gmail.com",
        "email": "balukolapaneni371@gmail.com"
    },
    {
        "id": 2,
        "username": "accuknox@gmail.com",
        "email": "accuknox@gmail.com"
    }
]


**API for list of friends:**

      GET: http://127.0.0.1:8000/social-network/friends/

Authorization : Token <token_id>

[
    {
        "id": 1,
        "username": "balukolapaneni371@gmail.com",
        "email": "balukolapaneni371@gmail.com"
    }
]

**API for get the pending requests:**

      GET: http://127.0.0.1:8000/social-network/pending-requests/

Authorization : Token <token_id>

