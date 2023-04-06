# openea
Enterprise-grade Enterprise Architecture tool based on ontology engine


![Default Home View](webapp/static/img/image_1_diagram.png?raw=true "Diagram view")

## Main features

* Web based enterprise architecture tool
* Ontology engine and research tool
* Tailored metamodel for your organisation
* Dynamic visualization
* Custom reports on knowledge base
* Model exchange
* Custom Plugin development

* SQLite by default if no env variable is set

### Matrix View
![Matrix View](webapp/static/img/image_2_matrix.png?raw=true "Diagram view")

# Usage

## Getting Started with project

First clone the repository from Github and switch to the new directory:

    $ git clone git@github.com/USERNAME/openea.git
    $ cd openea
    
Activate the virtualenv for your project.
    
Install project dependencies:

    $ pip install -r requirements.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver

And access the application at http://localhost:8000/

## Creating your organisation with admin rights

Register and create your organisation with your username as admin

    $ python manage.py create_organisation <organisation_name> --users <username>

## Navigating the interface

To display the repositories, click on your user at the top right, then on "Repositories".

Under the "Relations" tab, create at least the relation has the property
Under the "Concepts" tab, start by creating the concepts (boxes), Ex: fruit, color
under the "Ontology" tab, create the Concept-Relation-Concept links, Ex: fruits - has for property - color
You are ready to create the instances.

To create an instance:
Under the "Concepts" tab, select the concept of the instance you want to create
Then click on "New instance", fill in the form and save.

Click on the instance to view it.
You can edit the relationships between instances from the instance view page, Ex: apple - has property - red
You can view all instances under the "Instances" tab