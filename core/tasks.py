from celery import shared_task
from .models import CustomUser, Bill
from .scraper import scrape, read_pdf  # Assuming scrape logic is refactored into a separate file

MONTH_CHOICES = [
    (1, 'Jan'),
    (2, 'Feb'),
    (3, 'Mar'),
    (4, 'Apr'),
    (5, 'May'),
    (6, 'Jun'),
    (7, 'Jul'),
    (8, 'Aug'),
    (9, 'Sep'),
    (10, 'Oct'),
    (11, 'Nov'),
    (12, 'Dec')
]

@shared_task
def scrape_task(user_id, account_number):
    user = CustomUser.objects.get(id=user_id)  # Make sure to import User
    response = scrape(account_number)
    # Assuming scrape is adjusted to return JSON or some other data structure instead of a Response object
    print('Task executed')
    if response.get('status') == 200:
        units = read_pdf()
        if units:
            # Store units in the database...
            # store the units in the database
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
            return {'status': 'success', 'message': 'Scraping successful'}
    return {'status': 'failure', 'message': 'Scraping failed'}
