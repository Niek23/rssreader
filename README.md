# rssreader

## About
RSS Reader provides the possibility blity to subscribe for various feeds, mark articles and filter them via API.

## Getting Started
### Prerequisites
#### Docker
The recommended method to run the project is using by using Docker. Make sure [Docker](https://www.docker.com/products/docker-desktop) is installed and running on your machine.
1. Run ```mv rssreader/.env.example.docker rssreader/.env``` to rename the file with environment variables needed to start the app. Open with any text editor and fill in all fields (no space after =).
2. Run the following command: ```docker-compose up```. It will create and start all necessary containers for running the application. 


#### Locally
Make sure you have you have Python 3.6+ installed on your machine. ```mv rssreader/.env.example.local rssreader/.env```
1. Follow the 1st step from the Docker setup and get .env file ready.
2. Run ```pip install -r requirements.txt``` to install python packages for the app. Don't forget to set up python virtual environment.  
3. Run migrations by ```python manage.py migrate```
4. To create superuser use the following command ```python manage.py createsuperuser```. It will be necessary to log in before accessing any resource. 
5. Use ```python manage createfeed http://www.nu.nl/rss/Algemeen``` to load some feeds. Use a valid RSS source. 
6. And finally you can start the project by running ```python manage.py runserver```

**Keep in mind auto-updating functionality is not working when run locally**


### Usage
Go to ```http://127.0.0.1:8000``` in your browser to the app running. The first page gives the OpenAPI overview of all routes. Use ```?read=true/false``` to filter  read/unread articles.

## Testing
Pytest is used for all project tests. Run ```pytest``` within the project directory to start all tests. Provide directory or specific file after the command to choose which tests to run.
