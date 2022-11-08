## CS321 - Software Engineering
*Milestone_4*<br>
*Group 2: Max Duchesne, Rosie Ingmann, Jonna Sosa, Isabella Feng, Dylan Tymkiw*

### Abstract
For this project, we had to collaborate within our teams using git and GitHub, in order to peopare an interactive version of the Athletic Management System (AMS) using Flask. For this project we have to coordinate and conduct a full Agile Sprint implementing the backlog. The tasks included creating a database, pulling real data into our application to display, creating login/logout functionality along with permissions, and creating the ability to add new users and teams. 

### Sprint Backlog
High Priority
- Restructure repository to match Flask requirement (Completed)
- As a coach, I want to view my athlete's information page when I click on their hyperlinked name (completed)
- As a user, I want to access all webpages that I have access to (completed)
- As a user I want to see relevant graphs from my stats so that Have useful information (completed)
- As a user I want to see relevant graphs from my stats so that Have useful information (completed)
- As a user, I want to access my account when I input the correct username and password (completed)
- As a super admin, I want to be able to access and modify the permissions for all users (Peak, coaches, players) (completed)

Medium Priority
- As a PEAK member, I want to be able to set the ready-to-play status of players (completed)
- As a PEAK team member, I want to be able to add notes to a player's file so that the coach and the player is aware of any other factors impacting a player's performance (completed)
- As a coach, I want to be able to access my team's sleep and recovery data to be able to plan out practices (completed)
- As a coach, I want to be able to access my team's sleep and recovery data to be able to plan out practices (completed)

We actually ended up completing all of our user stories, even though some might need more work/improvements in the next sprint.


### Results
The result of this milestone was a working flask app that is connected to a database. Our database holds users, teams, and athletes and is added to when a new user or team is created. We also implemented permissions and the admin ability to change the permissions of other users. 

### Contribution List
In this project, Dylan worked on creating the database along with the auth, login, create_user, create_team functionalities, and deploying the website as extension. Max worked on the functionality of peak members being able to create and send notes. Isabella worked on the HTML inheritance, frontend lists that connect to backend, and Agile charts as extensions. Jonna worked on passing database information into the current webpages. Rosie worked on parsing csv files to display real data in the website and connecting javascript to flask. 

### Team Reflection
In this milestone, we were improving in our ability to use git and resolve any merge conflicts that came up, however git still challenged us at times. The biggest hurdle in this milestone was probably the learning curve of flask as well as the task of choosing how to structure the database. There were many different directions we could have gone in and we had to make a lot of decisions. In the end, this project helped us understand how to connect a database and backend to our previously static website.

### Extensions
1. Implement additional features from your backlog.
- Dylan used Azure to deploy our website, and even though we didn’t get to show it in class presentation, we are able to access our website online.
- We used the json graphs. And our visuals adjust its size automatically, so our website still looks great when viewing from a device with a different proportion, such as a mobile phone. 
2. Burndown chart of your project. <br>
A burndown chart, one of the most common and useful Agile metrics, is created using Excel and is shown below. It demonstrates our daily efforts in comparison to the ideal burndown, as well as actual and planned hours working every day.
![extension 2](/website/static/assets/report_images/extension2.png)
3. Write your report in Markdown as a readme file in your repository, including table images and appropriate tags and content. <br>
Done.
4. Suggest your own creative extensions. <br>
We created an auto-assign workflow that auto-assigns people to issues and pull requests.


