from django.contrib import admin
from django.contrib.auth import get_user_model

from event import models


User = get_user_model()

admin.site.register(models.Event)
admin.site.register(User)