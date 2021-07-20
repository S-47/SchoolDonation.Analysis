import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import chart_studio.plotly as pl
import plotly.offline as of
import cufflinks as cf
import datetime as dt

of.init_notebook_mode(connected=True)
cf.go_offline()
donations=pd.read_csv("Donations.csv")
donors=pd.read_csv("Donors.csv")
projects=pd.read_csv("Projects.csv")
resources=pd.read_csv("Resources.csv")
schools=pd.read_csv("Schools.csv")
teachers=pd.read_csv("Teachers.csv")
data=pd.merge(donations, projects, how="inner", on="Project ID")
data2=pd.merge(data, donors, how="inner", on="Donor ID")
data3=pd.merge(data2, schools, how="inner", on="School ID")
data4=pd.merge(data3, teachers, how="inner", on="Teacher ID")
a=data4.columns.values.tolist()
print("Which 10 states have the most number of schools that opened projects to gather donations?")
s=schools['School State'].value_counts().sort_values(ascending=False).head(10)
print(s)
s.iplot(kind="bar", xTitle="States", yTitle="Number of school", title="Number in schools involved in projects by  states")
print("What are the top 10 states in which schools gathered most amount of average donations for their projects?")
s2=data4.groupby("School State")["Donation Amount"].mean().sort_values(ascending=False).head(10)
#grouping the terms acording to the first parantesis: School State and getting the values of the second parantesis Donation
s2.iplot(kind="bar", xTitle='State', yTitle='Average donations per project', Title='Top 10 states with maximum donation', colorscale='paired')


print("Analyse the Maximum, minimum, mean, median, 25% and 75% percentiles of Donations")

mean=np.mean(data4['Donation Amount'].dropna())
median=np.median(data4['Donation Amount'].dropna())
percentiles=np.percentile(data4['Donation Amount'].dropna(), [25,75])
minimum=(data4['Donation Amount'].dropna().min())
maximum=(data4['Donation Amount'].dropna().max())
print('mean donation amount is: ', np.round(mean,2))
print('median donation amount is: ', median)
print('25% and 75%  donation amount is: ',percentiles)
print('minumum donation amount is: ', minimum)
print('maximum donation amount is: ', maximum)


print("In which states there are more donations done by donors? ")
s3=s3=data4.groupby('Donor State')['Donation ID'].count().sort_values(ascending=False).head(15)
s3.iplot(kind='bar', xTitle='State', yTitle='Number of donations', title='Donations Count', colorscale="paired")


print("""Is there a relationship between the number of projects offered and number of donations made by donors."
       Which state performing better in this case? How many of them responding project requests
       below average and which states are performing best in terms of donations per project?""")
s4=schools['School State'].value_counts()
s5=data4.groupby('Donor State')['Donation ID'].count()
df=pd.concat([s4,s5], axis=1,keys=['Projects', 'Donations'])
df.iplot(kind='scatter', xTitle='Projects',
         yTitle='Donations', title='Projects vs Donations',
         symbol='x', colorscale='paired', mode='markers')

slope,intercept=np.polyfit(df.Projects, df.Donations,1)
x=np.array([df.Projects.min(),df.Projects.max() ])
y=slope*x+intercept #mx+c
plt.plot(x,y)

print("How many different project types exists")
s6=data4['Project Type'].value_counts()
s7=data4.groupby('Project Type')['Donation Amount'].sum().astype(int)
plt.subplot(2, 1, 1)
plt.pie(s6, startangle=90)
plt.legend(loc='upper left')
plt.subplot(2, 1, 1)
plt.pie(s7, startangle=90)
plt.tight_layout()
plt.margins(0.05)
fig=plt.gcf()
fig.set_size_inches(25,15)

print('How many project subject category trees exists? Which ones attracted the most donations?')
data4['Project Subject Category Tree'].nunique()
s8=data4['Project Subject Category Tree'].value_counts()
s9=data4.groupby('Project Subject Category Tree')['Donation Amount'].sum().astype(int).sort_values(ascending=False).head(15)
s10=s9/1000000
s10.iplot(kind='bar', xTitle='Project Subcategory', yTitle='Donation amount in milions',
         title='Donation amount by project subject', colorscale='paired')

print('What is the mean time that takes a project to be fully funded after posted and how it varies between states?')
data4[['Project Posted Date', 'Project Fully Funded Date']].isnull().sum().head()
data4[['Project Posted Date', 'Project Fully Funded Date']].head()
data4['Funding Time']=data4['Project Fully Funded Date']-data4['Project Posted Date']
data4[['Funding Time', 'Project Posted Date', 'Project Fully Funded Date']].head()
data4[['Funding Time', 'Project Posted Date', 'Project Fully Funded Date']].isnull().sum().head()
data5=data4[pd.notnull(data4['Funding Time'])]
data5[['Funding Time', 'Project Posted Date', 'Project Fully Funded Date']].isnull().sum().head()
import datetime as dt
data5['Funding Time']=data5['Funding Time'].dt.days
data5[['Funding Time', 'Project Posted Date', 'Project Fully Funded Date']].head()
wrong_overall_mean_time=data5['Funding Time'].mean() #it is wrong because there are a number of project's id that contains
                                                     #same kind of projects , it just count one value and take that value
                                                     #for all the other same project id
print(wrong_overall_mean_time)
overall_mean_time=data5.groupby('Project ID')['Funding Time'].mean()
output=overall_mean_time.mean()
print(output)

print("Average  funding time for each state")
state_project_funding_time=data5.groupby(['School State', 'Project ID'])['Funding Time'].mean()
print(state_project_funding_time)
state_average_project_funding_time=state_project_funding_time.groupby('School State').mean()
print(state_average_project_funding_time)


print('''Which states are the best and which are the worst performing in terms of this criteria
        (mean project fully funded time''')
fast=state_average_project_funding_time.round()
fast[fast<32].sort_values().head(10)
fast_funding=fast[fast<32].sort_values().head(10)
fast_funding.iplot(kind='bar', xTitle='States', yTitle='Fully funding time ( in days) ',
                  title='States that fund projectc earlier than others', colorscale='paired')

slow=state_average_project_funding_time.round()
slow[slow>32].sort_values(ascending=False).head(10)
slow_funding=fast[fast>32].sort_values(ascending=False).head(10)
slow_funding.iplot(kind='bar', xTitle='States', yTitle='Fully funding time ( in days) ',
                  title='States that fund projectc later than others')

