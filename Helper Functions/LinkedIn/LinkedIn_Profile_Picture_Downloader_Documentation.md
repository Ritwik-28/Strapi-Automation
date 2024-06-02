
<h1 align="center">LinkedIn Profile Picture Downloader</h>

<p align="justified">This script automates the process of downloading LinkedIn profile pictures, converting them to WebP format, and uploading them to Google Drive. It also updates the status in a Google Sheet.</p>

## Prerequisites

1. Python 3.x
2. Google Cloud Platform (GCP) project with Google Sheets and Google Drive APIs enabled.
3. Service account credentials JSON file for GCP.
4. Chrome browser and ChromeDriver.

## Setup

### Google Cloud Platform

1. Create a GCP project.
2. Enable the Google Sheets API and Google Drive API.
3. Create a service account and download the credentials JSON file.
4. Share your Google Sheet and Google Drive folder with the service account email.

### Local Environment

1. Install required Python packages:
    ```bash
    pip install selenium requests google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client pillow webdriver-manager
    ```

2. Ensure you have Chrome installed. Download ChromeDriver and place it in your PATH.

#### Adding ChromeDriver to PATH

**Windows**

1. **Download ChromeDriver**:
   - Go to the [ChromeDriver download page](https://sites.google.com/a/chromium.org/chromedriver/downloads) and download the version that matches your Chrome browser.

2. **Extract ChromeDriver**:
   - Extract the downloaded file to a location of your choice, for example, `C:\chromedriver`.

3. **Add ChromeDriver to PATH**:
   - Open the Start Search, type in "env", and select "Edit the system environment variables".
   - In the System Properties window, click on the "Environment Variables" button.
   - In the Environment Variables window, under "System variables", find the "Path" variable, select it, and click "Edit".
   - In the Edit Environment Variable window, click "New" and add the path to the directory where you extracted ChromeDriver (`C:\chromedriver`).
   - Click OK on all the windows to close them.

**Linux**

1. **Download ChromeDriver**:
   - Go to the [ChromeDriver download page](https://sites.google.com/a/chromium.org/chromedriver/downloads) and download the version that matches your Chrome browser.

2. **Extract ChromeDriver**:
   - Extract the downloaded file and move it to `/usr/local/bin`. You can do this using the Terminal:
     ```bash
     mv ~/Downloads/chromedriver /usr/local/bin/chromedriver
     ```

3. **Make ChromeDriver executable**:
   - Ensure that ChromeDriver is executable:
     ```bash
     chmod +x /usr/local/bin/chromedriver
     ```

After adding ChromeDriver to your PATH, you can verify the installation by opening a terminal or command prompt and typing:
```bash
chromedriver --version
```
This should display the version of ChromeDriver you installed.

## Configuration

1. Update the following constants in the script:
    - `SERVICE_ACCOUNT_FILE`: Path to your service account key file.
    - `SPREADSHEET_ID`: ID of your Google Sheet.
    - `SHEET_NAME`: Name of the sheet within your Google Sheet.
    - `DRIVE_FOLDER_ID`: ID of your Google Drive folder where images will be uploaded.
    - `IMAGE_DOWNLOAD_PATH`: Path to the folder where images will be downloaded.

## Script Overview

### Google Sheets and Drive API Setup

- **Scopes**: Define the required API scopes.
- **Credentials**: Load the service account credentials.
- **Services**: Build the Google Sheets and Drive service objects.

### Selenium Setup

- Configure Chrome options and initialize the WebDriver.

### Functions

- **get_sheet_data()**: Fetch data from Google Sheets.
- **update_sheet_status(row_index, col, status)**: Update the status in the Google Sheet.
- **login_to_linkedin(driver, wait, username_str, password_str)**: Log in to LinkedIn.
- **close_pop_up(driver, wait)**: Close any pop-up that appears on LinkedIn.
- **download_image(driver, wait, download_path)**: Download the profile image.
- **convert_image_to_webp(input_path, output_path)**: Convert the image to WebP format.
- **upload_image_to_drive(file_name, folder_id, file_path)**: Upload the image to Google Drive.
- **process_row(row_index, row, wait)**: Process each row of the Google Sheet.

### Main Function

- Fetch sheet data.
- Prompt for LinkedIn credentials.
- Log in to LinkedIn.
- Process each row in the sheet.
- Quit the WebDriver.

## Running the Script

1. Ensure the necessary configurations are done.
2. Run the script:
    ```bash
    python3 LinkedIn Profile Picture.py
    ```

## Warnings

1. Never use your personal LinkedIn login credentials. Create a dummy account.
2. Post 100 entries the account might be flagged and suspended.
3. Ensure the service account has appropriate access to the Google Sheet and Drive folder.
