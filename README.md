# Textbook Buy/Sell Website
## About
This is Group 13's CMPT 470 Term Project. It is a textbook buy/sell website for students looking to save money on textbooks. The motivation for this project came from the creators getting fed up trying to use textbook buy/sell Facebook pages, which are cluttered and difficult to navigate.

## Setup/Usage
To start the project, have vagrant installed on your machine, and run the command, "vagrant up"
After this, navigate to [the login page](http://localhost:8080/accounts/login) and you should see the website up and running in development mode.

When you start the application, there are two pre-created accounts: test and test2. Both accounts have the same password: asdfasdf123

You can also create your own account by using the sign up page (linked to on the login page)

## Features
Currently implemented features include:

- Account Creation
- Account login
- Account Password reset
- Profile page where a user can see the ads they have posted
- Create ad page
- Edit ad page
- Delete ads
- View all ads page
- Ad details page
- Edit Textbook page (ads are associated with a textbook, and each textbook has its own wiki-style information page that anyone can edit)
- User-to-user messaging: each conversation between two users has its own page, and each user has a page that lists all the ongoing conversations they have
