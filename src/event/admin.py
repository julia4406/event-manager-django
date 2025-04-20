from django.contrib import admin
from django.contrib.auth import get_user_model

from event import models


admin.site.register(models.Event)
