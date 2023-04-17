import json

from environs import Env

from dialog import create_intent

env = Env()
env.read_env()

with open("./questions.json", "r", encoding="utf-8") as file:
    questions: dict = json.load(file)


for intent in questions.keys():
    phrases = questions[intent]["questions"]
    answer = questions[intent]["answer"]
    create_intent(env.str("PROJECT_ID"), intent, phrases, [answer])
