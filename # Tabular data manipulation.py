# Tabular data manipulation
import pandas as pd

# Numerical array handling
import numpy as np

# Statistical machine learning preprocessing
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder, MinMaxScaler 

# Publication-quality visualization
import matplotlib.pyplot as plt
import seaborn as sns


# 1. LOADING THE DATASET
df = pd.read_csv("heartdata.csv")
print("1. Raw Loaded DataFrame")
print(df)
print("\nData Types:")
print(df.dtypes)

# 2. DISPLAYING MISSING VALUES
print(df.isnull().sum())

# 3. REMOVING DUPLICATES
df = df.drop_duplicates()
print("\n2. After Removing Duplicates")
print(df)

# 4. CORRECTING INCOSISTANT DATA
df['Gender'] = df['Gender'].replace({'M': 'Male'}).replace({'F': 'Female'})
print("\n3. After Fixing Inconsistencies ")
print(df[['Name', 'Gender']])

df.loc[df['Age'] > 100, 'Age'] = 70
print("\n5. After Handling Extreme Outliers")
print(df)

df['Cholesterol_mgDL'] = df['Cholesterol_mgDL'].fillna(df['Cholesterol_mgDL'].median())
df['Systolic_BP'] = df['Systolic_BP'].fillna(df['Systolic_BP'].median())
df['Risk_Tier'] = df['Risk_Tier'].fillna("Low")
print("\n4. After Handling Missing Values")
print(df)

tier_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
df['Risk_Tier_Encoded'] = df['Risk_Tier'].map(tier_mapping)

df = pd.get_dummies(df, columns=['Gender', 'Smoker_Status'], dtype=int)
print("\n--- 6. After Categorical Encoding ---")
print(df.info())

scaler_minmax = MinMaxScaler()
df['Cholesterol_mgDL'] = scaler_minmax.fit_transform(df[['Cholesterol_mgDL']])
scaler_minmax1 = MinMaxScaler()
df['Systolic_BP'] = scaler_minmax1.fit_transform(df[['Systolic_BP']])
df_final = df.drop(columns=['Name', 'Risk_Tier'])

print(df_final.head(10))


# A. Scatter Plot - Cholesterol_mgDL vs Systolic_BP
plt.figure(figsize=(8, 6))
# Create scatter plot
plt.scatter(df['Cholesterol_mgDL'], df['Systolic_BP'], color='blue')
plt.title('Scatter Plot → Cholesterol_mgDL vs Systolic_BP')
plt.xlabel('Cholesterol_mgDL')
plt.ylabel('Systolic_BP')
plt.show()


plt.figure(figsize=(8, 6))

# Set labels and titles for a publication-quality layout
plt.title('Distribution of Normalized Systolic BP by Age Bracket')
plt.xlabel('Age')
plt.ylabel('Systolic_BP' )
plt.show()