from app.config.mysqlconnection import connectToMySQL
from app.models.task_model import TaskModel

class Todo:

    dB = 'z_todo'

    def __init__(self, data):

        self.id = data['id']
        self.text = data['text']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.tasks = []
    
    @classmethod
    def get_all(cls):

        query = """
            SELECT
                *
            FROM
                todos
        """

        results = connectToMySQL(cls.dB).query_db(query)

        rows = []

        for result in results: ## each result is a dictionary
            rows.append(cls(result)) # instantiate a Todo object from that data

        return rows
    
    @classmethod
    def update(cls, data):

        query = """
            UPDATE

                todos
                
            SET
                text=%(text)s,
                description=%(description)s
                
            WHERE
                id=%(id)s
            ;
    
        """

        return connectToMySQL(cls.dB).query_db(query, data)
    
    @classmethod
    def get_by_id(cls, id):
        
        query = """
                SELECT 
                * 
            FROM 
                todos
                
			LEFT JOIN tasks ON tasks.todo_id = todos.id

            WHERE 
                todos.id=%(id)s
                ;
        """
        # first save query to a variable and look at it with the debugger
        results = connectToMySQL(cls.dB).query_db(query, { 'id': id })

        if results:
            todo = cls(results[0])

            for result in results:

                task = TaskModel({
                        "id": result['tasks.id'],
                        "description": result['tasks.description']
                    })

                print(task)
                todo.tasks.append(task)

            return todo

        return None
    
    @classmethod
    def create(cls, data):

        query ="""
            INSERT INTO

                todos

            (text, description)

            VALUES
            (%(text)s, %(description)s)
        """

        return connectToMySQL(cls.dB).query_db(query, data)