from django.contrib import admin
from .models import FoodItemModel, FoodTypeModel, TeamModel, CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    pass
    # list_display = ('phone_number', 'short_name', 'date_added')
    # list_filter = ('long_name', 'short_name', 'date_added')
    # search_fields = ('long_name', 'short_name', 'date_added')


class FoodItemModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'date_added', 'veg',
                    'is_available', 'food_item_type')
    list_editable = ('is_available',)
    list_filter = ('name', 'price', 'date_added')
    search_fields = ('name', 'price', 'date_added',
                     'veg', 'is_available', 'description')


class TeamModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_address', 'date_added')
    list_filter = ('name', 'email_address', 'date_added')
    search_fields = ('name', 'email_address', 'date_added')


class FoodTypeModelAdmin(admin.ModelAdmin):
    list_display = ('long_name', 'short_name', 'date_added')
    list_filter = ('long_name', 'short_name', 'date_added')
    search_fields = ('long_name', 'short_name', 'date_added')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(FoodItemModel, FoodItemModelAdmin)
admin.site.register(FoodTypeModel, FoodTypeModelAdmin)
admin.site.register(TeamModel, TeamModelAdmin)
