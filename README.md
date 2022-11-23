## CS321 - Software Engineering
*Milestone_5*<br>
*Group 2: Max Duchesne, Rosie Ingmann, Jonna Sosa, Isabella Feng, Dylan Tymkiw, Philipp Bogatyrev, Chloe Zhang*

### Abstract
The goal of this milestone was to deploy our web app to the cloud, implement more features from our sprint backlog, and most importantly start testing our code using pytest. We had already deployed our web app in a previous milestone, so we mostly focused on adding features and increasing code coverage. In the end, we were able to test most of our code and also add in a couple new and exciting features

### Sprint Backlog
High Priority
-Create test files (done)

Medium Priority
-Fix bootstrap on front-end
-Implement live search bar (done)
-Make report files (done)
-Create multiple users and teams by uploading csv files (done)
-Connect to APIs (done)


Low Priority
-Make notifications disappear automatically after 5 seconds (done)
-Front end for specific sleep, readiness, etc. pages



### Results
In this milestone we were able to accomplish a lot in terms of testing code coverage. We were able to achieve over 70% code coverage, which is a great start. 

In terms of features, we were able to implement some of the features in our backlog. We created a live search on the admin home page that queries the backend for team names that match what was typed. We were also able to connect the oura API to a user’s page using token authentication, but we did not yet use the data for any visuals on the front end. 

There were also a couple features that we implemented but didn’t merge yet because of merge conflicts. We made sure that success notifications went away after 5 seconds. We also created a feature that allowed the creation of multiple users at once by uploading a csv file. Finally, we created a functionality for generating reports into a pdf file. 



### Contribution List
In this project, Dylan worked on exploring and connecting the oura API, filtering the athletes in the edit team page and helped Rosie with the search bar. Max worked on generating report files. Isabella worked the testing. Jonna worked on creating multiple users at once with a csv file . Rosie worked on the live search bar. Phil worked on making sure that the success notifications went away.

### Team Reflection
The main goal of this milestone was to get more experience with testing flask apps. This was challenging, especially because testing databases is super complicated. In the end we got something functional but still far from ideal. In addition to testing, we worked on a few extra features like linking APIs that will surely help in the upcoming milestones.

### Extensions
-Learn and use one of the API that are needed for this project, i.e. Hawkings Dynamics, MyFitnessPal, and sleep monitoring. 
-Write your report in Markdown as a readme file in your repository, including table images and appropriate tags and content.




