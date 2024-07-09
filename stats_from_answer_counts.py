#!/usr/bin/env python3

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'answer_counts', default=sys.stdin, nargs='?', type=argparse.FileType('r'),
        help="JSON file containing answer counts.")
    args = parser.parse_args()

    answer_counts = json.load(args.answer_counts)
    args.answer_counts.close()

    lecture_question_options = {}
    for key, count in answer_counts.items():
        lecture, question, option = key.split('-')
        if lecture not in lecture_question_options:
            lecture_question_options[lecture] = {}
        if question not in lecture_question_options[lecture]:
            lecture_question_options[lecture][question] = {}
        lecture_question_options[lecture][question][option] = count

    for lecture, questions in lecture_question_options.items():
        total_wrong_answers = 0
        total_correct_answers = 0
        for question, options in questions.items():
            total_correct_answers += max(options.values())
            total_wrong_answers += (
                sum(options.values()) - max(options.values()))
        print(f"{lecture}\t{total_wrong_answers/total_correct_answers}")

if __name__ == "__main__":
    main()
