import os
import pandas as pd

questions_file = 'questions.pkl'
answers_file = 'answers.pkl'

assert os.path.exists(questions_file), "No questions found, run parse.py first"
questions = pd.read_pickle(questions_file)

if os.path.exists(answers_file):
    answers = pd.read_pickle(answers_file)
else:
    answers = pd.DataFrame()

answer_map = {
    'y': 1,
    'yes': 1,
    'x': 0,
    'n': -1,
    'no': -1
}

print("Please answer these questions.  Reserve importance=2 for issues you care strongly about.")
for n, (_, question) in enumerate(questions.iloc[len(answers):].iterrows(), len(answers) + 1):
    print('\n----- Question {}/{} ----- Category: {}'.format(n, len(questions), question.category))
    print(question.text)
    while True:
        try:
            print('Answer y (yes), n (no), x (no response): ')
            answer = answer_map[input('y/n/x: ')]
        except KeyError:
            print("Invalid response")
        else:
            break
    while True:
        try:
            print('Importance 0 (dont care), 1 (care a little), 2 (care a lot): ')
            importance = int(input('Importance [0-2]: '))
        except ValueError:
            print("Invalid response")
        else:
            break

    answers = answers.append({'answer': answer, 'importance': importance}, ignore_index=True)

    answers.to_pickle(answers_file)
