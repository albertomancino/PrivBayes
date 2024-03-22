import pandas as pd
import os

# input dataset
data_path = 'original/tests/data/adult_tiny.csv'
assert os.path.exists(data_path)

data = pd.read_csv(data_path)

from src.original_priv_bayes import greedy_bayes_no_mp
# n = greedy_bayes_no_mp(data, k=1, epsilon=1)
# n2 = greedy_bayes_no_mp(data, k=2, epsilon=1)


from rec_data.datasets import FacebookBooks

data = FacebookBooks()
print()

from src.priv_bayes import PrivBayes

privatizer = PrivBayes(degree=3)
privatizer.greedy_bayes(data=data)



print()
n3 = greedy_bayes_no_mp(data, k=3, epsilon=1)
print()
