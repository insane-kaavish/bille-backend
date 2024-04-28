from .months import MONTH_CHOICES
from ..models import Bill, MonthlyAdjustment, Category, SubCategory, RoomTag, Tip, TipCategory

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
 

# create tips
def add_tips():
    tips = {
        'Inverter Air Conditioner': {
            'title': 'Inverter Air Conditioner',
            'content': 'Inverter air conditioners can save up to 50% of your annual electricity consumption compared to conventional AC units.\n\nEnergy-saving tip:\nTo save energy, set your AC thermostat to 26°C and regularly clean and replace its filters.'
        },
        'LED Lighting': {
            'title': 'LED Lighting',
            'content': 'LED lights can save up to 75% of your annual energy consumption and last up to 25 times longer than incandescent lights.\n\nEnergy-saving tip:\nTo conserve energy more efficiently, install smart home technology and draw your curtains during the day to utilize sunlight.'
        },
        'Heat Rejection and Insulation Sheets': {
            'title': 'Heat Rejection and Insulation Sheets',
            'content': 'Heat rejection and insulation sheets can reduce up to 78% of the sun\'s heat from entering your home, thereby reducing cooling costs.\n\nEnergy-saving tip:\nKeep your home cool and create a comfortable space for your family by installing heat rejection and insulation sheets.'
        },
        'Energy-Intensive Appliances': {
            'title': 'Energy-Intensive Appliances',
            'content': 'Old energy-intensive appliances cost an average homeowner up to 45% on their annual consumption.\n\nEnergy-saving tip:\nWhen buying appliances, look for the Energy Star label that identifies products in terms of energy efficiency. Make the smart switch to energy-efficient appliances. If you are using energy-intensive appliances, use them during off-peak hours (10 pm to 6 am) to reduce your consumption load.'
        },
        'Energy Efficient UPS': {
            'title': 'Energy Efficient UPS',
            'content': 'Energy-efficient UPS can reduce your annual energy loss by up to 55%.\n\nEnergy-saving tip:\nWhen buying a UPS, look for the Energy Star label that identifies products by their efficiency. Servicing equipment regularly ensures optimal efficiency.'
        },
        'Phantom Energy Consumption': {
            'title': 'Phantom Energy Consumption',
            'content': 'Phantom energy, which is unconsumed or wasted energy, contributes up to 10% of your annual electricity bill.\n\nEnergy-saving tip:\nIt is best to unplug electronic devices and kitchen appliances when not in use to save energy.'
        },
        'Smart Home Technology': {
            'title': 'Smart Home Technology',
            'content': 'Smart home technology can save up to 23% of your annual electricity consumption.\n\nEnergy-saving tip:\nTo save energy, use smart home technology to automate your home appliances and lighting. This will help you to monitor and control your energy consumption.'
        },
        'Solar Panels': {
            'title': 'Solar Panels',
            'content': 'Solar panels can save up to 100% of your annual electricity consumption and reduce your carbon footprint.\n\nEnergy-saving tip:\nTo save energy, install solar panels on your rooftop to generate your own electricity. This will help you to reduce your electricity bill and save money.'
        },
        'Energy-Efficient Refrigerator': {
            'title': 'Energy-Efficient Refrigerator',
            'content': 'Energy-efficient refrigerators can save up to 40% of your annual electricity consumption compared to conventional refrigerators.\n\nEnergy-saving tip:\nTo save energy, set your refrigerator temperature to 4°C and your freezer temperature to -18°C. Regularly defrost your refrigerator and keep it away from heat sources.'
        },
        'Energy-Efficient Iron': {
            'title': 'Energy-Efficient Iron',
            'content': 'Energy-efficient irons can save up to 30% of your annual electricity consumption compared to conventional irons.\n\nEnergy-saving tip:\nTo save energy, iron your clothes in bulk and use the iron at a lower temperature.'
        },
        'Energy-Efficient AC': {
            'title': 'Energy-Efficient AC',
            'content': 'Energy-efficient air conditioners can save up to 40% of your annual electricity consumption compared to conventional AC units.\n\nEnergy-saving tip:\nTo save energy, set your AC thermostat to 26°C and regularly clean and replace its filters.'
        },
        'Energy-Efficient Deep Freezer': {
            'title': 'Energy-Efficient Deep Freezer',
            'content': 'Energy-efficient deep freezers can save up to 30% of your annual electricity consumption compared to conventional deep freezers.\n\nEnergy-saving tip:\nTo save energy, defrost your deep freezer regularly and keep it away from heat sources.'
        },
        'Energy-Efficient Washing Machine': {
            'title': 'Energy-Efficient Washing Machine',
            'content': 'Energy-efficient washing machines can save up to 25% of your annual electricity consumption compared to conventional washing machines.\n\nEnergy-saving tip:\nTo save energy, wash your clothes in bulk and use cold water to rinse your clothes.'
        },
        'Energy-Efficient Television': {
            'title': 'Energy-Efficient Television',
            'content': 'Energy-efficient televisions can save up to 20% of your annual electricity consumption compared to conventional televisions.\n\nEnergy-saving tip:\nTo save energy, turn off your television when not in use and use the sleep timer feature.'
        },
        'Energy-Efficient Microwave Oven': {
            'title': 'Energy-Efficient Microwave Oven',
            'content': 'Energy-efficient microwave ovens can save up to 15% of your annual electricity consumption compared to conventional microwave ovens.\n\nEnergy-saving tip:\nTo save energy, use your microwave oven to reheat food and cook small meals.'
        },
        'Energy-Efficient Water Dispenser': {
            'title': 'Energy-Efficient Water Dispenser',
            'content': 'Energy-efficient water dispensers can save up to 10% of your annual electricity consumption compared to conventional water dispensers.\n\nEnergy-saving tip:\nTo save energy, use your water dispenser to dispense water at room temperature.'
        },
        'Energy-Efficient Water Heater': {
            'title': 'Energy-Efficient Water Heater',
            'content': 'Energy-efficient water heaters can save up to 5% of your annual electricity consumption compared to conventional water heaters.\n\nEnergy-saving tip:\nTo save energy, use your water heater to heat water only when needed.'
        },
        'Energy Star Refrigerator': {
            'title': 'Energy Star Refrigerator',
            'content': 'Energy Star refrigerators can save up to 40% of your annual electricity consumption compared to conventional refrigerators.\n\nEnergy-saving tip:\nTo save energy, set your refrigerator temperature to 4°C and your freezer temperature to -18°C. Regularly defrost your refrigerator and keep it away from heat sources.'
        },
        'Energy Star Iron': {
            'title': 'Energy Star Iron',
            'content': 'Energy Star irons can save up to 30% of your annual electricity consumption compared to conventional irons.\n\nEnergy-saving tip:\nTo save energy, iron your clothes in bulk and use the iron at a lower temperature.'
        },
        'Energy Star AC': {
            'title': 'Energy Star AC',
            'content': 'Energy Star air conditioners can save up to 40% of your annual electricity consumption compared to conventional AC units.\n\nEnergy-saving tip:\nTo save energy, set your AC thermostat to 26°C and regularly clean and replace its filters.'
        },
        'Energy Star Deep Freezer': {
            'title': 'Energy Star Deep Freezer',
            'content': 'Energy Star deep freezers can save up to 30% of your annual electricity consumption compared to conventional deep freezers.\n\nEnergy-saving tip:\nTo save energy, defrost your deep freezer regularly and keep it away from heat sources.'
        },
        'Energy Star Washing Machine': {
            'title': 'Energy Star Washing Machine',
            'content': 'Energy Star washing machines can save up to 25% of your annual electricity consumption compared to conventional washing machines.\n\nEnergy-saving tip:\nTo save energy, wash your clothes in bulk and use cold water to rinse your clothes.'
        },
        'Energy Star Television': {
            'title': 'Energy Star Television',
            'content': 'Energy Star televisions can save up to 20% of your annual electricity consumption compared to conventional televisions.\n\nEnergy-saving tip:\nTo save energy, turn off your television when not in use and use the sleep timer feature.'
        },
        'Energy Star Microwave Oven': {
            'title': 'Energy Star Microwave Oven',
            'content': 'Energy Star microwave ovens can save up to 15% of your annual electricity consumption compared to conventional microwave ovens.\n\nEnergy-saving tip:\nTo save energy, use your microwave oven to reheat food and cook small meals.'
        },
        'Energy Star Water Dispenser': {
            'title': 'Energy Star Water Dispenser',
            'content': 'Energy Star water dispensers can save up to 10% of your annual electricity consumption compared to conventional water dispensers.\n\nEnergy-saving tip:\nTo save energy, use your water dispenser to dispense water at room temperature.'
        },
        'Energy Star Water Heater': {
            'title': 'Energy Star Water Heater',
            'content': 'Energy Star water heaters can save up to 5% of your annual electricity consumption compared to conventional water heaters.\n\nEnergy-saving tip:\nTo save energy, use your water heater to heat water only when needed.'
        },
        'Smart Refrigerator': {
            'title': 'Smart Refrigerator',
            'content': 'Smart refrigerators can save up to 40% of your annual electricity consumption compared to conventional refrigerators.\n\nEnergy-saving tip:\nTo save energy, set your refrigerator temperature to 4°C and your freezer temperature to -18°C. Regularly defrost your refrigerator and keep it away from heat sources.'
        },
        'Smart Iron': {
            'title': 'Smart Iron',
            'content': 'Smart irons can save up to 30% of your annual electricity consumption compared to conventional irons.\n\nEnergy-saving tip:\nTo save energy, iron your clothes in bulk and use the iron at a lower temperature.'
        },
        'Smart AC': {
            'title': 'Smart AC',
            'content': 'Smart air conditioners can save up to 40% of your annual electricity consumption compared to conventional AC units.\n\nEnergy-saving tip:\nTo save energy, set your AC thermostat to 26°C and regularly clean and replace its filters.'
        },
        'Smart Deep Freezer': {
            'title': 'Smart Deep Freezer',
            'content': 'Smart deep freezers can save up to 30% of your annual electricity consumption compared to conventional deep freezers.\n\nEnergy-saving tip:\nTo save energy, defrost your deep freezer regularly and keep it away from heat sources.'
        },
        'Smart Washing Machine': {
            'title': 'Smart Washing Machine',
            'content': 'Smart washing machines can save up to 25% of your annual electricity consumption compared to conventional washing machines.\n\nEnergy-saving tip:\nTo save energy, wash your clothes in bulk and use cold water to rinse your clothes.'
        },
        'Smart Television': {
            'title': 'Smart Television',
            'content': 'Smart televisions can save up to 20% of your annual electricity consumption compared to conventional televisions.\n\nEnergy-saving tip:\nTo save energy, turn off your television when not in use and use the sleep timer feature.'
        },
        'Smart Microwave Oven': {
            'title': 'Smart Microwave Oven',
            'content': 'Smart microwave ovens can save up to 15% of your annual electricity consumption compared to conventional microwave ovens.\n\nEnergy-saving tip:\nTo save energy, use your microwave oven to reheat food and cook small meals.'
        },
        'Smart Water Dispenser': {
            'title': 'Smart Water Dispenser',
            'content': 'Smart water dispensers can save up to 10% of your annual electricity consumption compared to conventional water dispensers.\n\nEnergy-saving tip:\nTo save energy, use your water dispenser to dispense water at room temperature.'
        },
        'Smart Water Heater': {
            'title': 'Smart Water Heater',
            'content': 'Smart water heaters can save up to 5% of your annual electricity consumption compared to conventional water heaters.\n\nEnergy-saving tip:\nTo save energy, use your water heater to heat water only when needed.'
        },
        'Inverter Refrigerator': {
            'title': 'Inverter Refrigerator',
            'content': 'Inverter refrigerators can save up to 40% of your annual electricity consumption compared to conventional refrigerators.\n\nEnergy-saving tip:\nTo save energy, set your refrigerator temperature to 4°C and your freezer temperature to -18°C. Regularly defrost your refrigerator and keep it away from heat sources.'
        },
        'Inverter Iron': {
            'title': 'Inverter Iron',
            'content': 'Inverter irons can save up to 30% of your annual electricity consumption compared to conventional irons.\n\nEnergy-saving tip:\nTo save energy, iron your clothes in bulk and use the iron at a lower temperature.'
        },
        'Inverter AC': {
            'title': 'Inverter AC',
            'content': 'Inverter air conditioners can save up to 40% of your annual electricity consumption compared to conventional AC units.\n\nEnergy-saving tip:\nTo save energy, set your AC thermostat to 26°C and regularly clean and replace its filters.'
        },
        'Inverter Deep Freezer': {
            'title': 'Inverter Deep Freezer',
            'content': 'Inverter deep freezers can save up to 30% of your annual electricity consumption compared to conventional deep freezers.\n\nEnergy-saving tip:\nTo save energy, defrost your deep freezer regularly and keep it away from heat sources.'
        },
        'Inverter Washing Machine': {
            'title': 'Inverter Washing Machine',
            'content': 'Inverter washing machines can save up to 25% of your annual electricity consumption compared to conventional washing machines.\n\nEnergy-saving tip:\nTo save energy, wash your clothes in bulk and use cold water to rinse your clothes.'
        },
        'Inverter Television': {
            'title': 'Inverter Television',
            'content': 'Inverter televisions can save up to 20% of your annual electricity consumption compared to conventional televisions.\n\nEnergy-saving tip:\nTo save energy, turn off your television when not in use and use the sleep timer feature.'
        },
        'Inverter Microwave Oven': {
            'title': 'Inverter Microwave Oven',
            'content': 'Inverter microwave ovens can save up to 15% of your annual electricity consumption compared to conventional microwave ovens.\n\nEnergy-saving tip:\nTo save energy, use your microwave oven to reheat food and cook small meals.'
        },
        'Inverter Water Dispenser': {
            'title': 'Inverter Water Dispenser',
            'content': 'Inverter water dispensers can save up to 10% of your annual electricity consumption compared to conventional water dispensers.\n\nEnergy-saving tip:\nTo save energy, use your water dispenser to dispense water at room temperature.'
        },
        'Inverter Water Heater': {
            'title': 'Inverter Water Heater',
            'content': 'Inverter water heaters can save up to 5% of your annual electricity consumption compared to conventional water heaters.\n\nEnergy-saving tip:\nTo save energy, use your water heater to heat water only when needed.'
        },
    }
    
    for tip_title, tip_data in tips.items():
        tip, created = Tip.objects.get_or_create(title=tip_title, content=tip_data['content'])
        if created:
            tip.save()
            
