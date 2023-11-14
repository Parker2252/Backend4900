from django.contrib import admin
from .models import FoodItem, GuestRSVP, Catering, Event, Users
from django.contrib.auth.admin import UserAdmin

# class UsersAdmin(admin.ModelAdmin):
#     list_display = ('user_id', 'passwords')
#     list_filter = ('user_id',)
#     search_fields = ('user_id', 'rsvp_id')
#     ordering = ['user_id']


class GuestRSVPAdmin(admin.ModelAdmin):
    list_display = ('rsvp_id', 'email', 'first_name', 'last_name', 'food_choice')
    list_filter = ('food_choice',)
    search_fields = ('first_name', 'last_name')
    ordering = ['event_id']




class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)  # Make sure to use a tuple for single values
    search_fields = ('name',)


class CateringAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)  # Make sure to use a tuple for single values
    search_fields = ('name',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'event_date', 'number_of_guests', 'catering')
    list_filter = ('user', 'event_date')
    search_fields = ('event_name', 'user__username')


# class StockList(admin.ModelAdmin):
#     list_display = ('customer', 'symbol', 'name', 'shares', 'purchase_price')
#     list_filter = ('customer', 'symbol', 'name')
#     search_fields = ('customer', 'symbol', 'name')
#     ordering = ['customer']

admin.site.register(Users, UserAdmin)
# admin.site.register(GuestRSVP, GuestRSVPAdmin)
admin.site.register(FoodItem, FoodAdmin)
admin.site.register(Catering, CateringAdmin)
admin.site.register(Event, EventAdmin)
# admin.site.register(Testimonials, StockList)
