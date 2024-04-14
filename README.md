# analytics-rental-demands
A project to analyze declining rental demand in housing and proposals for scalability of csv in-house databases to SQL


# Contents:
analyzer.py: contains python application for csv data cleaning and manipulation.
project-report.pdf: Details the process and steps taken for each task and provide scalability solutions.
arff-files: sets of arff files used to analyze data in Weka and build predictive models
csv-files: original csv dataset
diagram-and-results: diagrams created for the relational models and results gained from analysis of data in Weka


# Project Statement:
The demand for rental housing decreased from 12.3% to 11.1% in mid-2022, and is predicted to further decline to 4.5% by the end of 2024 [1]. A company housing manager is concerned by this downward trend, and you have been assigned tasks to identify and investigate three problem areas and develop potential solutions to these problems. You are required to utilize the data mining techniques (regression/classification) and tools (WEKA version 3.8.5) that have been taught in the Big Data Analytics module and only use the “Housing” data set provided, which can be cleaned and used to generate specific output. 

Reference:</br>
[1] R. Donnell (2023, Nov. 3). Rental Market report: what’s happening to rents? [Online]. Available: https://www.zoopla.co.uk/discover/property-news/rental-market-report-march-2023/ [Accessed: Nov. 3, 2023]


# Tasks:

<h2>1. Rental “demand” investigation: </h2>

The housing manager has the following question: which characteristics of a property determine the level of customer demand? To answer this, the manager proposes looking into the following:
a.	Which of the “discrete variables” (e.g. bedrooms, smoking_allowed) have the potential to predict a “low demand” property? Do these variables also have the potential to predict a “high demand” property?
b.	Ascertain if there is a correlation (either positive or negative) between the “demand” for a property and its “rent” and “type”.  
c.	Identify if the size of the property “sqfeet” has an optimal range for generating high “demand”. 
You should utilize Weka and build a classifier or regression model to perform this analysis. 
<h2>2. Storing data and scalable solutions: </h2>	
<h3>Part 1: Design a relational database </h3>	

The housing manager is considering an alternative to the current flat file (CSV) system that stores the majority of their data. You have been tasked with designing a relational database to store the provided dataset ‘Housing’ in the flat file system. You will need to decide, and justify, which features to include and/or adapt to store all the provided data. To allow the housing manger to assess the feasibility of this you should provide the following:

a.	Produce a database design (in the form of a UML standard ER diagram with normalization to 3NF) for the given data. 
b.	Present sample SQL for the database you have created (given your ER diagram diagram) as follows:
i.	Demonstrate the SQL that you would write to enter a new line of data, covering all relevant attributes.  
ii.	Extract the ‘description’ for all properties with a rent equal to or less than 1000*, allows both cats and dogs, and is in the state represented by ‘ca’.
iii.	Extract the average rental value for each state so they can be compared.  
* No currency is specified in the dataset. 

<h3>Part 2: Consider scaling </h3>	

The housing manger is also considering longer term solutions for their business, given their intention to set up international offices across the globe. This would generate considerably more data (tens of megabytes). To be able to utilize this data effectively requires a rapid-response system for the business to be responsive in a global rental environment. Assume certain messages are required to be sent as soon as certain automated analysis results are returned of a certain value (e.g. a count of items of a particular type exceeds a pre-determined threshold). With reference to specific details in the data set, present a way that you could use appropriate technologies to spread the load over multiple computers and justify why this would be a good approach.

<h2>1.Considering public-facing application:  </h2>	

The housing manager is considering the development of a public-facing application, to assist in promoting the expansion of his business, and to make it easier for potential clients to view and select from current offerings. As part of this, he is also considering capturing (via an online form) the personal details of potential clients so he can provide recommendations to revisiting clients.  

Identify the three most salient privacy issues that he needs to consider before embarking on this new venture. You should consider the potential issues in the context of the new application, the rental agencies’ intentions regarding data analysis (Task 1), and the move towards permanent data storage (Task 2). For each of the issues you have identified, discuss the strategies that could be employed to address each of them in the context of the given scenario and data set.

