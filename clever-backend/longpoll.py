import requests
import time

# NOT WORK
# DON'T USE THAT

class CleverQuestion():

    __slots__ = ('question', 'answers', 'num')

    def __init__(self, question, answers: list, num: int):
        self.question = question
        self.answers = answers
        self.num = num

class LongPoll():

    def __init__(self, token):
        if not token or token is "":
            print("Token is empty. Exiting...")
            exit()
        self.token = token
        self.base_uri = "https://api.vk.com/method/execute."
        self.start_data = "getStartData"
        self.get_question = "getLastQuestion"

        self.wait = 10
        self.values = {
            'access_token': token,
            'v': '5.73'
        }
        self.status_value = {
            "access_token": token,
            "v": "5.73",
            "lang": "ru",
            "https": 1
        }
    
    def check_question(self):
        response = requests.get(
            self.base_uri+self.get_question,
            params=self.values,
            timeout=self.wait
        ).json()
        time.sleep(1)

        if not response['response']:
            return None
        else:
            q = response['response']['text']
            a1 = response['response']['answers'][0]['text']
            a2 = response['response']['answers'][1]['text']
            a3 = response['response']['answers'][2]['text']
            num = response['response']['number']

            clever = CleverQuestion(q, (a1, a2, a3), num)

        return clever
      
    def get_stream_info(self):
        response = requests.post("https://api.vk.com/method/streamQuiz.getCurrentStatus",
                                 data=self.status_value,
                                 timeout=self.wait
        ).json()

        return response
        
    def check_start_data(self):
        response = requests.get(
            self.base_uri+self.start_data,
            params=self.values
        ).json()
        return response    
        