from celery import shared_task
from datetime import datetime
from .models import *
from .utils.scraper import scrape, read_pdf  # Assuming scrape logic is refactored into a separate file
from .utils.predict import *

curr_month = datetime.now().month
curr_year = datetime.now().year

@shared_task
def scrape_task(user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        response = scrape(user.ke_num)
        if response.status_code == 501:
            response = scrape(user.ke_num)
        if response.status_code == 404:
            return {'status': 404, 'message': 'KE number not found'}
        if response.status_code == 200:
            units = read_pdf(user.ke_num)
            if units:
                # Store units in the database...
                for month, unit in units.items():
                    # separate month and year from 'jan-23'
                    month, year = month.split('-')
                    month = month.capitalize()
                    month = next((m[0] for m in MONTH_CHOICES if m[1] == month), None)
                    year = int(year) + 2000
                    # create a bill object only if the bill does not exist
                    if not Bill.objects.filter(user=user, month=month, year=year, is_predicted=False).exists():
                        bill = Bill.objects.create(user=user, month=month, year=year, units=unit, is_predicted=False)
                        bill.save()
                forcast, _ = store_predicted_units(user, is_scraper=True)   
                print("Forcast: ", forcast)
                return {'status': 200, 'message': 'Scraping successful'}
        return {'status': 500, 'message': 'Scraping failed'}
    except Exception as e:
        return {'status': 500, 'message': str(e)}

@shared_task
def scrape_all_task():
    users = CustomUser.objects.all()
    for user in users:
        if user.ke_num:
            scrape_task.delay(user.id)
    return {'status': 200, 'message': 'Scraping initiated for all users'}