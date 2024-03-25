import math
from ..models import *

def get_or_create_category_sub_category(category_name, sub_category_name=None):
    category, _ = Category.objects.get_or_create(name=category_name)
    sub_category = None
    if sub_category_name:
        sub_category, _ = SubCategory.objects.get_or_create(name=sub_category_name, category=category)
    return category, sub_category

def get_latest_usage(appliance=None, room=None):
    if room:
        return Usage.objects.filter(room=room).order_by('-predict_date').first()
    return Usage.objects.filter(appliance=appliance).order_by('-predict_date').first()

def calculate_total_units(appliances):
    return sum(get_latest_usage(appliance).units for appliance in appliances if get_latest_usage(appliance))

def update_appliance_data(appliance, data):
    appliance.alias = data.get('alias', appliance.alias)
    category_name = data.get('category', appliance.category.name)
    sub_category_name = data.get('sub_category')
    daily_usage = int(data.get('daily_usage'))
    category, sub_category = get_or_create_category_sub_category(category_name, sub_category_name)
    appliance.category = category
    appliance.sub_category = sub_category
    appliance.daily_usage = daily_usage
    appliance.save()
    return appliance

def calculate_and_save_usage(instance, units, is_room=False):
    if is_room:
        usage = Usage.objects.create(room=instance, units=units)
    else:
        usage = Usage.objects.create(appliance=instance, units=math.ceil(units * instance.wattage / 1000))
    usage.save()
    return usage