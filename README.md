# myEXPENSES Tracker
#### Video Demo:  https://www.youtube.com/watch?v=e4BPP7cb0MU
#### Description:
This project is an expenses and income tracking app that allows users to post daily expenses and/or income.
The application used Python3 and incorporates the open-source Flask framework for web-app logic. The project is part of my submission to Harvard University's [CS50](https://www.edx.org/course/introduction-computer-science-harvardx-cs50x) final project. 
  
![logo](https://user-images.githubusercontent.com/86846386/145723112-935f9399-1a57-4fd0-8e76-67bcb41f6cd9.png)

## Background
### How did the project idea come about?
The motivation for the project was to create a web app that will simplify daily expenses and income tracking activities into a dedicated platform. 
Below are the objectives to be included in the project:

1. Solve a Business Problem
2. Simple UI
3. CRUD Functionality
4. Authentication/Authorization
5. Database

### Problem to solve
The problem to solve was to visualize such daily transactions (expenses and income) into a dashboard so that users can better understand their income and expenses behaviour. For example, the use of a combination of cards and charts were necessary to aggregate and provide insights to the data submitted by users for each income/expense entry. 

Users typically want to have some degree of interaction with their data hence, this project solves that problem by allowing users to access a variety of programmed features such as filters of dates "from" and "to" of when they made the entry and the option to either view income or expenses data. Validation prompts were included in the form of modals to ensure user's do not accidentally delete a record unintentionally. 

Furthermore, users may choose to edit their expense/income data, which is enabled in the home page, upon logging into the app. 

The final problem is about database security, which is handled by the 'sha256' algorithm to cryptographically hash user passwords instead of storing plain text passwords into the database.

### Tech Stacks/ Resources Used
- Python
  - Flask (with Jinja templating)
- JavaScript
    - Chart.js
- CSS
  - Bootstrap
- HTML

### Design Choices
  - Object-Oriented Programming (OOP) - To instantiate objects based on classes for the various database models and web forms. This assisted in improving reusability and cleaner code (i.e. reducing unnecessary lines of code).
  - Data Visualization - Chart.js was used as it is an open-source JavaScript library that produces interactive charts for data visualization. It supports various chart types such as bar, line, area, pie (doughnut) etc. Other visualization tools such as Matplotlib, Plotly and D3 were considered however, due to the simplicity, well written documentation and responsiveness of Chart.js, it was chosen for this project.
 - Database Design - Object-relational mapping (ORM) with the Flask SQLAlchemy library, to map object parameters to the structure of a layer RDBMS table. CRUD operations can be executed without writing raw SQL statements.

## Setup & Installation

Make sure you have the latest version of Python installed.

```bash
git clone <repo-url>
```

```bash
pip install -r requirements.txt
```

## Running The App

```bash
python project_app.py
```

## Viewing The App

Go to `http://127.0.0.1:5000`


## Functionality of Project
The flow of the application starts from the user running the app from their command line interface (CLI). The user is redirected to the login page if they are not yet registered or signed in. If the user is authenticated, the index page will display a table that summarizes all income and expenditure entries submitted, and their amount (will be empty initially). 

Users can add expenses and/or income by selecting add expenses/add income pages in the navigation bar. Both pages will redirect the user to fill in a form containing the amount, transaction type and category. The form handles various conditions in the back-end such as empty fields and prompts the user accordingly on the validity of their form submission. Flask's "flash" function is used to inform of errors or successful requests. 

The Sqlite3 database operates in the back-end upon any "POST" or "GET" request using the CRUD principle, which facilitates reading, searching, and changing or updating information. Upon validation on submit, the record will be automatically updated into the table in the index page. Meanwhile, the dashboard page can be accessed to view interactive charts created by the chart.js library.
  
### Directory Structure
```  
├── application             # Contains the main project files and database
  ├── static                # Contains logos and static images
    ├── css                 # Contains external stylesheets
  ├── templates             # Contains templates for each page of the application
    ├── helpers             # Contains template for modals (pop-up boxes)
├── screenshots             # Contains screenshots of the working application
```
  
