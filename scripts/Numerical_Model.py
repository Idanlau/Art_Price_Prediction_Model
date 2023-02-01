#!/usr/bin/env python
# coding: utf-8

# In[130]:


import pandas as pd


# In[131]:


df = pd.read_csv("https://raw.githubusercontent.com/Idanlau/Cloudera_Hackathon/Word-Encoding/artist_fame.csv")
df


# In[132]:


movement_df = pd.get_dummies(df['movement'])
period_df = pd.get_dummies(df['period'])
movement_df.drop(columns='[nan]',inplace=True)
period_df.drop(columns='[nan]',inplace=True)


# In[133]:


df.drop(columns='movement',inplace=True)
df.drop(columns='period',inplace=True)


# In[134]:


df = df.join(movement_df)


# In[135]:


df = df.join(period_df)


# In[136]:


df


# In[137]:


df['yearCreation'] = pd.to_numeric(df['yearCreation'],errors = "coerce")
nan_count = df['yearCreation'].isna().sum().sum()
#print(nan_count) #104/753 = around 13.8 percent of data missing for years!
df['yearCreation'] = df['yearCreation'].fillna(df['yearCreation'].median()) #Fill it with the median, any better approaches?
df['yearCreation']


# In[138]:


df['price'] = df['price'].str.replace("USD","") #Dropping the USD string so its just numbers
df['price'] = df['price'].str.replace(".","")
df['price'] = pd.to_numeric(df['price'])
df['price']


# In[139]:


from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()
condition = vectorizer.fit_transform(df['condition'])
condition


# In[140]:


vectorizer.get_feature_names_out()


# In[141]:


print(condition.toarray())


# In[142]:


condition_labels = pd.DataFrame(condition.toarray(),columns=vectorizer.get_feature_names())
condition_labels


# In[143]:


from sklearn.feature_extraction.text import CountVectorizer
vectorizer2 = CountVectorizer()
signed = vectorizer2.fit_transform(df['signed'])
signed


# In[144]:


vectorizer2.get_feature_names_out()


# In[145]:


signed_labels = pd.DataFrame(signed.toarray(),columns=vectorizer2.get_feature_names())
signed_labels


# In[146]:


df.drop(columns='signed',inplace=True)
df.drop(columns='condition',inplace=True)
df.drop(columns='artist',inplace=True)


# In[147]:


signed_labels = signed_labels.astype(int)
condition_labels = condition_labels.astype(int)


# In[148]:


df = df.join(condition_labels)


# In[149]:


df


# In[150]:


df = df.join(signed_labels,lsuffix="_left", rsuffix="_right", how='right')


# In[151]:


df = df.drop(df.columns[[0, 1, 2,5]],axis = 1)


# In[152]:


df


# In[161]:


from sklearn.model_selection import train_test_split
X = df.loc[:, ~df.columns.isin(['artist', 'title', 'signed','condition','title_left','price'])]
Y = df["price"]
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)


# In[162]:


from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
regr = RandomForestRegressor(max_depth=20, random_state=0)
regr.fit(X_train,y_train)
print("Training Score: ",regr.score(X_train,y_train))
print("Testing Score: ",regr.score(X_test,y_test))
print("Testing Mean Absolute Error: ", mean_absolute_error(y_test,regr.predict(X_test)))


# In[163]:


import numpy as np
importances = regr.feature_importances_
sorted_indices = np.argsort(importances)[::-1]
 
feat_labels = df.columns[1:]
 
for f in range(40):
    print("%2d) %-*s %f" % (f + 1, 10,
                            feat_labels[sorted_indices[f]],
                            importances[sorted_indices[f]]),"index: ",df.columns.get_loc(str(feat_labels[sorted_indices[f]])))


# In[164]:


from sklearn.linear_model import LinearRegression
import numpy as np
regr = LinearRegression()
regr.fit(X_train,y_train)
print("Training Score: ",regr.score(X_train,y_train))
print("Testing Score: ",regr.score(X_test,y_test))
print("Testing Mean Absolute Error: ", mean_absolute_error(y_test,regr.predict(X_test)))


# In[165]:


from sklearn.neighbors import KNeighborsRegressor
regr = KNeighborsRegressor()
regr.fit(X_train,y_train)
print("Training Score: ",regr.score(X_train,y_train))
print("Testing Score: ",regr.score(X_test,y_test))
print("Testing Mean Absolute Error: ", mean_absolute_error(y_test,regr.predict(X_test)))


# In[166]:


# import libraries
from sklearn.feature_selection import RFE

# define RFE
rfe = RFE(estimator=RandomForestRegressor(max_depth=20, random_state=0),n_features_to_select=15)
# fit RFE
rfe.fit(X, Y)


# In[167]:


forest = RandomForestRegressor(max_depth=20, random_state=0)
_ = forest.fit(rfe.transform(X_train), y_train)
print("Training Score: ",forest.score(rfe.transform(X_train),y_train))
print("Testing Score: ",forest.score(rfe.transform(X_test),y_test))
print("Testing Mean Absolute Error: ", mean_absolute_error(y_test,forest.predict(rfe.transform(X_test))))


# In[168]:


import numpy as np
importances = forest.feature_importances_
sorted_indices = np.argsort(importances)[::-1]
 
feat_labels = df.columns[1:]
 
for f in range(15):
    print("%2d) %-*s %f" % (f + 1, 10,
                            feat_labels[sorted_indices[f]],
                            importances[sorted_indices[f]]),"index: ",df.columns.get_loc(str(feat_labels[sorted_indices[f]])))


# In[169]:


print(X.shape[1])


# In[170]:


from joblib import dump, load
dump(forest, 'ArtNum.joblib') 


# In[1]:


print("The model complexity has been greatly reduced using recursive feature elimination from 1286 features down to 15 features. However the simplified model estimation is around 300 dollars worse which is about 10 percent worse.")


# In[ ]:




