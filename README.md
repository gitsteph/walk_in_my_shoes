# Walk in My Shoes

## Purpose
A game based on Women's Health Specialists' "Walk in My Shoes" curriculum.
[NEED CONTENT]

## Features
[NEED CONTENT]

## Team
* Andrea (@bobicka): Animation, Illustration, UX
* Grant (@grant): Engineering, UX
* Somer: Content, UX
* Stephanie (@gitsteph): Engineering, Project Management
* Steven (@steven-jeram): Engineering, Content

## Getting Started

### 1. Download the repository
```bash
git clone https://github.com/gitsteph/walk_in_my_shoes.git
```

### 2. Install `pip`, `virtualenv`, create a new virtual environment, and activate it
(if `pip install virtualenv` does not work, try uninstalling and reinstalling virtualenv...
or try deleting `sudo rm -r /usr/local/var/postgres` then installing virtualenv again)

To install:
```bash
$ sudo easy_install pip
$ pip install virtualenv
$ virtualenv venv
```
To activate:
```bash
$ source venv/bin/activate
```
To deactivate:
```bash
(venv)$ deactivate
```

### 3. Install dependencies from `requirements.txt`
```bash
$ source venv/bin/activate
(venv)$ pip install -r requirements.txt
```

### 4. Install PostgreSQL
To install:
```bash
$ brew install postgresql
```
To check the version:
```bash
$ postgres -V
```
To start postgres:
```bash
$ brew services start postgresql
```

### 5. Create a new database in PostgreSQL and login with your user account
```bash
$ createdb `whoami`
$ psql
```
Change your password, create a database specifically for AAH, and grant privileges to that databaes to your user.
```postgresql
your_username=# ALTER USER your_username WITH PASSWORD 'your_new_pw';
your_username=# CREATE DATABASE aah;
your_username=# GRANT ALL PRIVILEGES ON DATABASE aah TO your_username;
```
To access your database directly:
```bash
$ psql aah
```
To see all your tables:
```bash
$ psql aah
aah=# \dt
```
(TODO: Figure out a way to make this more secure if needed/double-check the above steps)

### 6. Create a `secrets.sh` file for any future keys inside of the main project directory
```bash
$ touch secrets.sh
```

### 7. Create all tables inside an `ipython` shell
This should be handled automatically `db.create_all()` in `model.py` when you first run the server.
However: If you change the schema of an existing model, you'll need to delete the table that was
changed.  The next time (and every time) you run the server (`python server.py`), tables that do not
exist will be created using the updated models.

After changing the schema of an existing table:
```bash
(venv)$ psql aah
psql (9.5.3)
aah=# DROP TABLE tablename_of_model_you_changed CASCADE;
```

### 8. Run server
```bash
(venv)$ python server.py
```
To access content/test routes, type in the address bar: `http://localhost:5000/your_route_name`

### 9. ipython!
Executing below will load up the contents of the file you specify into an interactive ipython session.
```bash
(venv)$ ipython -i name_of_file.py
```

### 10. Seeding your database tables
```bash
(venv)$ ipython -i seed.py
```
```ipython
>>> CSVParser.read_csv("images")
>>> CSVParser.read_csv("biographies")
>>> CSVParser.read_csv("situationcards")
>>> CSVParser.read_csv("clinics")
```
(TODO: make this a shell script)


## Git Basics
## (an abridged guide to git for non-engineers)

### Most Used Commands

#### Starting a new development branch and switching between branches
`git checkout -b your_branch_name` -> creates a new development branch called `your_branch_name`
`git branch` -> to check what branch you are currently on
`git checkout other_branch_name` -> to switch from your current branch to another branch

#### View all changes on the active branch
`git status` -> will show all files changed
`git diff` -> will show specific lines changed

#### Add changes to a commit and include a message
`git add specific_files` or `git add .` (for all files) -> select files to include
`git commit -m 'your_message_in_here'` -> to include a helpful message with your commit

#### Pushing changes from your local development branch up to share with others/for review to merge in
`git push origin your_branch_name` -> pushes whatever changes you've saved locally in this branch to your remote tracking branch on GitHub with the same name
(Submit Pull Requests for other people to review, merge into `master` branch via GitHub site)

#### Updating a local branch to have the latest changes from the `master` branch
`git pull origin master` -> pulls all commits from master into the branch you are currently on

### Miscellaneous Commands (that you probably don't need)

#### Deleting an old local branch
`git branch -D your_branch_name` -> to delete old branches no longer in use (this isn't really necessary)

#### Rebasing
`git rebase -i HEAD~` -> an example of this command... rebasing can be used to clean up your git commit history, squash multiple commits together, skip select commits, reword your commit message, etc.