def add_tips_categories():
    # Define your tips categories
    tips_categories = {
        'Refrigerator': {
            'sub_category': [{
                'Single Door': [
                    'Inverter Refrigerator',
                    'Energy-Efficient Refrigerator',
                    'Energy Star Refrigerator',
                    'Smart Refrigerator'
                ]},
                {'Double Door': [
                    'Inverter Refrigerator',
                    'Energy-Efficient Refrigerator',
                    'Energy Star Refrigerator',
                    'Smart Refrigerator'
                ]}
            ]
        },
        'Iron': {
            'sub_category': [
                {
                    'Dry Iron': [
                        'Inverter Iron',
                        'Energy-Efficient Iron',
                        'Energy Star Iron',
                        'Smart Iron'
                    ]
                },
                {
                    'Steam Iron': [
                        'Inverter Iron',
                        'Energy-Efficient Iron',
                        'Energy Star Iron',
                        'Smart Iron'
                    ]
                }
            ]
        },
        'Air Conditioner': {
            'sub_category': [
                {
                    'Window AC': [
                        'Inverter AC',
                        'Energy-Efficient AC',
                        'Energy Star AC',
                        'Smart AC'
                    ]
                },
                {
                    'Split AC 1 Ton': [
                        'Inverter AC',
                        'Energy-Efficient AC',
                        'Energy Star AC',
                        'Smart AC'
                    ]
                },
                {
                    'Split AC 1.5 Ton': [
                        'Inverter AC',
                        'Energy-Efficient AC',
                        'Energy Star AC',
                        'Smart AC'
                    ]
                },
                {
                    'Split AC 2 Ton': [
                        'Inverter AC',
                        'Energy-Efficient AC',
                        'Energy Star AC',
                        'Smart AC'
                    ]
                },
                {
                    'Split Inverter AC 1 Ton': [
                        'Inverter AC',
                        'Energy-Efficient AC',
                        'Energy Star AC',
                        'Smart AC'
                    ]
                },
                {
                    'Split Inverter AC 1.5 Ton': [
                        'Inverter AC',
                        'Energy-Efficient AC',
                        'Energy Star AC',
                        'Smart AC'
                    ]
                },
                {
                    'Split Inverter AC 2 Ton': [
                        'Inverter AC',
                        'Energy-Efficient AC',
                        'Energy Star AC',
                        'Smart AC'
                    ]
                }
            ]
        },
        'Deep Freezer': {
            'sub_category': [
                {
                    'Small': [
                        'Inverter Deep Freezer',
                        'Energy-Efficient Deep Freezer',
                        'Energy Star Deep Freezer',
                        'Smart Deep Freezer'
                    ]
                },
                {
                    'Medium': [
                        'Inverter Deep Freezer',
                        'Energy-Efficient Deep Freezer',
                        'Energy Star Deep Freezer',
                        'Smart Deep Freezer'
                    ]
                },
                {
                    'Large': [
                        'Inverter Deep Freezer',
                        'Energy-Efficient Deep Freezer',
                        'Energy Star Deep Freezer',
                        'Smart Deep Freezer'
                    ]
                }
            ]
        },
        'Washing Machine': {
            'sub_category': [
                {
                    'Semi-Automatic': [
                        'Inverter Washing Machine',
                        'Energy-Efficient Washing Machine',
                        'Energy Star Washing Machine',
                        'Smart Washing Machine'
                    ]
                },
                {
                    'Automatic': [
                        'Inverter Washing Machine',
                        'Energy-Efficient Washing Machine',
                        'Energy Star Washing Machine',
                        'Smart Washing Machine'
                    ]
                }
            ]
        },
        'Television': {
            'sub_category': [
                {
                    'CRT': [
                        'Inverter Television',
                        'Energy-Efficient Television',
                        'Energy Star Television',
                        'Smart Television'
                    ]
                },
                {
                    'LCD': [
                        'Inverter Television',
                        'Energy-Efficient Television',
                        'Energy Star Television',
                        'Smart Television'
                    ]
                },
                {
                    'LED': [
                        'Inverter Television',
                        'Energy-Efficient Television',
                        'Energy Star Television',
                        'Smart Television'
                    ]
                },
                {
                    'Plasma': [
                        'Inverter Television',
                        'Energy-Efficient Television',
                        'Energy Star Television',
                        'Smart Television'
                    ]
                }
            ]
        },
        'Microwave Oven': {
            'sub_category': [
                {
                    'Solo': [
                        'Inverter Microwave Oven',
                        'Energy-Efficient Microwave Oven',
                        'Energy Star Microwave Oven',
                        'Smart Microwave Oven'
                    ]
                },
                {
                    'Grill': [
                        'Inverter Microwave Oven',
                        'Energy-Efficient Microwave Oven',
                        'Energy Star Microwave Oven',
                        'Smart Microwave Oven'
                    ]
                },
                {
                    'Convection': [
                        'Inverter Microwave Oven',
                        'Energy-Efficient Microwave Oven',
                        'Energy Star Microwave Oven',
                        'Smart Microwave Oven'
                    ]
                }
            ]
        },
        'Water Dispenser': {
            'sub_category': [
                {
                    'Hot & Cold': [
                        'Inverter Water Dispenser',
                        'Energy-Efficient Water Dispenser',
                        'Energy Star Water Dispenser',
                        'Smart Water Dispenser'
                    ]
                },
                {
                    'Normal': [
                        'Inverter Water Dispenser',
                        'Energy-Efficient Water Dispenser',
                        'Energy Star Water Dispenser',
                        'Smart Water Dispenser'
                    ]
                }
            ]
        },
        'Water Heater': {
            'sub_category': [
                {
                    'Instant': [
                        'Inverter Water Heater',
                        'Energy-Efficient Water Heater',
                        'Energy Star Water Heater',
                        'Smart Water Heater'
                    ]
                },
                {
                    'Storage': [
                        'Inverter Water Heater',
                        'Energy-Efficient Water Heater',
                        'Energy Star Water Heater',
                        'Smart Water Heater'
                    ]
                }
            ]
        }
    }
    
    for category_name, category_data in tips_categories.items():
        category_obj = Category.objects.get(name=category_name)
        for subcategory_data in category_data['sub_category']:
            for subcategory_name, tips in subcategory_data.items():
                subcategory_obj = SubCategory.objects.get(name=subcategory_name)
                for tip_title in tips:
                    print('category: ', category_obj.name, 'subcategory: ', subcategory_obj.name, 'tip: ', tip_title)
                    tip = Tip.objects.get(title=tip_title)
                    TipCategory.objects.get_or_create(tip=tip, category=category_obj, sub_category=subcategory_obj)
                    