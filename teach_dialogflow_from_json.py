import json
import argparse
from dialog import create_intent
from environs import Env

ENV = Env()
ENV.read_env()

def get_args():
    parser = argparse.ArgumentParser(description="DialogFlow ")    
    parser.add_argument(
        "-p", dest="path", default="./questions.json", 
        type=str, description="Path to json file with questions"
    )
    args = parser.parse_args()

def load_questions(filepath):
    with open("./questions.json", "r", encoding="utf-8") as file:
        questions: dict = json.load(file)
        return questions


def teach(questions):
    for intent in questions.keys():
        phrases = questions[intent]["questions"]
        answer = questions[intent]["answer"]
        create_intent(ENV.str("PROJECT_ID"), intent, phrases, [answer])


def main():
    args = get_args()
    questions = load_questions(args.path)
    teach(questions)


if __name__ == "__main__":
    main()