<h1 align="center">Company Logo Downloader and Uploader</h1>

<p align="justified">This script automates the process of searching for company logos using the Google Custom Search API, downloading them, and uploading them to Google Drive. It updates the status in a Google Sheet to indicate the progress.</p>

## Prerequisites

1. Python 3.x
2. Google Cloud Platform (GCP) project with Google Sheets and Google Drive APIs enabled.
3. Service account credentials JSON file for GCP.
4. Google Custom Search API key and Search Engine ID.

## Setup

### Google Cloud Platform

1. Create a GCP project.
2. Enable the Google Sheets API and Google Drive API.
3. Create a service account and download the credentials JSON file.
4. Share your Google Sheet and Google Drive folder with the service account email.

### Google Custom Search API

1. Enable the Google Custom Search API in your GCP project.
2. Create a Custom Search Engine and obtain the Search Engine ID.
3. Generate an API key for the Custom Search API.

#### Obtaining the Custom Search Engine ID

1. Go to the [Google Custom Search Engine](https://cse.google.com/cse/) page.
2. Click on "Add" to create a new search engine.
3. In the "Sites to Search" section, you can specify a domain (e.g., "example.com"). For broad searches, you can use "www.google.com".
4. Click on "Create" to create the search engine.
5. Once created, go to the "Control Panel" of your search engine.
6. Under the "Basics" tab, you will find the "Search engine ID". Copy this ID as you will need it in your script.

### Local Environment

1. Install required Python packages:
    ```bash
    pip install requests gspread oauth2client google-api-python-client
    ```

2. Ensure you have your service account credentials JSON file.

## Configuration

1. Update the following constants in the script:
    - `credentials_path`: Path to your service account key file.
    - `sheet_id`: ID of your Google Sheet.
    - `tab_name`: Name of the tab within your Google Sheet.
    - `drive_folder_id`: ID of your Google Drive folder where images will be uploaded.
    - `temp_dir`: Path to the directory where images will be downloaded temporarily.
    - `google_api_key`: Your Google Custom Search API key.
    - `search_engine_id`: Your Google Custom Search Engine ID.

## Script Overview

### Google Sheets and Drive Setup

- **Scopes**: Define the required API scopes.
- **Credentials**: Load the service account credentials.
- **Client**: Authorize the Google Sheets client and build the Drive service object.

### Functions

- **search_image(company_name)**: Search for the company logo using the Google Custom Search API.
- **download_image(url, company_name, ext='svg')**: Download the image from the provided URL.
- **upload_to_drive(file_path, company_name)**: Upload the image to Google Drive and return the shareable link.

### Main Script

- Open the Google Sheet and read all records.
- Ensure the temporary directory for logos exists.
- Process each row in the Google Sheet:
  - Skip rows with empty company names or already processed (status "Done").
  - Search for the company logo.
  - Download the logo if found.
  - Upload the logo to Google Drive.
  - Update the Google Sheet with the status and link to the uploaded logo.

## Running the Script

1. Ensure the necessary configurations are done.
2. Run the script:
    ```bash
    python script_name.py
    ```

## Warnings

1. Be cautious while using your Google API credentials in scripts.
2. Monitor the usage limits of the Google Custom Search API.
3. Ensure the service account has appropriate access to the Google Sheet and Drive folder.
