# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

GET '/questions'
- Fetches a all the questions in which the keys are the ids and the value is the corresponding string of the question, its answer, the diffculty and the category.
- Request Arguments: None
- Returns: All the questions, it's categories, total number of questions and the picked category if any.
- Example
Requested Path http://localhost:5000/questions
{{
      "success": True,
      "questions": [{
          "id": 5, 
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
          "answer": "Maya Angelou",
          "difficulty": 2,
          "category": 4
      },
      {
          "id": 9, 
          "question": "What boxer's original name is Cassius Clay?",
          "answer": "Muhammad Ali",
          "difficulty": 1,
          "category": 4   
      },
      {
          "id": 2, 
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
          "answer": "Apollo 13",
          "difficulty": 4,
          "category": 5   
      },
      ],
      "total_questions": 3,
      "categories": {
        "1": "science",
        "2": "art",
        "3": "geography",
        "4": "history",
        "5": "entertainment",
        "6": "sports"
    },
      "current_category": null
        }

}
GET '/categories/<int:id>/questions'
- Fetches all the questions of a specific category based on the category id.
- Request Arguments: The id of the category.
- Returns: all the question of the asked category.
- Example Requested Path http://localhost:5000/categories/1/questions
{
    "questions": [
        {
            "id": 20,
            "question": "What is the heaviest organ in the human body?",  
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4

        },
        {
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?",
            "answer": "Blood",
            "category": 1,
            "difficulty": 4

        }
    ],
    "total_questions": 2,
    "current_category": 1

}
DELETE '/questions/<int:id>'
- Fetches the questions that with the matched Id and delete it
- Request Arguments: The id of the question to be deleted
- Returns: None
- Example
Requested Path http://localhost:5000/questions/2
{
    "success": true
}

POST '/questions'
- Fetches the questions need to be added, check the filled fields
- Fetches the search string check if it match any substring of the question stored in the database. 
- Request Arguments: None
- Returns: For searching (It returns all the question that match the search string)
-Example 
Requested Path http://localhost:5000/questions
1) For adding question:
{
    "question": "What is mu name",
    "answer": "farah",
    "category": 3,
    "difficulty": 1
}
The respond is:
{
    "success": true
}

2) For searching term
{
    "searchTerm": "palace"
}
The respond is:
{
    "questions": [
        {   "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?",
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3
        }
    ],
    "total_questions": 1,
    "current_category": null
}
POST '/quizzes'
- Fetches the questions based on the category ID that the user chooses.
- The question will be chosen at random and will keep track of the previous question to not duplicate.
- Request Arguments: None
- Returns: Questions of a specific category that does not duplicate.
-Example 
Requested Path http://localhost:5000/quizzes
The request
{
    "quiz_category": {
        "id": 2
    },
    "previous_questions": []
}
The respond
{
    "question": {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
 ```
