from django.contrib import admin
from .models import FoodItem, FoodType, PersonInTeam, CustomUser, CartItem, Order


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'confirmed', 'confirm_id')
    list_filter = ('user', 'confirmed', 'confirm_id')
    search_fields = ('user', 'confirmed', 'confirm_id')


class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date_added', 'veg',
                    'is_available', 'food_item_type')
    list_editable = ('is_available',)
    list_filter = ('name', 'price', 'date_added')
    search_fields = ('name', 'price', 'date_added',
                     'veg', 'is_available', 'description')


class PersonInTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_address', 'date_added')
    list_filter = ('name', 'email_address', 'date_added')
    search_fields = ('name', 'email_address', 'date_added')


class FoodTypeAdmin(admin.ModelAdmin):
    list_display = ('long_name', 'short_name', 'date_added')
    list_filter = ('long_name', 'short_name', 'date_added')
    search_fields = ('long_name', 'short_name', 'date_added')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'qty', 'date_added')
    list_filter = ('user', 'item', 'qty', 'date_added')
    search_fields = ('user', 'item', 'qty', 'date_added')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'price', 'date_added', 'status', 'last_modified')
    list_filter = ('user', 'date_added', 'status')
    list_editable = ('status', )
    search_fields = ('user', 'date_added', 'status')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
admin.site.register(FoodType, FoodTypeAdmin)
admin.site.register(PersonInTeam, PersonInTeamAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
