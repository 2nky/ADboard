from django.contrib import admin

from adverts.models import AdvertType, Advert, Reply

admin.site.register(AdvertType)
admin.site.register(Advert)
admin.site.register(Reply)
