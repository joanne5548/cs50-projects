from django.contrib import admin

from .models import *

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class AuctionAdmin(admin.ModelAdmin):
    list_display = ("id", "title")

admin.site.register(User, UserAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid)
admin.site.register(Comment)