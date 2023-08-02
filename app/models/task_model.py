
class TaskModel:

    dB = 'z_pets'

    def __init__(self, data):

        self.id = data['id']
        self.description = data['description']

    def __str__(self):
        return f"{self.description}"