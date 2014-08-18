###############################
#                             #
# Admin Seite um Eintraege zu #
# loeschen, Daten anzupassen. #
#                             #
# Author: Gabor Tanz          #
# Changed: 13.08.2014         #
#                             #
###############################

from django.contrib import admin
from scom.models import *
# Register your models here.
admin.site.register(Server)
admin.site.register(Source)
admin.site.register(Alert)
admin.site.register(Status)
admin.site.register(Vorfall)
admin.site.register(Operator)
admin.site.register(Aktion)