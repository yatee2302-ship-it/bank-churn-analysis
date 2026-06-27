import pandas as pd
import numpy as np

np.random.seed(42)

n = 100

df = pd.DataFrame({
    "CreditScore": np.random.randint(350, 850, n),
    "Age": np.random.randint(18, 80, n),
    "Tenure": np.random.randint(0, 11, n),
    "Balance": np.random.randint(0, 200000, n),
    "NumOfProducts": np.random.randint(1, 5, n),
    "HasCrCard": np.random.randint(0, 2, n),
    "IsActiveMember": np.random.randint(0, 2, n),
    "EstimatedSalary": np.random.randint(10000, 200000, n)
})

df.to_csv("test_customers.csv", index=False)

print("CSV Created Successfully")