import re
import logging
from datetime import datetime
import fitz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, UnexpectedAlertPresentException, NoAlertPresentException, NoSuchElementException
import os
import time

logging.basicConfig(filename='scraper.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to extract unit values from a specific section of the text
def extract_units_from_section(text):
    start_marker_match = re.search(r'\b(\d{4})\n(\d{4})\b', text)
    start_marker = start_marker_match.group() if start_marker_match else None
    end_marker_match = re.search(r'\b(\d{2})/(\d{2})\b', text)
    end_marker = end_marker_match.group() if end_marker_match else None
    if not end_marker: return
    logging.info(f"Start & End Markers Processed: {start_marker} - {end_marker}")
    # Find the start and end index of the relevant section
    start_index = text.find(start_marker) + len(start_marker)
    end_index = text.find(end_marker, start_index)
    # Extract the relevant text
    relevant_section = text[start_index:end_index]
    unit_values = re.findall(r'\b\d{1,5}\b', relevant_section) 
    return [int(value) for value in unit_values]

# Function to generate month names in reverse order starting from a given month and year
def generate_months_reversed(start_month, start_year, num_months):
    month_names = []
    current_month = datetime.strptime(f"{start_month}-{start_year}", "%b-%y")
    current_year = datetime.strptime(start_year, "%y").year
    for _ in range(num_months):
        month_names.insert(0, current_month.strftime("%b-%y"))
        if current_month.month == 1:
            current_month = current_month.replace(year=current_year - 1, month=12)
        else:
            current_month = current_month.replace(month=current_month.month - 1)
    return month_names

# Function to process a single PDF file
def process_single_pdf(pdf_file_path):
    try:
        doc = fitz.open(pdf_file_path)
        text = doc[0].get_text()
        units_sequence = extract_units_from_section(text)
        if units_sequence is None:
            logging.warning(f"No units found in {pdf_file_path}")
            return
        valid_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        start_index = 0
        while True:
            match = re.search(r'\b([A-Za-z]{3})-(\d{2})\b', text[start_index:])
            if match:
                if match.group(1) in valid_months:
                    bill_month_year = match
                    break
                start_index += match.end()
            else:
                logging.warning("No valid mmm-yy found in %s", pdf_file_path)
                break
        month = bill_month_year.group(1)
        year = bill_month_year.group(2)
        # if bill month is before jul 2023, then log a warning and return
        if int(year) < 23 or (int(year) == 23 and valid_months.index(month) < 6):
            logging.warning(f"Bill month is before Jul 2023 in {pdf_file_path}")
            return
        months_reversed = generate_months_reversed(month, year, 13)
        month_units_dict_reversed = dict(zip(months_reversed, units_sequence))
        logging.info("Processed %s - Units: %s", pdf_file_path, month_units_dict_reversed)
        return month_units_dict_reversed
    except Exception as e:
        logging.error("Error processing %s: %s", pdf_file_path, str(e))

def wait_for_download(directory):
    while True:
        if not len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.crdownload')]):
            break
        time.sleep(5)
        
def read_pdf():
    directory = os.path.join(os.getcwd(), "bills")
    units = {}
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            data = process_single_pdf(os.path.join(directory, file))
            units.update(data)
    print(units)
    # delete all files in the directory
    for file in os.listdir(directory):
        os.remove(os.path.join(directory, file))

def scrape(account_number):
    # Set up the web driver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("prefs", {
    "download.default_directory": os.path.join(os.getcwd(), "bills"),
})
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options)
    
    driver.get('https://staging.ke.com.pk:24555/ReBrand/DuplicateBill.aspx')
    driver.implicitly_wait(30)
    try:
        acc_input = driver.find_element(by=By.ID, value='txtAccNo')
        acc_input.clear()
        acc_input.send_keys(account_number)
        
        captcha = driver.find_element(by=By.ID, value='lblCaptcha')
        print("Captcha:", captcha.text)
        captcha_input = driver.find_element(by=By.ID, value='txtimgcode')
        captcha_input.clear()
        captcha_input.send_keys(captcha.text)
        
        view_bill_button = driver.find_element(By.ID, 'btnViewBill') # Replace with the correct ID
        if view_bill_button:
            print("View Bill Button Found")
        view_bill_button.click()
        
        first_entry_download_button_xpath = "(//input[@value='Download'])[1]"
        first_entry_download_button = driver.find_element(By.XPATH, first_entry_download_button_xpath)
        first_entry_download_button.click()

        last_entry_download_button_xpath = "(//input[@value='Download'])[last()]"
        last_entry_download_button = driver.find_element(By.XPATH, last_entry_download_button_xpath)
        last_entry_download_button.click()
    except NoSuchElementException:
        logging.error("Element not found")
        print("Element not found")
    except UnexpectedAlertPresentException:
        try:
            alert = driver.switch_to.alert
            alert.accept()
            logging.error("Account number not found")
        except NoAlertPresentException:
            logging.error("No alert present")
    except Exception as e:
        logging.error(str(e))
        print(str(e))
    
    wait_for_download(os.path.join(os.getcwd(), "bills"))
    
    driver.quit()
    
    