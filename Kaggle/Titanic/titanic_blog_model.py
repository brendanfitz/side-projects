#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
sns.set_style('whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


def age_category(x):
    categories = ['young_child', 'child', 'adult', 'senior', 'Unknown', 'ERROR']
    x_mapped = np.where(x.isna(), 'Unknown', 
                        np.where(x < 12, 'young_child', 
                                 np.where(x < 18, 'child', 
                                          np.where(x < 50, 'adult',
                                                   np.where(x >= 50, 'senior', 'ERROR')
                                                  )
                                         )
                                )
                       )
    return pd.Categorical(x_mapped, ordered=True, categories=categories)


# In[3]:


df = (pd.read_csv(r'data/train.csv')
      .set_index('PassengerId')
      .rename(columns=str.lower)
      .assign(
          age_category=lambda x: age_category(x.age),
          family_size=lambda x: x.sibsp + x.parch,
          is_alone=lambda x: (x.family_size == 0).astype('int'),
          fare_bins =lambda x: pd.qcut(x.fare, 4),
      )
     )


# In[4]:


""" Check for duplicates """
assert(not df.duplicated(keep=False).any())


# ## Overall Survival Rate

# In[5]:


print('{:.2%}'.format(df.survived.mean()))


# ## Survival Rate

# In[6]:


def survival_rate(input_df, dims, include_totals=False, format_rate=True):
    df = input_df.copy()
    df = (df.groupby(dims)
          .agg(
              total_passengers=pd.NamedAgg(column='survived', aggfunc='count'),
              number_survived=pd.NamedAgg(column='survived', aggfunc='sum'),
          )
          .assign(
              number_died=lambda x: x.total_passengers-x.number_survived,
              survival_rate=lambda x: x.number_survived.div(x.total_passengers)
          )
         )
    if format_rate:
        df = df.assign(survival_rate=lambda x: x.survival_rate.map("{:.1%}".format))
    
    if include_totals:
        return df
    return df.drop(['total_passengers', 'number_survived', 'number_died'], axis=1)


# In[7]:


df.pipe(survival_rate, 'pclass', False)


# In[8]:


df.pipe(survival_rate, ['sex', 'pclass'], True).unstack('sex')


# Clearly your class affects who survives

# In[9]:


df.pipe(survival_rate, ['sex', 'age_category'], True).unstack('sex')


# ## Age

# In[10]:


sns.distplot(df.age.dropna())
sns.despine(left=True)


# ## Title

# In[11]:


""" Add title """
pat = r'[\w\s\'-]+, ([\w\s]+)\. [\w\(\)\"\s\'-]+'
assert(df.name.str.match(pat).all() == True)
df = df.assign(title=lambda x: x.name.str.extract(pat))


# In[12]:


df.title.unique()


# In[13]:


pd.concat([
    df.groupby('title').survived.mean().sort_values(ascending=False),
    df.title.value_counts()
], axis=1)


# In[14]:


"""
We are using a data structure of dictionaries with keys --> lists for title_groups --> titles
and flipping it as it is easier to keep track
I know this creates extra work but the organization is worth it
"""
title =  {
    'Rare': ['the Countess', 'Mlle', 'Lady', 'Sir', 'Mme', 'Jonkheer', 'Don'],
    'Miss': ['Ms', 'Miss'],
    'Mrs': ['Mrs'],
    'Master': ['Master'],
    'Army': ['Major', 'Col',],
    'Navy': ['Capt'],
    'Religious': ['Rev'],
    'Medical': ['Dr'],
    'Mr': ['Mr']
    }
title_map = {}
for title_group, title_list in title.items():
    for title in title_list:
        title_map[title] = title_group
assert(df.title.drop_duplicates().loc[df.title.drop_duplicates().map(title_map).isna(), ].empty == True)


# In[15]:


df = df.assign(title=lambda x: x.title.map(title_map))


# ## Class

# In[16]:


sns.catplot(x="pclass", hue="survived", col="sex",
            data=df, kind="count",
            height=4, aspect=.7)
plt.show()


# If you're a male in third class, you are f*'d. If you're a female in third class, it's a coin toss.

# ## Parch

# In[17]:


sns.distplot(df.parch.dropna(), kde=False)
sns.despine(left=True)


# ## Sex

# In[18]:


sex_map = {'male': 0, 'female': 1}
df.loc[:, 'sex'] = df.loc[:, 'sex'].map(sex_map)


# ## Fare by Classes

# In[19]:


ax = sns.barplot(x="pclass", y="fare", data=df)
plt.show()


# First class was between \\$75 and \\$100.
# Second class was \\$20 and third class was about \\$10.

# ## Fare by Classes Adjusted for Inflation

# In[20]:


df = df.assign(fare_today=lambda x: x.fare * 26.07)


# In[21]:


ax = sns.barplot(x="pclass", y="fare_today", data=df)
plt.show()


# First class was between \\$2,000 and \\$2,500.
# Second class was \\$500 and third class was about \\$250. About the cost of a flight.

# [Sourced from the Inflation Calculator](https://www.usinflationcalculator.com/)

# ## Title

# In[22]:


x = df.title
title_le = preprocessing.LabelEncoder()
title_le.fit(x)
df.loc[:, 'title'] = title_le.transform(x)


# ## Embarked

# In[23]:


df.loc[df.embarked.isna(), 'embarked']


# In[24]:


df.loc[:, 'embarked'] = df.loc[:, 'embarked'].fillna(df.embarked.mode().values[0])


# In[25]:


x = df.embarked
embarked_le = preprocessing.LabelEncoder()
embarked_le.fit(x)
df.loc[:, 'embarked'] = embarked_le.transform(x)


# In[26]:


def le_map(le):
    classes = le.classes_
    labels = le.transform(le.classes_)
    return dict(zip(classes, labels))


# ## Fare Bins

# In[27]:


column = 'survived'
df.loc[df.loc[:, column].isna(), column]


# In[28]:


columns_to_be_encoded = 'fare_bins'
x = df.loc[:, columns_to_be_encoded]
fare_le = preprocessing.LabelEncoder()
fare_le.fit(x)
df.loc[:, columns_to_be_encoded] = fare_le.transform(x)


# ## Age Category

# In[29]:


columns_to_be_encoded = 'age_category'
x = df.loc[:, columns_to_be_encoded]
age_le = preprocessing.LabelEncoder()
age_le.fit(x)
df.loc[:, columns_to_be_encoded] = age_le.transform(x)


# ## Random Forest

# In[30]:


ivars = ['pclass', 'sex', 'fare_bins', 'title', 'embarked', 'family_size', 'is_alone',]
X = df.loc[:, ivars]
mask = X.loc[:, ivars].isna().any(axis=1)
assert(X.loc[mask, ].empty)


# In[31]:


dvar = 'survived'
ivars = ['pclass', 'sex', 'title', 'embarked', 'family_size', 'is_alone', 'age_category']
y = df.loc[:, dvar].ravel()
X = df.loc[:, ivars]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


# In[32]:


rf_params = {
    'n_jobs': -1,
    'n_estimators': 500,
     'warm_start': True, 
     #'max_features': 0.2,
    'max_depth': 6,
    'min_samples_leaf': 2,
    'max_features' : 'sqrt',
    'verbose': 0
}
rf = RandomForestClassifier()
rf.fit(X_train, y_train)


# In[33]:


from sklearn.metrics import accuracy_score


# In[34]:


""" Accuracy Score without fare_bins """
y_pred = rf.predict(X_test)
accuracy_score(y_test, y_pred)


# In[35]:


""" Accuracy Score with fare_bins """
y_pred = rf.predict(X_test)
accuracy_score(y_test, y_pred)


# In[36]:


feature_importances = []
for feature, importance in dict(zip(X.columns.tolist(), rf.feature_importances_)).items():
    row = {}
    row['feature'] = feature
    row['importance'] = importance
    feature_importances.append(row)
data = pd.DataFrame.from_dict(feature_importances)
sns.barplot(x='feature', y='importance', data=data)
plt.show()


# In[37]:


import pickle

filename = 'titanic_model.pkl'
with open(filename, 'wb') as f:
    pickle.dump(rf, f)

