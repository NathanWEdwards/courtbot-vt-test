# Courtbot-VT-test

A test repository for the [Courtbot-VT](https://github.com/codeforbtv/courtbot-vt) project,
a free service that will send you a text message reminder the day before your court hearing.

## Setup
This project uses [git-repo](https://gerrit.googlesource.com/git-repo) as part of the test workflow.

1. Install repo, initialize, and sync the project in a new directory:
```
# Install repo.
mkdir ~/.bin
PATH="~/.bin:${PATH}"
wget --https-only --secure-protocol=TLSv1_2 https://storage.googleapis.com/git-repo-downloads/repo -O ~/.bin/repo
chmod a+rx ~/.bin/repo

# Initialize and sync the project.
mkdir ~/courtbot-vt
cd ~/courtbot-vt
repo init -u "https://github.com/NathanWEdwards/courtbot-vt-project" -m default.xml
repo sync
```

2. In the courtbot-vt folder create a virtual environment and activate it:
```
python3 -m venv env
source env/bin/activate
```

3. Install packages inside the virtual environment:
```
pip install -r requirements.txt
```

4. Create an `.env` file to define config variables that will be used.

5. Open `.env` and populate the variables:
```
SFTP_HOST
SFTP_PORT
SFTP_USERNAME
SFTP_PRIVATE_KEY
MONGODB_URI
MONGO_COLLECTION
CLEAR_FTP_SERVER
