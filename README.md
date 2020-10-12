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
	* step 4: Create a config.py file in dashboard/FlaskApp directory, take example_config.py as an example. Make sure the credentials in the file align with the MySQL database credentials.
	* step 5: Create a python3 virtual environment in the \dashboard\FlaskApp\FlaskApp directory.
	** step 5a: Install the virtualenv library in pip3, type in terminal: pip3 install virtualenv 
	** step 5b: Move to \dashboard\FlaskApp\FlaskApp, type in terminal: cd [PATH_TO\dashboard\FlaskApp\FlaskApp]
	** step 5c: Create the virtualenv, type in terminal: virtualenv venv.
	** step 5d: Install the required packages, type in terminal: pip3 install requirements.txt 
	* step 6: enter the virtual environment, this can differ based on the OS. Try: source venv/bin/activate
	* step 7: Type in terminal [WINDOWS]: set FLASK_APP = FlaskApp, Type in terminal [LINUX]: export FLASK_APP = FlaskApp
	* step 8: Type in terminal [WINDOWS]: set FLASK_ENV = production, Type in terminal [LINUX]: export FLASK_ENV = production
	* step 9: Run the Flask application using the FlaskApp folder in dashboard/FlaskApp as a module, type in terminal: flask run

Now paste the following in your browser: http://localhost:5005//.
Visit http:/104.248.92.134 to view the final result!
## Result snapshot