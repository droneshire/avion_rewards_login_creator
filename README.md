# Avion Rewards Login Creator

[![Python application](https://github.com/droneshire/avion_rewards_login_creator/actions/workflows/python-app.yml/badge.svg)](https://github.com/droneshire/avion_rewards_login_creator/actions/workflows/python-app.yml)

Automatically Create Avion Rewards Logins

## Email Setup

If you want the bot to automatically parse the login codes from email addresses, you'll need to enable OATH on the master email account and on the backup email account:

(Pulled from [this tutorial](https://www.thepythoncode.com/article/use-gmail-api-in-python#Enabling_Gmail_API)

To use the Gmail API, we need a token to connect to Gmail's API. We can get one from the Google APIs' dashboard.

We first enable the Google mail API, head to the dashboard, and use the search bar to search for Gmail API, click on it, and then enable:

![image](https://github.com/droneshire/avion_rewards_login_creator/assets/2355438/331093bd-db53-4abd-9b33-54f4b31ef2e4)

Now, configure the Consent screen by clicking on OAuth Consent Screen if it is not already configured.

Make sure the app is in Testing mode, and add the email you will use to auth under the `Test users` section

We then create an OAuth 2.0 client ID by creating credentials (by heading to the Create Credentials button):

![image](https://github.com/droneshire/avion_rewards_login_creator/assets/2355438/c616dabe-662a-4259-953e-fc8b3b470433)

Click on Create Credentials, and then choose OAuth client ID from the dropdown menu:
![image](https://github.com/droneshire/avion_rewards_login_creator/assets/2355438/e9b28a32-783e-4a73-ab3e-9d741497deeb)

You'll be headed to this page:
![image](https://github.com/droneshire/avion_rewards_login_creator/assets/2355438/21655e85-bb64-42d7-9a97-008145401d3e)

Select Desktop App as the Application type and proceed. You'll see a window like this:
![image](https://github.com/droneshire/avion_rewards_login_creator/assets/2355438/013cc18e-885a-45f9-8b4b-76dab377d983)

Go ahead and click on DOWNLOAD JSON; it will download a long-named JSON file. Rename it to credentials.json and put it in the current directory of the project.

Alternatively, if you missed that window, you can click on that download icon button at the right of the page:
![image](https://github.com/droneshire/avion_rewards_login_creator/assets/2355438/d5161579-ba1a-475a-9e37-8da2e25db928)

Note: If this is the first time you use Google APIs, you may need to simply create an OAuth Consent screen and add your email as a testing user.

Save this credential file in the root directory (same place this `README` is located in).

Do this for both email accounts (e.g. as `google_credentials_main.json` and `google_credentials_backup.json`)

## Env File

Create a `.env` file in the root directory (same place this `README` is located in) with the following:

```
# Chrome Driver Configs
CHROME_DRIVER_PATHS_BROWSER="/usr/bin/google-chrome-stable"
CHROME_DRIVER_PATHS_DRIVER="/usr/local/bin/chromedriver"

# Google Email Credentials
GOOGLE_OATH_CREDENTIALS_FILE_MAIN="google_credentials_main.json"
GMAIL_MAIN_EMAIL="MAIN_EMAIL@gmail.com"
GOOGLE_OATH_CREDENTIALS_FILE_BACKUP="google_credentials_backup.json"
GMAIL_BACKUP_EMAIL="BACKUP_EMAIL@gmail.com"

AVION_REWARDS_EMAIL_ADDRESS="Avion Rewards <avionrewards@offers.rbc.com>"
AVION_REWARDS_EMAIL_SUBJECT="Avion Rewards Security Code"
AVION_REWARDS_EMAIL_REGEX=Your Avion Rewards security code is (\d{6})
```

## Installation

From the directory that this repo was cloned into:

**On Linux/Mac:**

```
make init
make install
source ./venv/bin/activate
```

**On Windows:**

```
python3 -m venv venv
pip3 install -r requirements.txt
source .\venv\bin\activate
```

## Running the Script

**On Linux/Mac:**

To manually input the login codes:

```
make create_account_manual email=foo@gmail.com backup_email=bar@gmail.com
```

To auto input the login codes (must provide the oauth credentials from `Email Setup` above)

```
make create_account_auto
```

**On Windows:**

To manually input the login codes:

```
PYTHONPATH=C:\Path\To\Repo\src python3 -m executables.create_account --manual-input --email foo@gmail.com --backup-email bar@gmail.com
```

To auto input the login codes (must provide the oauth credentials from `Email Setup` above)

```
PYTHONPATH=C:\Path\To\Repo\src python3 -m executables.create_account
```

## Landing Page

Starts here, the bot does the rest!

![image](https://github.com/droneshire/avion_rewards_login_creator/assets/2355438/2de61549-1836-422d-86fb-7eac7a34e087)

## Confirm Login Email

![image](https://github.com/droneshire/avion_rewards_login_creator/assets/2355438/7046abfb-8598-43dc-9c6a-fed07fa54782)
