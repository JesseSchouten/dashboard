# Description
THIS PROJECT IS A WORK IN PROGRESS.

This is a Flask template dashboard. Special thanks to traversy media (https://www.youtube.com/channel/UC29ju8bIPH5as8OGnQzwJyA) for the free tutorials (https://www.youtube.com/watch?v=zRwy8gtgJ1A). 

## Tools used:
   * Python
   * Flask
   * GitHub
   * HTML
   * CSS

## Prerequisites:
	* MySQL database instance
	* Python3 
	* Github

## Reproducing the results:
To get the dashboard to run locally:
	* step 1: Open the terminal.
	* step 2: Type the following in the terminal: git clone https://github.com/JesseSchouten/dashboard
	* step 3: Create the necassary database structure, this is given in:\dashboard\FlaskApp\FlaskApp\db\create_dashboard_database.sql
	* step 4: Make sure the credentials in C:\Users\Jesse\OneDrive\Documents\GitHub\dashboard\FlaskApp\FlaskApp\app.py from row 14 to 17 align with the MySQL database credentials.
	* step 5: Create a python3 virtual environment in the \dashboard\FlaskApp\FlaskApp directory.
	** step 5a: Install the virtualenv library in pip3, type in terminal: pip3 install virtualenv 
	** step 5b: Move to \dashboard\FlaskApp\FlaskApp, type in terminal: cd [PATH_TO\dashboard\FlaskApp\FlaskApp]
	** step 5c: Create the virtualenv, type in terminal: virtualenv venv.
	** step 5d: Install the required packages, type in terminal: pip3 install requirements.txt 
	* step 6: enter the virtual environment, this can differ based on the OS. Try: source venv/bin/activate
	* step 7: Run the Flask application in the \dashboard\FlaskApp\FlaskApp directory, type in terminal: python3 app.py

Now paste the following in your browser: http://localhost:5005//.

## Result snapshot