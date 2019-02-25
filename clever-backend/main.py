# Data looks this
#{
#  "answer" : 1,
#  "answers" : {
#    "first" : "Ля",
#    "second" : "Ляяяяяяяяяяя",
#    "third" : "Ляяяяя"
#  },
#  "correct_answer" : 2,
#  "question" : "Как звали петуха?"
#}
from clever import *
from firebase_worker import KRBase
from longpoll import LongPoll

import logging
import config

logging.basicConfig(format='%(levelname)-8s [%(asctime)s]  %(message)s',
                    filemode='at',
                    filename='krclever_log.log',
                    level=logging.INFO)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)-8s [%(asctime)s]  %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

base = KRBase(
    config.firebase_url_project,
    config.firebase_email,
    config.firebase_secret
)
clever = LongPoll(config.clever_token)

def display_answer(qid, answer):
    logging.info("-------------------\n")
    logging.info(f"Вопрос номер {qid}:")
    logging.info(f"Ответ: {answer}")
    return

if __name__ == "__main__":
    logging.info("К приему вопросов, готов!")
    while True:
        c_q = clever.check_question()          	
        if c_q:
            logging.info("start search new question")
            google = KleverGoogler(c_q.question, c_q.answers, 0, c_q.num)
            try:
                google.search()
            except ConnectionResetError as e:
                logging.info(e)
            question = google.genQuestion()
    
            probabilities = (
                question.answers[0].probability,
                question.answers[1].probability,
                question.answers[2].probability
            )

            base.push_new_question(question.question, int(question.best[0]), c_q.answers, probabilities, c_q.num)
            display_answer(question.id, question.best[0])

            while True:
                logging.info("check correct answer")
                answrsp = clever.get_stream_info()
                try:
                    answrsp = answrsp["response"]["question"]
                except KeyError:
                    logging.error(f"Exception occurred:\n{answrsp}")
                    break
            
                try:
                    correct = answrsp["right_answer_id"]
                    base.push_new_question(question.question, int(question.best[0]), c_q.answers, probabilities, c_q.num, correct+1)
                    logging.info("sucs push correct answer")
                    break
                except KeyError:
                    time.sleep(2)
        else:
            s_d = clever.check_start_data()
            if s_d:
                try:
                    start_time = s_d["response"]["game_info"]["game"]["start_time"]
                    prize = s_d["response"]["game_info"]["game"]["prize"]                    
                    base.push_start_data(prize, start_time)
                except KeyError:
                    pass

                base.clear_question()



