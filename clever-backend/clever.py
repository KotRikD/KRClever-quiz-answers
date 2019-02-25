import time
import random
import re
from datetime import datetime, timezone
import json
import requests
import time, asyncio
import urllib.request, urllib.parse
import webbrowser

class KleverAnswer:
    def __init__(self, text, coincidences):
        self.text = text
        self.coincidences = coincidences
        self.probability = 0
 
    def __str__(self):
        return self.text + " | " + str(self.probability) + "%"
 
    def setProbability(self, new):
        self.probability = new
 
 
class KleverQuestion:
    def __init__(self, question, answers: list, sent_time: int, kid: int, optimized: str):
        self.question = question
        self.answers = answers
        self.sent_time = sent_time
        self.id = kid
        self.reverse = " не " in question.lower() or " ни " in question.lower()
        self.optimized = optimized
 
    def __str__(self):
        return self.question + ":" + self.answers[0].text + "#" + self.answers[1].text + "#" + self.answers[2].text
 
    def calculate_probability(self):
        total = 0
        for answer in self.answers:
            total += answer.coincidences  # first of all count total, then anything else
        for answer in self.answers:
            if total == 0:
                answer.setProbability(0)
            else:
                answer.setProbability(round(answer.coincidences / total * 100, 1))
        if total == 0:
            self.question += " | NOT FOUND!"
            self.best = "0. ???"
        else:
            a = min(self.answers[a].coincidences for a in range(3)) if self.reverse else \
                max(self.answers[a].coincidences for a in range(3))
            i = 0
            for answer in self.answers:
                i += 1
                if answer.coincidences == a:
                    self.best = str(i) + ". " + answer.text
 
 
