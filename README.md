# Textbook Buy/Sell Website
## About
This is Group 13's CMPT 470 Term Project. It is a textbook buy/sell website for students looking to save money on textbooks. The motivation for this project came from the creators getting fed up trying to use textbook buy/sell Facebook pages, which are cluttered and difficult to navigate.

## Setup/Usage
To start the project, have vagrant installed on your machine, and run the command, "vagrant up"
After this, navigate to [the login page](http://localhost:8080/accounts/login) and you should see the website up and running in development mode.

When you start the application, there are no pre-created users (sorry!), so you'll have to create one (or many). Though you can create an account by going to the "Create an account" page, accounts require email activation\*  which complicates things. Instead, we recommend doing the following commands:

- vagrant ssh (from the root project folder after the vagrant vm is running)
- cd project/webroot/
- python3 manage.py createsuperuser (then follow the prompts to enter account information in the terminal)

After this, you can login through the website user interface with the account you have created.

## Features
Currently implemented features include:

- Account Creation
- Account login
- Account Password reset
- Account Email Activation
- Profile page where a user can see the ads they have posted
- Create ad page
- Edit ad page
- View all ads page
- Ad details page
- Edit Textbook page (ads are associated with a textbook, and each textbook has its own wiki-style information page that anyone can edit)

## Fineprint
\*activation emails are currently not setup to be sent. Instead, they are printed to the vagrant machine's command line when the django development server is being run in the foreground. This makes creating an account through the regular application interface more complex which is why we recommend creating an account with the createsuperuser command
