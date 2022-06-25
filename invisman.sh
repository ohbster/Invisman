#!/bin/bash

if [ -z "$1" ]
then
	echo "-i	Fresh install"
	echo "-I	Initialize database"
	echo "-t	Enter testing mode"
	echo "-p	Enter production mode"
	echo "-D 	Delete the database"
	echo "-d	Drop database <argument>"
fi


database_file="invisman.db"

while getopts 'd:DiItp' OPTION; do
	case "$OPTION" in
		i)
			echo "**********initializing**********"
			echo "installing flask"
			python3 -m venv env
			source env/bin/activate
			pip install flask
			pip install sqlalchemy
			pip install requests
			pip install faker
			pip install multipledispatch
			
			#cat countries.sql | sqlite3 invisman.db
			python3 app.py
			

			;;
		I)
			echo "************ populating tables ************"
			export FLASK_APP=populate_tables.py
			python3 populate_tables.py
			;;
		t)
			source env/bin/activate
			echo "************ testing ************"			 
			export FLASK_APP=tester.py
			export FLASK_ENV=development
			flask run

			;;
		p)
			source env/bin/activate 
			echo "running production"
			export FLASK_APP=app.py
			flask run
			;;
			
		D)
			echo "dropping all tables"
			rm $database_file
			;;
		d)
			dvalue="$OPTARG"
			echo "dropping table $dvalue"
			sqlite3 $database_file "DROP TABLE $dvalue;"
			;;
		?)
			echo "script usage: $(basename \$0) [-d] [-D] [-i]" >&2
			exit 1
			;;
	esac
done
shift "$(($OPTIND -1))"