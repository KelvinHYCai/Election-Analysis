Election Analysis Data Science Project
===================
This write-up details the why, what, and how of my analysis on the 2012 election. Polled information from the Huffington Post was used to better understand voters and nominees and analyze factors that influenced voters. 

Below are the steps I took towards my goal. 


----------

Data Requesting and Description
-------------
*Pandas*, an online software library for data manipulation in Python, served to import election data from a Huffington Post URL. After setting the poll data as a Pandas dataframe, a quick look at a sample of the data showed a few unnecessary variables: Pollster URL, Source URL, Question Text, and Question Iteration. Each observation of the poll represented a poll, which each varied in size. Each poll was broken down into party affiliation. 


----------


Observations and Analysis
-------------------
**Party Affiliation**
Visualizing all affiliations in a count plot showed that the vast majority of polls had "None" as their affiliation, with "Democratic" as a second. This showed that the polled people were mostly neutral, leaning towards a Democratic affiliation.  

Plotting the average and standard error of the number each candidate's affiliates revealed that Obama and Romney were surprisingly close overall. 
Subtracting the Romney alignment from the Obama alignment and then plotting it against the poll data sorted by Start Date allowed for analysis of the difference alignments over time. The resulting graph did not give significant information at first glance, but finding the date of each nominee debate and aligning them on the graph revealed a significant dip for Romney after the first debate, then another for Obama after the second debate. 

**Donors**
The next goal was to look at another instrumental part of the campaigns: donors. I specifically wanted to look at the total amount of donations for each candidate, the average donation and who they're coming from, as well as differences between donors towards the Republicans and Democrats.

After plotting both the number of donors and total amount of donations for each candidate, it became very apparent that Obama led both fields by a large margin. So although the democrats had less overall donations, Obama had the advantage that the Republican donations were more split across each Republican candidate. 

Next was to better understand the distribution of donors and their respective professions. A cutoff sum of one million dollars was set, and professions that had donated an amount over that cutoff were all plotted. After deleting unavailable data and combining variables like "CEO" and "C.E.O", the top three professions for donations were: retired people, homemakers, and attorneys, in order.

**Conclusion**
After sorting and cleaning up the data pulled from Huffington Post, analysis was possible. Each debate brought significant change to what was overall a close race between alignment towards Obama and Romney. Taking a closer look at each party's and candidate's donors revealed that although the Democrats as a party had less donations, Obama accounted for the vast majority of their donations, giving him the edge over the more evenly distributed funds of the Republicans. Sorting the donors by their professions saw retired people, homemakers, and attorneys as the most significant donors.