class KleverGoogler:
    FILTERED_WORDS = ("сколько", "как много", "вошли в историю как", "какие", "как называется", "чем является",
                      "что из этого", "(у |)как(ой|ого|их) из( этих|)", "какой из героев", "традиционно", "согласно",
                      " - ",
                      "чем занимается", "чья профессия", "состоялся", "из фильма", "что из этого",
                      "какой", "является", "в мире", "и к", "термин(ов|ы|)", "относ(и|я)тся", "в какой",
                      "у как(ого|ой|их)", "согласно", "на каком", "состоялся", "по численности", " не ", " ни ")
    OPTIMIZE_DICT = {
        "в каком году": "когда",
        "какого животного": "кого",  ###############################
        "один": "1",  ###############################
        "одна": "1",  ###############################
        "одно": "1",  ####        #######        ####
        "два": "2",  ####        #######        ####
        "двое": "2",  ####        #######        ####
        "две": "2",  ####        #######        ####
        "три": "3",  ###############################
        "трое": "3",  ##############   ##############
        "четыре": "4",  ##############   ##############
        "четверо": "4",  ##############   ##############
        "пять": "5",  ###############################
        "пятеро": "5",  ########               ########
        "шесть": "6",  ########               ########
        "шестеро": "6",  ####    ###############   #####
        "семь": "7",  ####    ###############   #####
        "семеро": "7",  ###############################
        "восемь": "8",  ###############################
        "девять": "9",  #####                     #####
        "десять": "10",  #####                     #####
        "одиннадцать": "11",  #############     #############
        "двенадцать": "12",  #############     #############
        "тринадцать": "13",  #############     #############
        "четырнадцать": "14",  #############     #############
        "пятнадцать": "15",  #############     #############
        "шестнадцать": "16",  #############     #############
        "семнадцать": "17",  #############     #############
        "восемнадцать": "18",  #############     #############
        "девятнадцать": "19",  ###############################
        "двадцать": "20",  ###############################
        "тридцать": "30",  ###############################
        "сорок": "40",  ####         #####         ####
        "пятьдесят": "50",  ####  ############  ###########
        "шестьдесят": "60",  ####  ############  ###########
        "семьдесят": "70",  ####  #####  #####  #####  ####
        "восемьдесят": "80",  ####  ###### #####  ###### ####
        "девяносто": "90",  ####  ###### #####  ###### ####
        "сто": "100",  ####         #####         ####
        "двести": "200",  ###############################
        "триста": "300",  ###############################
        "четыреста": "400",  ###############################
        "пятьсот": "500",  ###############################
        "шестьсот": "600",  ###############################
        "семьсот": "700",  ###############################
        "восемьсот": "800",  ######                   ######
        "девятсот": "900",  ######  if you use this  ######
        "тысача": "1000",  ######    please leave   ######
        " тысячи": "000",  ######  copyright notice ######
        " тысяч": "000",  ######                   ######
        "миллион": "1000000",  ######   (c) TaizoGem    ######
        " миллиона": "000000",  ###############################
        " миллионов": "000000"  ###############################
    }
 
    def __init__(self, question: str, answers, sent_time: int, num: int):
        self._question = question
        self.__question = self.optimizeString(question)
        self.answers = []
        self.__answers = [self.optimizeString(a) for a in answers]
        self.newquestion = self.__question + '("' + '" | "'.join(answers) + '")'
        self.conn = requests.Session()
        self.sent_time = sent_time
        self.number = num
        self.ran_reverse = False
 
    def fetch(self, query, newquery=""):
        try:
            google = self.conn.get("https://www.google.ru/search?q=" + urllib.parse.quote_plus(query)).text.lower()
            yandex = self.conn.get("https://www.yandex.ru/search/?text=" + urllib.parse.quote_plus(query)).text.lower()
            newyandex = self.conn.get("https://www.yandex.ru/search/?text=" + urllib.parse.quote_plus(
                newquery)).text.lower() if newquery else ""
            ddg = self.conn.get("https://duckduckgo.com/?q=" + urllib.parse.quote_plus(query) + "&format=json").json()
            out = ""
            try:
                smth = self.conn.get(ddg["AbstractURL"]).text.lower()
                out += smth
            except:
                pass
            out += ddg["Abstract"]
            if not "Our systems have detected unusual traffic from your computer network" in google \
                    and not "support.google.com/websearch/answer/86640" in google:
                out += google
            if not "{\"captchaSound\"" in yandex:
                out += yandex
            if not "{\"captchaSound\"" in newyandex:
                out += newyandex
            return out
        except Exception as e:
            return ""
 
    def search(self):
        response = self.fetch(self.__question, self.newquestion)
        if all(" и " in s for s in self.__answers):  # если И есть в каждом ответе...
            print("Found multipart question", end="\r")
            for answer in self.__answers:
                current_count = 0
                for part in answer.split(" и "):
                    current_count += len(
                        re.findall("(:|-|!|.|,|\?|;|\"|'|`| )" + part.lower() + "(:|-|!|.|,|\?|;|\"|'|`| )", response))
                self.answers.append(KleverAnswer(answer, current_count))
        else:
            for answer in self.__answers:
                current_count = 0
                for part in answer.split(" "):
                    current_count += len(
                        re.findall("(:|-|!|.|,|\?|;|\"|'|`| )" + part.lower() + "(:|-|!|.|,|\?|;|\"|'|`| )", response))
                self.answers.append(KleverAnswer(answer, current_count))
        a = [b.coincidences for b in self.answers]
        if a[1:] == a[:-1]:
            self.doReverse(a)
        del a
 
    def doReverse(self, prev_results=[0 for a in range(25)]):
        self.answers = []
        i = 0
        for answer in self.__answers:
            rsp = self.fetch(self.optimizeString(answer))
            sumd = 0
            for word in self.getLemmas(self.__question):
                sumd += len(re.findall("(:|-|!|.|,|\?|;|\"|'|`| )" + word.lower() + "(:|-|!|.|,|\?|;|\"|'|`| )", rsp))
            self.answers.append(KleverAnswer(answer, prev_results[i] + sumd))
            i += 1
        self.ran_reverse = True
 
    def genQuestion(self):
        a = KleverQuestion(self._question, self.answers, self.sent_time, self.number, self.__question)
        a.calculate_probability()
        return a
 
    def optimizeString(self, base):
        base = base.lower()
        base = re.sub("[\'@<!«»?,.]", "", base)
        base = re.sub("(" + "|".join(self.FILTERED_WORDS) + ")( |)", "", base)
        pattern = re.compile(r'\b(' + '|'.join(self.OPTIMIZE_DICT.keys()) + r')\b')
        base = pattern.sub(lambda x: self.OPTIMIZE_DICT[x.group()], base)
        return base
 
    def getLemmas(self, base):
        out = []
        for a in requests.get(
                "http://www.solarix.ru/php/lemma-provider.php?query=" + urllib.parse.quote_plus(base)).text.split(" "):
            a = a.replace("\r\n", "")
            if a:
                out.append(a)
        return out