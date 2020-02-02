# Playing Around with Flask
This repository is used to keep track of the codes and learning from playing around with flask.

Website used for guidance:
* https://www.rithmschool.com/courses/flask-fundamentals

# Lesson from PlayTest
## Each route contains a function
* Think of the function as the backend for the particular route
* What should be done when loading the page
* What should be done with the data that is sent to it
* **it does not have to render a page, it can just process something and redirect elsewhere

## Jinja 2 templating
* `{ ... }` - evaluation
* `{{ ... }}` - print

## SQL (Postgres)
* **Remember connection requires user and password
* Basic - Use `db.py` to manage actions on database
* SQLALchemy - use models to manage actions on database (better)

## Migrations
Never DDL the database directly, use migrations (`manage.py`)
* Used to allow keep multiple users up to date and ensures everyone is using the same version

## One-to-many Associations
With one-to-many associations, use `db.relationship(...)` to let flask-alchemy know the relationship
