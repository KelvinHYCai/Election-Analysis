
# coding: utf-8

# In[1]:

# For data
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import io as io

# For visualization
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().magic('matplotlib inline')

from __future__ import division


# In[2]:

# Use to grab data from the web(HTTP capabilities)
import requests

# We'll also use StringIO to work with the csv file, the DataFrame will require a .read() method
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


# In[3]:

# This is the url link for the poll data in csv form
url = "http://elections.huffingtonpost.com/pollster/2012-general-election-romney-vs-obama.csv"

# Use requests to get the information in text form
source = requests.get(url).text

# Use StringIO to avoid an IO error with pandas
poll_data = StringIO(source) 


# In[4]:

# Set poll data as pandas DataFrame
poll_df = pd.read_csv(poll_data)

# Let's get a glimpse at the data
poll_df.info()


# In[5]:

poll_df.head()


# In[6]:

# Factorplot the affiliation
sns.countplot("Affiliation",data=poll_df)


# In[7]:

sns.countplot('Affiliation',data=poll_df,hue='Population')


# In[11]:

poll_df.head()
poll_df = poll_df.drop(['Question Text', 'Question Iteration'], axis=1)


# In[12]:

poll_df.head()


# In[14]:

poll_df = poll_df.drop(['Other'], axis=1)
# First we'll get the average
avg = pd.DataFrame(poll_df.mean()) 
avg.drop('Number of Observations',axis=0,inplace=True)

# After that let's get the error
std = pd.DataFrame(poll_df.std())
std.drop('Number of Observations',axis=0,inplace=True)

# now plot using pandas built-in plot, with kind='bar' and yerr='std'
avg.plot(yerr=std,kind='bar',legend=False)


# In[22]:

# Concatenate our Average and Std DataFrames
poll_avg = pd.concat([avg,std],axis=1)

#Rename columns
poll_avg.columns = ['Average','STD']

#Show
poll_avg


# In[23]:

# For timestamps
from datetime import datetime


# In[24]:

# Create a new column for the difference between the two candidates
poll_df['Difference'] = (poll_df.Obama - poll_df.Romney)/100
# Preview the new column
poll_df.head()


# In[25]:

# Set as_index=Flase to keep the 0,1,2,... index. Then we'll take the mean of the polls on that day.
poll_df = poll_df.groupby(['Start Date'],as_index=False).mean()

# Let's go ahead and see what this looks like
poll_df.head()


# In[28]:

# Plotting the difference in polls between Obama and Romney
fig = poll_df.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle='-',color='blue')


# In[38]:

#In order to find where to set the x limits for the figure we need to find out where the index for the 
#month of October in 2012 is. 

# Set row count and xlimit list
row_in = 0
xlimit = []

# Cycle through dates until 2012-10 is found, then print row index
for date in poll_df['Start Date']:
    if date[0:7] == '2012-10':
        xlimit.append(row_in)
        row_in +=1
    else:
        row_in += 1
        
min(xlimit)


# In[39]:

max(xlimit)


# In[41]:

# Start with original figure
fig = poll_df.plot('Start Date','Difference',figsize=(12,4),marker='o',linestyle='-',color='purple',xlim=(329,356))

# Now add the debate markers
plt.axvline(x=329+2, linewidth=4, color='grey')
plt.axvline(x=329+10, linewidth=4, color='grey')
plt.axvline(x=329+21, linewidth=4, color='grey')


# In[43]:

donor_df = pd.read_csv('Election_Donor_Data.csv')


# In[44]:

# Get a quick overview
donor_df.info()


# In[45]:

donor_df.head()


# In[55]:

# Get the mean donation
don_mean = donor_df['contb_receipt_amt'].mean()

# Get the std of the donation
don_std = donor_df['contb_receipt_amt'].std()
# %(don_mean,don_std)
print ('The average donation was ' + str(don_mean) + ' with a std of ' + str(don_std))


# In[59]:

