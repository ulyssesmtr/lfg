## Project setup

At the project root folder, run the following command:
```
docker-compose -f docker-compose-local.yml up -d --build
```

This will start all the service's containers, apply
database migrations, load initial data, create an admin user
and start the API server, meaning it is not necessary to do anything else
to mess with the project.


## Admin panel

The admin panel can be accessed at localhost:8000/admin/ by using the already created user
with the following credentials:
```
username: admin
password: admin
```
There are three admin models in the LFG_API section of the home page, as can be seen below:

![image](https://github.com/ulyssesmtr/lfg/assets/73036888/95498f21-fbc5-4a1c-acae-0343a39a68c3)


### API Approved Loans

This admin registered model is the Loan model with a modified queryset, made to show
only model instances that were approved by the third party API in order to facilitate
management during human approval.

![image](https://github.com/ulyssesmtr/lfg/assets/73036888/22d3dedc-6bef-418c-9e75-8541d476d645)

In this section, the admin can see all the API approved loans submissions and approve them if
necessary.


### All Submitted Loans

This admin registered model shows all the Loan model instances that were created, despite
if it was approved or not by the third party API.

![image](https://github.com/ulyssesmtr/lfg/assets/73036888/082ef7c6-626f-4feb-ba18-5ec482772a5a)


In both sections, the admin is not allowed to edit the "is_api_approved" field for obvious reasons.

### Loan fields

This section shows all the input fields that will be rendered in the interface (shown later).

![image](https://github.com/ulyssesmtr/lfg/assets/73036888/510e3913-683b-46a5-8ae2-33dcd23df73a)

At the project setup, a few fields are loaded by default, but the admin is free to delete,
edit and create new fields at will. When creating a field, it is possible to choose its
characteristics:

1. Type: Text, number, month, time and e-mail
2. Required or optional
3. The order it will apear in the interface
4. If its active or not (only active fields are taken into consideration in the interface and
data validation)

## Interface

The frontend interface can be accessed at localhost:3000

![image](https://github.com/ulyssesmtr/lfg/assets/73036888/cd96d6f1-8897-4164-981e-1ea05bd4c14f)


There might be a slight delay before the form fields can appear when loading the page just after the project setup
due to the fact that it takes a moment until all the migrations and fixtures are loaded
into the database. Refreshing the page after a few seconds should be enough.

In this page, only the Contact Name input is fixed, all the other inputs are created based on the
fields created by the admin and sent in the API response.

After correctly filling the form, a request is made to the API and a Loan model instance
should be created. It can be seen in the All Submitted Loans admin section.

To change the form fields, all it takes is to delete/create/edit the Loan fields instances
in the admin panel and refresh the interface page.

## API

There are only two endpoints

POST /api/v1/loan/
Creates the Loan instance in the database.

GET /api/v1/loanfield/
Returns all the loan fields 

Detailed docs can be accessed at localhost:8000/swagger/

## Tests

Tests for the views and serializers were written and can be found at
api/lfg_api/tests

In order to run them, execute the following commands

```
docker exec -it lfg_api_1 bash
python manage.py test
```
















