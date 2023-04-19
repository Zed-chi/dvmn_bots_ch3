import argparse
import json
from google.api_core.exceptions import InvalidArgument
from dialogflow import create_intent
from environs import Env
import logging

ENV = Env()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_args():
    parser = argparse.ArgumentParser(description="DialogFlow ")
    parser.add_argument(
        "-p",
        dest="path",
        default="./questions.json",
        type=str,
        help="Path to json file with questions",
    )
    return parser.parse_args()


def load_questions(filepath):
    with open("./questions.json", "r", encoding="utf-8") as file:
        questions: dict = json.load(file)
        return questions


def teach(questions):
    for intent in questions.keys():
        try:
            phrases = questions[intent]["questions"]
            answer = questions[intent]["answer"]
            create_intent(ENV.str("GOOGLE_CLOUD_PROJECT"), intent, phrases, [answer])
        except InvalidArgument as e:
            logging.info(f"Раздел {intent} уже существует")


def main():
    ENV.read_env()
    questions_path = ENV.str("QUESTIONS_JSON", None)
    if not questions_path:
        questions_path = get_args().path

    questions = load_questions(questions_path)
    teach(questions)


if __name__ == "__main__":
    main()