# The standard deviation is too large, so we need to find any factors that are influencing it too much.
# Let's make a Series from the DataFrame, use .copy() to avoid view errors
top_donor = donor_df['contb_receipt_amt'].copy()

# Now sort it
top_donor.sort_index()

# Then check the Series
top_donor


# In[61]:

#Lets get rid of the negative values and find the most common donations
# Get rid of the negative values
top_donor = top_donor[top_donor >0]

# Sort the Series
top_donor.sort_values()

# Look at the top 10 most common donations value counts
top_donor.value_counts().head(10)


# In[62]:

# Let's dive deeper into the data and see if we can seperate donations by Party
# In order to do this we'll have to figure out a way of creating a new 'Party' column. 
# Grab the unique object from the candidate column
candidates = donor_df.cand_nm.unique()
#Show
candidates


# In[63]:

# Dictionary of party affiliation
party_map = {'Bachmann, Michelle': 'Republican',
           'Cain, Herman': 'Republican',
           'Gingrich, Newt': 'Republican',
           'Huntsman, Jon': 'Republican',
           'Johnson, Gary Earl': 'Republican',
           'McCotter, Thaddeus G': 'Republican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Republican',
           'Pawlenty, Timothy': 'Republican',
           'Perry, Rick': 'Republican',
           "Roemer, Charles E. 'Buddy' III": 'Republican',
           'Romney, Mitt': 'Republican',
           'Santorum, Rick': 'Republican'}

# Now map the party with candidate
donor_df['Party'] = donor_df.cand_nm.map(party_map)


# In[64]:

# Clear refunds
donor_df = donor_df[donor_df.contb_receipt_amt >0]

# Preview DataFrame
donor_df.head()


# In[65]:

# Groupby candidate and then displayt the total number of people who donated
donor_df.groupby('cand_nm')['contb_receipt_amt'].count()


# In[66]:

# As seen above, Obama leads with the most number of donations. Now let's see the total amount of donations per candidate
donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()


# In[68]:

# These raw numbers are hard to read, so let's visualize them
cand_amount = donor_df.groupby('cand_nm')['contb_receipt_amt'].sum()
cand_amount.plot(kind='bar')


# In[69]:

# The donation gap between each nominee is now very apparently clear. Although Obama had the most donations himself,
# let's see how the Democrats did versus the Republicans
donor_df.groupby('Party')['contb_receipt_amt'].sum().plot(kind='bar')


# In[70]:

# It can be seen that although Obama was in the lead, he could not carry all the Democrats against the Republicans.
# This also means that he had the advantage of Republican funding being split across multiple candidates.
# Use a pivot table to extract and organize the data by the donor occupation
occupation_df = donor_df.pivot_table('contb_receipt_amt',
                                index='contbr_occupation',
                                columns='Party', aggfunc='sum')


# In[71]:

# Let's go ahead and check out the DataFrame
occupation_df.head()


# In[72]:

# Check size
occupation_df.shape


# In[73]:

# Set a cut off point at 1 milllion dollars of sum contributions
occupation_df = occupation_df[occupation_df.sum(1) > 1000000]


# In[74]:

# Now let's check the size!
occupation_df.shape


# In[75]:

# Horizontal plot, use a convienently colored cmap
occupation_df.plot(kind='barh',figsize=(10,12),cmap='seismic')


# In[76]:

# Drop the unavailble occupations
occupation_df.drop(['INFORMATION REQUESTED PER BEST EFFORTS','INFORMATION REQUESTED'],axis=0,inplace=True)


# In[77]:

# Combine CEO and C.E.O rows
# Set new ceo row as sum of the current two
occupation_df.loc['CEO'] = occupation_df.loc['CEO'] + occupation_df.loc['C.E.O.']
# Drop CEO
occupation_df.drop('C.E.O.',inplace=True)


# In[78]:

# Repeat previous plot!
occupation_df.plot(kind='barh',figsize=(10,12),cmap='seismic')


# In[ ]:



