# django-query-debugger
Prints queries executed on you projects along with line traceback.

## Table of Contents
1. [Why Should I Use This?](#why-should-i-use-this?)
2. [When Should I NOT Use This?](#when-should-i-not-use-this)
3. [How To](#how-to)
4. [Features](#features)
5. [Usage](#usage)
    1. [Singleton module](#singleton-module)
    2. [On Django shell](#on-django-shell)
    3. [Traceback feature](#traceback-feature)

## Why Should I Use This?

Django ORM is great but ccan be a little obscure sometimes. Sometimes you want to know what queries your project is doing, some other times you see some weird looking querie running on your DB logs and have no ideia what triggered. This little lib helps with that.

## When Should I NOT Use This?

On your production environment. This guy is working fine but you dont need to insert this lame-hacking-failure-point into you production code, do you?


## How To

Just import this file. See the [Usage](#usage) section for more information

#### But remember:

Do not use it on production. I love this little hack but IT'S NOT NEEDED FOR PRODUCTION


## Features

- Print out EVERY query you make using django ORM or django.db.connection directly
- Print out EVERY query make by your, your framework or external libs
- Print out ONLY query trigged by a specific file
- Print usable strings for debug
- Traceback query execution to related files

# Usage:

### Singleton module:
- As Python's modules are singleton import this lib anywhere and it will affect the who project.

For example, when you hit a simple django view like this one:
```python
"""myproject/myapp/views.py"""
from django.http import Http404
from django.shortcuts import render
from myapp.models import MyModel
import query_debugger

def detail(request, my_model_id):
    try:
        p = MyModel.objects.get(pk=my_model_id)
    except MyModel.DoesNotExist:
        raise Http404("MyModel does not exist")
    return render(request, 'mymodel/detail.html', {'mymodel': p})
```

Your server output will look like this:
```
[12:03:23]myproject$ ./manage.py runserver
Performing system checks...
System check identified no issues (0 silenced).
May 15, 2019 - 11:03:31
Django version 2.1, using settings 'myproject.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
[11:03:38] INFO "GET /mymodel/1 HTTP/1.1" 200 38346
  /Users/fabio/projects/myproject/myapp/views.py Line: 7
    SELECT "myapp_mymodel"."id", "myapp_mymodel"."name" FROM "myapp_mymodel" WHERE "myapp_mymodel"."id" = 1
```

### On Django shell
```python
>>> import query_debugger
>>> from myapp.models import MyModel
>>> MyModel.objects.count()
/Users/fabio/envs/py36/lib/python3.6/site-packages/traitlets/config/application.py Line: 658
  /Users/fabio/envs/py36/lib/python3.6/site-packages/IPython/terminal/ipapp.py Line: 356
    /Users/fabio/envs/py36/lib/python3.6/site-packages/IPython/terminal/interactiveshell.py Line: 489
      /Users/fabio/envs/py36/lib/python3.6/site-packages/IPython/core/interactiveshell.py Line: 3291
        <ipython-input-3-0ccef3f04b0a> Line: 1
          /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/models/query.py Line: 383
            /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/models/sql/query.py Line: 483
              /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/models/sql/compiler.py Line: 1061
                /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/backends/utils.py Line: 100
                  SELECT COUNT(*) AS "__count" FROM "myapp_mymodel"
3
```

### Traceback feature
- The default behavior is to traceback only queries trigged by your code, ommiting queries trigged by the framework or libraries. However, if you want you can expand to any querie trigged anywhere like this:

```python
"""myproject/myapp/views.py"""
import query_debugger
query_debugger.everywhere()

...
```

Your server output will look like this:
```
[12:03:23]myproject$ ./manage.py runserver
Performing system checks...
System check identified no issues (0 silenced).
/Users/fabio/envs/py36/lib/python3.6/site-packages/django/utils/autoreload.py Line: 225
  /Users/fabio/envs/py36/lib/python3.6/site-packages/django/core/management/commands/runserver.py Line: 120
    /Users/fabio/envs/py36/lib/python3.6/site-packages/django/core/management/base.py Line: 442
      /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/migrations/executor.py Line: 18
        /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/migrations/loader.py Line: 209
          /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/migrations/recorder.py Line: 62
            /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/models/query.py Line: 138
              /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/models/sql/compiler.py Line: 1061
                /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/backends/utils.py Line: 100
                  SELECT "django_migrations"."app", "django_migrations"."name" FROM "django_migrations"
May 15, 2019 - 11:15:57
Django version 2.1, using settings 'thundera.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
[11:03:38] INFO "GET /mymodel/1 HTTP/1.1" 200 38346
  /Users/fabio/envs/py36/lib/python3.6/site-packages/django/contrib/auth/decorators.py Line: 20
    /Users/fabio/projects/myproject/myapp/views.py Line: 7
      /Users/fabio/envs/py36/lib/python3.6/site-packages/django/utils/functional.py Line: 347
        /Users/fabio/envs/py36/lib/python3.6/site-packages/django/contrib/auth/middleware.py Line: 12
          /Users/fabio/envs/py36/lib/python3.6/site-packages/django/contrib/auth/__init__.py Line: 189
            /Users/fabio/envs/py36/lib/python3.6/site-packages/django/contrib/auth/backends.py Line: 98
              /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/models/manager.py Line: 82
                /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/models/query.py Line: 54
                  /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/models/sql/compiler.py Line: 1061
                    /Users/fabio/envs/py36/lib/python3.6/site-packages/django/db/backends/utils.py Line: 100
                      SELECT "myapp_mymodel"."id", "myapp_mymodel"."name" FROM "myapp_mymodel" WHERE "myapp_mymodel"."id" = 1
```

Or narrow down to the file where you imported the debugger:
```python
"""myproject/myapp/views.py"""
import query_debugger
query_debugger.here()  # will only print queries trigged by myproject/myapp/views.py

...
```
