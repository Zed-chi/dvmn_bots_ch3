import argparse
import json
import logging

from environs import Env
from google.api_core.exceptions import InvalidArgument

from dialogflow import create_intent

ENV = Env()


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
    with open(filepath, "r", encoding="utf-8") as file:
        questions: dict = json.load(file)
        return questions


def teach(questions, project_id):
    for intent_name, intent_data in questions.items():
        try:
            phrases = intent_data["questions"]
            answer = intent_data["answer"]
            create_intent(project_id, intent_name, phrases, [answer])
        except InvalidArgument:
            logging.info(f"Раздел {intent_name} уже существует")


def main():
    ENV.read_env()
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    questions_path = ENV.str("QUESTIONS_JSON", None)
    project_id = ENV.str("GOOGLE_CLOUD_PROJECT")

    if not questions_path:
        questions_path = get_args().path

    questions = load_questions(questions_path)
    teach(questions, project_id)


if __name__ == "__main__":
    main()
