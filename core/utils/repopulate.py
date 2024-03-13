from .months import MONTH_CHOICES
from ..models import Bill, MonthlyAdjustment, Category, SubCategory, RoomTag

def add_category_subcategory():
    # Define your categories and subcategories
    categories_with_subcategories = {
        'Refrigerator': [
            ('Single Door', 150),
            ('Double Door', 500),
        ],
        'Iron': [
            ('Dry Iron', 200),
            ('Steam Iron', 50),
        ],
        'Air Conditioner': [
            ('Window AC', 1000),
            ('Split AC 1 Ton', 1200),
            ('Split AC 1.5 Ton', 1800),
            ('Split AC 2 Ton', 2000),
            ('Split Inverter AC 1 Ton', 900),
            ('Split Inverter AC 1.5 Ton', 1300),
            ('Split Inverter AC 2 Ton', 1500),
        ],
        'Deep Freezer': [
            ('Small', 150),
            ('Medium', 200),
            ('Large', 250),
        ],
        'Washing Machine': [
            ('Semi-Automatic', 300),
            ('Automatic', 500),
        ],
        'Television': [
            ('CRT', 150),
            ('LCD', 200),
            ('LED', 150),
            ('Plasma', 300),
        ],
        'Microwave Oven': [
            ('Solo', 800),
            ('Grill', 1000),
            ('Convection', 1200),
        ],
        'Water Dispenser': [
            ('Hot & Cold', 1500),
            ('Normal', 500),
        ],
        'Water Heater': [
            ('Instant', 3000),
            ('Storage', 2000),
        ],
    }

    for category_name, subcategories in categories_with_subcategories.items():
        category_obj, created = Category.objects.get_or_create(name=category_name)
        for subcategory_name, wattage in subcategories:
            SubCategory.objects.get_or_create(category=category_obj, name=subcategory_name, wattage=wattage)

def add_room_tags():
    # Define your room tags
    room_tags = [
        ('LR', 'Living Room'),
        ('BD', 'Bedroom'),
        ('KT', 'Kitchen'),
        ('DR', 'Dining Room'),
        ('ST', 'Study Room'),
        ('OT', 'Others'),
    ]

    for tag, description in room_tags:
        RoomTag.objects.get_or_create(tag=tag, description=description)
    
# create MonthlyAdjustments
def add_monthly_adjustments():
    for month, _ in MONTH_CHOICES:
        MonthlyAdjustment.objects.get_or_create(month=month)