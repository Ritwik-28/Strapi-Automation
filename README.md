
<h1 align="center">Strapi Data Upload Script</h1>

<p align="justified">This script uploads data from a Google Sheet to Strapi. The script includes functionality for handling image uploads from Google Drive and various conditional data fields. Below are the details for the setup, Google Sheet structure, and how the script works.</p>

## Setup

1. **Google Sheet Preparation**
   - Create a Google Sheet with the name `Strapi - Working Sheet`.
   - Ensure the sheet follows the structure detailed in the Table section below.
   - Mark rows as "Ready to Upload" in column AD (index 29) to include them in the upload process.

2. **Script Properties**
   - Set the Strapi token in the script properties:
     - Open your Google Apps Script project.
     - Navigate to `File > Project Properties > Script Properties`.
     - Add a new property with the key `STRAPI_TOKEN` and your Strapi API token as the value.

3. **Permissions**
   - Ensure the script has the necessary permissions to access Google Drive and make URL fetch requests.

## Google Sheet Structure

| Column Name                    | Index | Data Type | Description                                      |
|--------------------------------|-------|-----------|--------------------------------------------------|
| Name                           | 0     | String    | Name of the individual                           |
| Designation                    | 1     | String    | Designation of the individual                    |
| Testimonial Video Link         | 2     | URL       | Link to the testimonial video                    |
| LinkedIn Post Link             | 3     | URL       | Link to the LinkedIn post                        |
| Hike Percentage                | 4     | Number    | Percentage of hike received                      |
| Experience Level               | 5     | String    | Level of experience                              |
| Program Chosen                 | 6     | String    | Program chosen by the individual                 |
| Company Logo URL               | 7     | URL       | Google Drive URL of the company logo             |
| Profile Picture URL            | 8     | URL       | Google Drive URL of the profile picture          |
| Static Post URL                | 9     | URL       | Google Drive URL of the static post              |
| Google Review Link             | 10    | URL       | Link to the Google review                        |
| Google Review Text             | 11    | String    | Text of the Google review                        |
| Google Review Rating           | 12    | Number    | Rating of the Google review                      |
| Tag                            | 13    | String    | Tag associated with the entry                    |
| Transition 1 - From            | 14    | String    | Starting point of the first transition           |
| Transition 1 - To              | 15    | String    | Ending point of the first transition             |
| Transition 1 - Is Primary      | 16    | Boolean   | Indicates if the first transition is primary     |
| Transition 2 - From            | 17    | String    | Starting point of the second transition          |
| Transition 2 - To              | 18    | String    | Ending point of the second transition            |
| Transition 2 - Is Primary      | 19    | Boolean   | Indicates if the second transition is primary    |
| Transition 3 - From            | 20    | String    | Starting point of the third transition           |
| Transition 3 - To              | 21    | String    | Ending point of the third transition             |
| Transition 3 - Is Primary      | 22    | Boolean   | Indicates if the third transition is primary     |
| Transition 4 - From            | 23    | String    | Starting point of the fourth transition          |
| Transition 4 - To              | 24    | String    | Ending point of the fourth transition            |
| Transition 4 - Is Primary      | 25    | Boolean   | Indicates if the fourth transition is primary    |
| Transition 5 - From            | 26    | String    | Starting point of the fifth transition           |
| Transition 5 - To              | 27    | String    | Ending point of the fifth transition             |
| Transition 5 - Is Primary      | 28    | Boolean   | Indicates if the fifth transition is primary     |
| Ready to Upload                | 29    | String    | Indicates if the row is ready to be uploaded     |
| ID (Strapi Entry ID)           | 30    | Number    | Strapi Entry ID of the uploaded data             |
| Upload Status                  | 31    | String    | Status of the upload (e.g., Done)                |

* Note this is for the json payload mentioned in the [strapi-automation.js](strapi-automation.js) file.

## Script Functionality

The `uploadDataToStrapi` function performs the following tasks:

1. **Data Retrieval**
   - Retrieves data from the Google Sheet named `Strapi - Working Sheet`.

2. **File ID Extraction**
   - Extracts the file ID from Google Drive URLs.

3. **Image Upload**
   - Uploads images from Google Drive to Strapi and returns the file ID.

4. **Data Upload**
   - Constructs a payload based on the data in each row.
   - Uploads the payload to Strapi.
   - Updates the Google Sheet with the Strapi Entry ID and marks the row as done.

## Important Notes

- **Update the JSON Payload:** Ensure the JSON payload structure matches the content structure defined in your Strapi instance. Adjust the payload construction in the script accordingly.
- **Update API URL:** Make sure to update the `strapiUrl` variable in the script to the appropriate API URL for your Strapi instance.

## How to Use

1. **Run the Script**
   - Open your Google Apps Script project.
   - Run the `uploadDataToStrapi` function.

2. **Verify the Upload**
   - Check the Google Sheet for the Strapi Entry ID and status updates.
   - Verify the data in your Strapi instance.

By following the setup instructions and ensuring your Google Sheet is structured correctly, you can automate the process of uploading data to Strapi efficiently.
