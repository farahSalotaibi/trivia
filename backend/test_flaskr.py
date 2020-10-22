import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('postgres:1234@localhost:5432', self.database_name)


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    


    def get_categories_test(self):
        res = self.client().get('/categories')
        self.assertEqual(res.status_code, 200)
   
    def get_questions_get(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)

    def get_questions_correct_page_test(self):
        res = self.client().get('/questions?page=2')
        self.assertEqual(res.status_code, 200)

    def delete_question_test(self):
        res = self.client().delete('/questions/2')
        self.assertEqual(res.status_code, 200)
        id=Question.query.filter(Question.id==2).count()
        self.assertEqual(id, 0)

    def get_questions_by_category_test(self):
        res = self.client().get('categories/2/questions')
        self.assertEqual(res.status_code, 200)   

    def get_questions_with_search_term(self):
        res = self.client().post('/questions', json={"searchTerm":"world"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.json['questions']), 2)

    def insert_question_test(self):
        res = self.client().post('/questions', json={"question": "what is love?", "answer": "food", "difficulty": "3", "category": "1"})
        self.assertEqual(res.status_code, 200)
        question=Question.query.filter(Question.question=="what is love?").one_or_none()
        self.assertIsNotNone(question)

    def test_play_quiz_getting_question(self):
        res = self.client().post('/quizzes', json={})
        self.assertEqual(res.status_code, 200)

    def play_quiz_question_correct_category_test(self):
        res = self.client().post('/quizzes', json={"quiz_category":{'type': 'History', 'id': '4'}})
        question = res.json.get('question')
        self.assertEqual(question['category'], 4)



    def get_questions_wrong_page_test(self):
        res = self.client().get('/questions?page=20')
        self.assertEqual(res.status_code, 404)

    def delete_question_by_unavailable_id_test(self):
        res = self.client().delete('/questions/100')
        self.assertEqual(res.status_code, 404)


    def get_questions_by_wrong_category_test(self):
        res = self.client().get('categories/203/questions')
        self.assertEqual(res.status_code, 404)

    def get_questions_by_bad_request_search_term_test(self):
        res = self.client().post('/questions', json={})
        self.assertEqual(res.status_code, 400)

    def test_insert_invalid_question(self):
        res = self.client().post('/questions', json={"question": "what is love?"})
        self.assertEqual(res.status_code, 400)        

    def test_play_quiz_getting_question_in_invalid_category(self):
        res = self.client().post('/quizzes', json={"quiz_category":{'type': 'nove', 'id': '100'}})
        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()