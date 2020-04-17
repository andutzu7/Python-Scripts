import matplotlib.pyplot as plt
from pandasql import *
import pandas as pd

pysqldf = lambda q: sqldf(q, globals())


database = pd.read_csv("Iteratia2.csv")

q  = """
SELECT AVG(AverageTemperature) FROM database WHERE dt>1990 AND Country='Romania' 
"""

df = pysqldf(q)
print(df)