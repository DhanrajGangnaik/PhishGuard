"""
Optional training placeholder for academic completeness.
This project currently uses a lightweight explainable hybrid engine.
You can extend this file later to train a text classifier on phishing datasets.
"""

import pandas as pd


if __name__ == '__main__':
    print('PhishGuard uses a hybrid rule-based engine by default.')
    print('Add dataset loading and model training here if you want an ML extension.')
    sample = pd.DataFrame({
        'text': ['verify your account now', 'meeting at 5 pm', 'reset your password immediately'],
        'label': [1, 0, 1],
    })
    print(sample)
