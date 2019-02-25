import requests
from firebase import firebase # CUSTOM LIB (i lost)


class KRBase():

    def __init__(self, app_url: str, user: str, secret: str):
        self.app_url = app_url

        self.auth = firebase.FirebaseAuthentication(secret, user, extra={'id': "kolhoz"})
        self.worker = firebase.FirebaseApplication(self.app_url, self.auth)
        
    def push_new_question(self, question: str, answer: int, answers: list, probabilities: list, num: int, correct: int = 0):
        if len(answers) < 3:
            return None

        data_to_push = {
            "number": num,
            "answer" : answer,
            "answers" : {
                "first" : [answers[0], probabilities[0]],
                "second" : [answers[1], probabilities[1]],
                "third" : [answers[2], probabilities[2]]
            },
            "correct_answer": correct,
            "question" : question
        }
        result = self.worker.patch("/questions", data_to_push, name="now_question", params={'print' : 'pretty'})
        #user = self.auth.get_user()
        return result

    def push_start_data(self, prize: int, timestamp: int):
        data_to_push = {
            'prize': prize,
            'timestamp': timestamp
        }

        result = self.worker.patch("/", data_to_push, name="startdata", params={'print' : 'pretty'})
        return result

    def clear_question(self):
        result = self.worker.patch("/questions", None, name="now_question", params={'print' : 'pretty'})
        return result

    #def push_correct_answer(self, answer: int):
    #    data_to_push = {"correct_answer": answer}
    #    result = self.worker.patch("/questions/now_question", data_to_push, name="correct_answer", params={'print', 'pretty'})
    #    return result