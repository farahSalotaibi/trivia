import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func
import json
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')     
   # This function will retrive all the categories from the database. 
   # First query the category table then put in an array the id and type of the category. 
   # return jsonify with the sucess status and the array list

  def categories_list():
    categories = Category.query.all()
    list_categories = { category.id: category.type for category in categories}

    return jsonify({
      "success": True,
      "categories": list_categories
        })

  @app.route('/questions')   
     # This function will retrive all the questions from the database. 
     # First we sit questions based on the number we have sit before which is 10.
     # Then put all the questions with its info to an array.
     # query the categories and put it also in an array. 
     # return jsonify with the sucess status, the question array list,
     # the categories array list and the picked category if any.

  def questions_list():
    page = request.args.get('page', 1, type=int)
    questions_page = Question.query.paginate(page, per_page=QUESTIONS_PER_PAGE)
    total_questions = questions_page.total

    questions_list = [
      question.format()
      for question in questions_page.items]

    category = Category.query.all()
    
    list_categories = { y.id: y.type for y in category}
   
    picked_category = ''
    
    return jsonify({
      "success": True,
      "questions": questions_list,
      "total_questions": total_questions,
      "categories": list_categories,
      "current_category": picked_category
        })

  @app.route('/questions/<int:id>', methods=['DELETE'])   
     # This function will delete the requested question based on the id. 
     # First we query the requested question using filter.
     # Then delete it.
     # return jsonify with the sucess status.

  def delete_question(id):
    question = Question.query.filter(Question.id == id).one_or_none()

    if question is None:
      abort(422)

    question.delete()
    return jsonify({
            "success": True
        })

  @app.route('/categories/<int:id>/questions', methods=['GET']) 
     # This function will retreve the requested category using the id. 
     # if the category is not in the database abort 404.
     # else query all the questions that match the category id.
     # return jsonify with the question list, number of the total questions and the id of the category.
  def search_by_category(id):
    category = Category.query.filter(Category.id == id).one_or_none()

    if category is None:
      abort(404)

    questions = Question.query.filter(Question.category == id).order_by(Question.id.asc()).all()

    questions_list = [
      question.format()
      for question in questions
        ]

    total = len(questions_list)
        
    return jsonify({
      "questions": questions_list,
      "total_questions": total,
      "current_category": id
        })


  @app.route('/questions', methods=["POST"]) 
    # The function here would do two things.
    # First it will take search field value and use a filter
    # to search for the same substring in the questions database (case insenstive).
    # Else if the search field is empty it will take
    # all fields in the add question page with checking all the fields.
    # Then it will add the question to the database and
    # return a jsonify with the success stateus or it will abort. 

  def questions_search():
    search = request.json.get('searchTerm', None)
    if search:
      questions = Question.query.filter(
      Question.question.ilike(f'%{search}%')).all()
      questions_list = [question.format() for question in questions]
      total = len(questions)
      current_category = ''
      return jsonify({
        "questions": questions_list,
        "total_questions": total,
        "current_category": current_category
          })
  
    else:
      added_question = request.json.get('question', None)
      added_answer = request.json.get('answer', None)
      added_category_id = request.json.get('category', None)
      added_difficulty = request.json.get('difficulty', None)
      if all([added_question, added_answer, added_category_id, added_difficulty]):
        category = Category.query.get(added_category_id)
        if category is None:
          abort(404)
        question = Question(question=added_question, answer=added_answer,
        category=category.id, difficulty=added_difficulty)
        question.insert()
        return jsonify({
          "success": True
         })
        
      else:
        abort(400)

  @app.route('/quizzes', methods=["POST"])
  #this function will take the category that the user choose
  # then the question will be chosen at random using 'random.choice' 
  # and will keep track of the previous questions to not duplicate.
  # then it will return the question or false if there are no more questions
  def quiz():
    previous_questions = request.json.get("previous_questions", [])
    quiz_category = request.json.get("quiz_category", None)

    if quiz_category and quiz_category["id"] != 0:
      category = Category.query.get(quiz_category["id"])
      if category is None:
        abort(404)
      questions = Question.query.filter(Question.category == category.id)
    else:
      questions = Question.query
    questions = questions.filter(Question.id.notin_(
        previous_questions)).all() if previous_questions else questions.all()
    if questions:
      next_question = random.choice(
      [question.format() for question in questions])
    else:
      next_question = False
    return jsonify({
      "question": next_question,
      "quiz_category": quiz_category
        })


  @app.errorhandler(400)
  def badrequest(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resourse not found"
    }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
    }), 422
    
  @app.errorhandler(422)
  def internalServerError(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "Internal Server Error"
    }), 422
    
  
  return app

    