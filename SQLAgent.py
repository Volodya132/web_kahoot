import sqlite3


class SQLAgent:
    def __init__(self, name_db):
        self.db = sqlite3.connect(name_db)
        self.create_tables()

    def create_tables(self):
        cursor = self.db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Quizz (
            quizz_id INTEGER PRIMARY KEY,
            quizz_name TEXT NOT NULL,
            description TEXT
            )
        ''')
        cursor.execute('''
                      CREATE TABLE IF NOT EXISTS Questions (
                           question_id INTEGER PRIMARY KEY,
                           quiz_id INTEGER,
                           content TEXT,
                           FOREIGN KEY (quiz_id) REFERENCES Quizz(quiz_id)
                      );
                      ''')
        cursor.execute('''
                      CREATE TABLE IF NOT EXISTS Answers (
                           answer_id INTEGER PRIMARY KEY,
                           question_id INTEGER,
                           content TEXT,
                           is_right BOOLEAN,
                           FOREIGN KEY (question_id) REFERENCES Questions(question_id)
                      );
                      ''')
        cursor.close()
        self.db.commit()

    def add_quizz(self, name, description):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO Quizz(quizz_name, description) VALUES(?, ?)',
                       [name, description])
        cursor.close()
        self.db.commit()

    def add_question(self, quiz_id, content):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO Questions(quiz_id, content) VALUES(?, ?)',
                       [quiz_id, content])
        cursor.close()
        self.db.commit()

    def add_answer(self, question_id, content, is_right):
        cursor = self.db.cursor()
        cursor.execute('INSERT INTO Answers(question_id, content, is_right) VALUES(?, ?, ?)',
                       [question_id, content, is_right])
        cursor.close()
        self.db.commit()

    def get_quizzes(self):
        cursor = self.db.cursor()
        query = "SELECT * FROM Quizz "
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_questions(self, quiz_id):
        cursor = self.db.cursor()
        query = "SELECT * FROM Questions WHERE quiz_id = ?"
        cursor.execute(query, [quiz_id])
        result = cursor.fetchall()
        cursor.close()
        return result

    def get_options_for_question(self, question_id):
        cursor = self.db.cursor()
        query = 'SELECT * FROM Answers WHERE question_id = ?'
        cursor.execute(query, (question_id,))
        qoptions = cursor.fetchall()
        cursor.close()
        return qoptions

