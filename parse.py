from lxml import etree
import pandas as pd
import pathlib

parser = etree.HTMLParser()

xml = etree.parse(open('prez_issues.html'), parser)

candidates = ['biden', 'trump', 'jorgensen', 'hawkins']

questions = []

answer_map = {
    '?': 0,
    'Pro': 1,
    'Con': -1,
    'NC': 0,
    'Now Pro': 1,
    'Now Con': 1,
    'Now NC': 1,
}

items = xml.xpath('//tbody/tr')

for item in items:
    question = {}
    question['text'] = item.xpath('.//div[contains(@class,"question-question")]/a/text()')[0]
    question['category'] = item.xpath('.//div[contains(@class,"question-issue")]/text()')[0]
    answers = item.xpath('.//td[contains(@class,"question-response")]/descendant::*[last()]/text()')
    assert len(answers) == len(candidates), "Invalid length of responses"
    for candidate, answer in zip(candidates, answers):
        question[candidate] = answer_map[answer]

    questions.append(question)

questions = pd.DataFrame(questions)

# drop random broken question
drop_indices = questions[questions.text == 'Timeline of Comments'].index
questions.drop(drop_indices, inplace=True)
questions.reset_index(drop=True, inplace=True)

questions.to_pickle('questions.pkl')
