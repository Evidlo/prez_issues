import pandas as pd
import matplotlib.pyplot as plt

questions_file = 'questions.pkl'
answers_file = 'answers.pkl'

candidates = ['biden', 'trump', 'jorgensen', 'hawkins']

questions = pd.read_pickle(questions_file)
answers = pd.read_pickle(answers_file)

scores = questions.copy()
scores[candidates] = scores[candidates].mul(answers.answer, axis=0)

category_scores = {}
for category in scores.category.unique():
    category_scores[category] = scores[scores.category == category][candidates].sum()

plt.close()
figs, axes = plt.subplots(2, 1, figsize=(8, 6))

axes[0].set_title('Candidate Similarity')
scores[candidates].sum().plot.bar(ax=axes[0])
axes[0].spines["bottom"].set_position(("data", 0))
axes[0].set_ylabel('Score')

axes[1].set_title('Candidate Similarity by Category')
pd.DataFrame(category_scores).plot.bar(ax=axes[1])
axes[1].spines["bottom"].set_position(("data", 0))
plt.legend(bbox_to_anchor=(1.04,0.5), loc="center left", borderaxespad=0)
plt.ylabel('Score')
axes[1].set_ylabel('Score')

plt.tight_layout()
plt.show()
