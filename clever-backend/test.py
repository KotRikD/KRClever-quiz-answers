from clever import *
from firebase_worker import KRBase
from longpoll import LongPoll
import time
import config

base = KRBase(
    config.firebase_url_project,
    config.firebase_email,
    config.firebase_secret
)
clever = LongPoll(config.clever_token)

if __name__ == "__main__":
    num = 1
    quest = "Кого больше всего боятся слоны?"
    answers = ("Мышей", "Пчёл", "Мух")
    google = KleverGoogler(quest, answers, 0, num)
    try:
        google.search()
    except ConnectionResetError as e:
        print(e)

    question = google.genQuestion()
    probabilities = (
        question.answers[0].probability,
        question.answers[1].probability,
        question.answers[2].probability
    )

    base.push_new_question(quest, int(question.best[0]), answers, probabilities, num)
    time.sleep(5)
    base.push_new_question(quest, int(question.best[0]), answers, probabilities, num, 2)