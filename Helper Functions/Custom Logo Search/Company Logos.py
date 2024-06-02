import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning from urllib3 needed for this script
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Path to credentials
credentials_path = 'credentials.json' # Path to the google service account credentials

# Google Sheets and Drive setup
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
client = gspread.authorize(creds)
service = build('drive', 'v3', credentials=creds)

# Google Sheets ID and tab name
sheet_id = '1BfJ3G_tIjPllBQDvZ9SvdJDcbDDbWf5WbY8qOzPzG60'
tab_name = 'Company Logos'
drive_folder_id = '1HzuSPWJE5esAaPVH8US6CifOmXRYXctV'

# Open the Google Sheet
sheet = client.open_by_key(sheet_id).worksheet(tab_name)
rows = sheet.get_all_records()

# Directory to save logos temporarily
temp_dir = "Logos" # Path to the directory on your local machine
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)

# Google Custom Search API setup
google_api_key = 'google_custom_search_API_Key'
search_engine_id = 'google_custom_search_engine_id'

def search_image(company_name):
    # Split the company name by commas and take the second part if available
    parts = company_name.split(',')
    if len(parts) > 1:
        primary_name = parts[1].strip()
    else:
        primary_name = parts[0].strip()
        
    search_url = f"https://www.googleapis.com/customsearch/v1?q={primary_name}+company+logo+filetype:svg&cx={search_engine_id}&key={google_api_key}&searchType=image"
    print(f"Searching for: {primary_name}")
    print(f"Search URL: {search_url}")
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json()
        print(f"Search results: {results}")
        if 'items' in results and len(results['items']) > 0:
            return results['items'][0]['link']
    else:
        print(f"Search failed with status code: {response.status_code}")
    return None

def download_image(url, company_name, ext='svg'):
    try:
        response = requests.get(url, verify=False)  # Disable SSL verification
        if response.status_code == 200:
            file_path = os.path.join(temp_dir, f"{company_name}.{ext}")
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded image for {company_name} to {file_path}")
            return file_path
        else:
            print(f"Failed to download image for {company_name}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image for {company_name}: {e}")
    return None

def upload_to_drive(file_path, company_name):
    try:
        file_metadata = {
            'name': f"{company_name}.svg",
            'parents': [drive_folder_id],
            'mimeType': 'image/svg+xml'
        }
        media = MediaFileUpload(file_path, mimetype='image/svg+xml')
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')
        service.permissions().create(
            fileId=file_id,
            body={'type': 'anyone', 'role': 'reader'}
        ).execute()
        link = f"https://drive.google.com/uc?id={file_id}"
        print(f"Uploaded image for {company_name} to {link}")
        return link
    except Exception as e:
        print(f"Error uploading image for {company_name}: {e}")
    return None

batch_size = 100
processed_count = 0

for i, row in enumerate(rows, start=2):
    print(f"Processing row {i}: {row}")
    company_name = row.get('Company Names', '').strip()
    status = row.get('Status', '').strip()

    if not company_name:
        print(f"Skipping row {i} due to empty Company name.")
        continue
    
    if status == 'Done':
        print(f"Skipping row {i} (Company: {company_name}, Status: {status})")
        continue
    
    print(f"Processing row {i}: Company: {company_name}")
    image_url = search_image(company_name)

    if image_url:
        print(f"Found image URL for {company_name}: {image_url}")
        logo_path = download_image(image_url, company_name)

        if logo_path:
            try:
                link = upload_to_drive(logo_path, company_name)
                if link:
                    sheet.update(f'B{i}', [[link]])
                    sheet.update(f'C{i}', [['Done']])
                else:
                    sheet.update(f'C{i}', [[f'Failed to upload']])
            except Exception as e:
                print(f"Error uploading image for {company_name}: {e}")
                sheet.update(f'C{i}', [[f'Failed: {str(e)}']])
            finally:
                os.remove(logo_path)
                print(f"Deleted temporary file for {company_name}: {logo_path}")
        else:
            print(f"Logo not found for {company_name}")
            sheet.update(f'C{i}', [['Logo Not Found']])
    else:
        print(f"Image URL not found for {company_name}")
        sheet.update(f'C{i}', [['Logo Not Found']])

    processed_count += 1
    if processed_count >= batch_size:
        break

print("Process completed.")
