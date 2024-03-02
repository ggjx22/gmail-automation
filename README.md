# Gmail Automation 

## Create a Google Cloud Project and Enable Google Mail API
1. go to https://cloud.google.com/
2. click on Console
3. In Console dashboard, select a project or create a new project
4. If creating new project, click on NEW PROJECT. Give your project a name and click on CREATE.
5. Go to the Nagivation menu and select APIs & Services, then Library.
6. At the search bar, search "Gmail API", click on it and select Enable.
7. Repeat step 6 and 7 for other Google APIs.

## Create an OAuth page
1. In your dashboard, go to the Nagivation Menu, API & Services, OAuth consent screen.
2. Select User Type as External for testing purposes, and click on Create.
3. Under App information, give your app a name and include an User support email (you can use your personal gmail address for that).
4. Skip the rest of the sections as we do not need them in our development.
5. Under Developer contact information, you can include your own gamil address. Click on Save and Continue.
6. Skip the whole section on Scopes and click on Save and Continue.
7. Under Test User, we skip that as well, click on Save and Continue.
8. Review the OAuth consent screen page.
9. Go back to the OAuth consent screen and click on Publish App.

## Create an OAuth2 Account
1. Go to Nagivation menu, API & Services, click on credentials.
2. Click on + create credentials.
3. Select OAuth Client ID
4. For Application type, select Desktop app.
5. Give your OAuth 2.0 client a name.
6. Click on create.
7. The OAuth client account is now created. Download the JSON file and save it in your project folder.
8. If the JSON file is lost, you can go back to the credentials page, under OAuth 2.0 Client IDs, click the download button under Actions to download tje JSON file again.

## Install Google API Python Client Library
1. Create a virtual environment for your project first and activate the virtual environment.
2. Pip install the following packages
    ```bash
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
    ```

## Connect to Google API services using Python