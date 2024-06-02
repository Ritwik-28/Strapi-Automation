import os
import getpass
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from PIL import Image

# Google Sheets and Drive API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Path to your service account key file

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

sheets_service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)

SPREADSHEET_ID = '1BfJ3G_tIjPllBQDvZ9SvdJDcbDDbWf5WbY8qOzPzG60'
SHEET_NAME = 'Picture Generation'
DRIVE_FOLDER_ID = '1QiJ5fsZfs2q8itr5bT6OgOWBYmTma7x0'
IMAGE_DOWNLOAD_PATH = 'downloaded_images' # Path to your folder on local machine

# Ensure the download directory exists
os.makedirs(IMAGE_DOWNLOAD_PATH, exist_ok=True)

# Selenium setup
chrome_options = Options()
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")  # Ensure the browser starts maximized for visibility
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_sheet_data():
    try:
        print("Fetching data from Google Sheets...")
        range_ = f"{SHEET_NAME}!A:D"  # Adjusted to get columns A to D only
        sheet = sheets_service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_).execute()
        values = result.get('values', [])
        print(f"Data fetched: {values}")
        return values
    except Exception as e:
        print(f"Error fetching data from Google Sheets: {e}")
        return []

def update_sheet_status(row_index, col, status):
    try:
        print(f"Updating sheet status at row {row_index + 1}, column {col} with status: {status}")
        body = {
            'values': [[status]]
        }
        range_ = f"{SHEET_NAME}!{col}{row_index + 1}"
        sheets_service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=range_,
            valueInputOption="RAW", body=body).execute()
        print("Sheet status updated")
    except Exception as e:
        print(f"Error updating Google Sheet: {e}")

def login_to_linkedin(driver, wait, username_str, password_str):
    try:
        print("Attempting to log in to LinkedIn...")
        driver.get("https://www.linkedin.com/login")
        username = wait.until(EC.visibility_of_element_located((By.ID, 'username')))
        password = wait.until(EC.visibility_of_element_located((By.ID, 'password')))
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@type="submit"]')))

        username.send_keys(username_str)
        password.send_keys(password_str)
        login_button.click()
        wait.until(EC.presence_of_element_located((By.ID, 'global-nav-search')))
        print("Logged in successfully")
    except Exception as e:
        print(f"Login elements not found or login failed: {e}")

def close_pop_up(driver, wait):
    try:
        pop_up_close_button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/section/button')))
        pop_up_close_button.click()
        print("Pop-up closed")
    except Exception as e:
        print(f"No pop-up appeared or pop-up elements not found: {e}")

def download_image(driver, wait, download_path):
    try:
        print("Attempting to download profile image...")
        img = wait.until(EC.presence_of_element_located((By.XPATH, '//img[contains(@class, "pv-top-card-profile-picture__image")]')))
        img_url = img.get_attribute('src')

        img_data = requests.get(img_url).content
        with open(download_path, 'wb') as handler:
            handler.write(img_data)

        print("Image downloaded successfully")
    except Exception as e:
        print(f"Image not found or failed to download: {e}")

def convert_image_to_webp(input_path, output_path):
    try:
        print(f"Converting image {input_path} to WebP format...")
        with Image.open(input_path) as img:
            img.save(output_path, 'webp')
        print("Image converted to WebP format")
    except Exception as e:
        print(f"Error converting image to WebP format: {e}")

def upload_image_to_drive(file_name, folder_id, file_path):
    try:
        print(f"Uploading image {file_name} to Google Drive...")
        file_metadata = {
            'name': file_name,
            'parents': [folder_id],
            'mimeType': 'image/webp'
        }
        media = MediaFileUpload(file_path, mimetype='image/webp')
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        file_id = file.get('id')
        web_view_link = file.get('webViewLink')

        # Make the file public
        drive_service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'},
            fields='id'
        ).execute()

        print(f"Image uploaded successfully, web view link: {web_view_link}")
        return web_view_link
    except Exception as e:
        print(f"Error uploading image to Google Drive: {e}")
        return None

def process_row(row_index, row, wait):
    if row_index == 0 or len(row) < 2 or (len(row) > 2 and row[2].strip().lower() == 'done'):
        print(f"Skipping row {row_index}")
        return

    name, linkedin_url = row[:2]  # Extract only first two elements
    print(f"Processing row {row_index + 1}: {linkedin_url}")

    try:
        # Open the LinkedIn profile
        print(f"Navigating to LinkedIn profile: {linkedin_url}")
        driver.get(linkedin_url)
        sleep(5)  # Wait for the URL to load
        print(f"Opened LinkedIn profile: {linkedin_url}")

        # Close pop-up if it appears
        close_pop_up(driver, wait)

        # Download the image
        png_image_path = os.path.join(IMAGE_DOWNLOAD_PATH, f'{name}_profile.png')
        download_image(driver, wait, png_image_path)

        # Convert the image to WebP format
        webp_image_path = os.path.join(IMAGE_DOWNLOAD_PATH, f'{name}_profile.webp')
        convert_image_to_webp(png_image_path, webp_image_path)

        # Upload the image to Google Drive
        image_name = f"{name} - Profile Picture.webp"
        web_view_link = upload_image_to_drive(image_name, DRIVE_FOLDER_ID, webp_image_path)

        if web_view_link:
            # Update Google Sheet with the link and status
            update_sheet_status(row_index, 'C', web_view_link)
            update_sheet_status(row_index, 'D', 'Done')

        # Clean up the downloaded images
        os.remove(png_image_path)
        os.remove(webp_image_path)

    except Exception as e:
        update_sheet_status(row_index, 'D', f"Error: {str(e)}")
        print(f"Error processing row {row_index + 1}: {e}")

def main():
    sheet_data = get_sheet_data()
    linkedin_username = input("Enter your LinkedIn username: ")
    linkedin_password = getpass.getpass("Enter your LinkedIn password: ")
    wait = WebDriverWait(driver, 20)

    if not sheet_data:
        print("No data found in Google Sheets.")
        return

    # Log in to LinkedIn once
    login_to_linkedin(driver, wait, linkedin_username, linkedin_password)

    for row_index, row in enumerate(sheet_data):
        process_row(row_index, row, wait)

if __name__ == "__main__":
    main()
    driver.quit()
