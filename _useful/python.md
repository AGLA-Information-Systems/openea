./manage.py dumpdata auth.user --indent 2 > user.json
./manage.py dumpdata auth.user --indent 2 --format xml > user.xml

# Export/Import
./manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude authorization --indent 2 > db.json
./manage.py loaddata db.json

./manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude authorization --indent 2 --format xml > currentdb.xml
./manage.py loaddata currentdb.xml

./manage.py dumpdata ontology --indent 2 --format xml > ontology.20230922.xml
./manage.py loaddata ontology.20230922.xml