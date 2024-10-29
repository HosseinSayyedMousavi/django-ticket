# django-ticket
Ticket application for django project

## Repository

You can find the source code and contribute to the project at the following link:

[GitHub Repository](https://github.com/HosseinSayyedMousavi/django-ticket)

## Installation
### 1. install package
```
pip install django-ticket
```

### 2. add this application in settings.INSTALLED_APPS :
```
INSTALLED_APPS = [
    # ...
    'ticket',
    # ...
]
```
### 3. create and migrate migrations in BASE_DIR: 
    python manage.py migrate ticket

### 4. in core application include application urls:
```
from django.urls import path , include

urlpatterns += path("ticket/", include("ticket.urls"))
```

when you pass this missions you will see this in your admin panel:


![Screenshot from 2024-01-14 10-07-30](https://github.com/HosseinSayyedMousavi/django-ticket/assets/104124540/15d7ba19-c157-4cb0-a4a5-330101641b19)


## API Documentation:
You can create a Ticket from admin panel for a user to  admin.
Note that and you can do all this operations from admin to a user

### .../create_ticket/
Create a ticket from user to admin and add a new message:

method: ```post```

required keywords :  ```("title","section","priority","message")```

### .../add_message/
Add message to a ticket :

method: ```post```

required keywords : ```("ticket","message")```

Note: ticket means ticket's id

### .../close/
Close ticket.

method: ```patch```

required keywords : ```("ticket",)```

Note: ticket means ticket's id

### .../seen/
Change ticket to seen state from user

method: ```patch```

required keywords : ```("ticket",)```

Note: ticket means ticket's id

### .../get_my_tickets/
Get all tickets of user as a list

method: ```get```

required keywords : ```just must to be authorized.```


## A little more Professional
You can filter and have not seen tickets in admin panel:
### settings.py:

### 1. Add 'ticket/templates' to DIRS of TEMPLATES:
```
TEMPLATES = [
    {
            # ...
        'DIRS': ['ticket/templates'],
            # ...
    }
]
```

### 2.Add 'ticket.context_processors.get_pending_tickets' to context_processors OPTIONS:
```
TEMPLATES = [
    # ...
            "OPTIONS": {
            # ...
            "context_processors": [
                # ...
            'ticket.context_processors.get_pending_tickets'
                # ...
            ]
            # ...
    }
]
    # ...
```
Finally your application is complete to use:


![Screenshot from 2024-01-14 10-19-39](https://github.com/HosseinSayyedMousavi/django-ticket/assets/104124540/c68600d9-1e9f-4f5a-9a7a-8ba4644a8bec)

Thanks for attention
## Contributors

- [Abbas Ebadian](https://github.com/AbbasEbadian) - Founder of the project
- [Hossein Sayyedmousavi](https://github.com/HosseinSayyedMousavi) - Primary Developer and Contributorand Contributor


