====
SCOM
====

SCOM ist eine einfache Django app um Fehlermeldungen & Warnungen von Microsoft
System Center Operations Manager (SCOM) zu verwalten. Zusätzlich ist eine 
einfache Server-Verwaltung vorhanden.

Quick start
-----------

1. Add "scom" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'scom',
    )

2. Include the scom URLconf in your project urls.py like this::

    url(r'^scom/', include('scom.urls')),

3. Run `python manage.py syncdb` to create the scom models.

4. Start the development server and visit http://127.0.0.1:8000/scom/ 
   to begin to add Operators, Sources, Alerts and Servers.