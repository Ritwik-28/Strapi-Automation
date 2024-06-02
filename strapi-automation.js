function uploadDataToStrapi() {
  // Get the data from the Google Sheet
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Strapi - Working Sheet');
  var data = sheet.getDataRange().getValues();
  
  // Strapi setup
  var strapiUrl = 'https://strapi.internal.crio.do/api/success-stories';
  var strapiToken = PropertiesService.getScriptProperties().getProperty('STRAPI_TOKEN');
  var strapiUploadUrl = 'https://strapi.internal.crio.do/api/upload';

  // Function to extract file ID from Google Drive URL
  function extractFileIdFromUrl(url) {
    var fileIdMatch = url.match(/[-\w]{25,}/);
    return fileIdMatch ? fileIdMatch[0] : null;
  }

  // Function to upload images from Google Drive as an asset
  function uploadImageFromDrive(url, name) {
    try {
      var fileId = extractFileIdFromUrl(url);
      if (!fileId) {
        throw new Error('Invalid Google Drive URL');
      }
      var file = DriveApp.getFileById(fileId);
      var blob = file.getBlob();
      var originalFileName = file.getName();
      var newFileName = name + "_" + originalFileName;

      var formData = {
        files: blob.setName(newFileName),
        ref: 'upload',
        source: 'admin',
        path: ''
      };

      var options = {
        method: 'post',
        headers: {
          'Authorization': 'Bearer ' + strapiToken
        },
        payload: formData
      };

      var uploadResponse = UrlFetchApp.fetch(strapiUploadUrl, options);
      var responseJson = JSON.parse(uploadResponse.getContentText());
      return responseJson[0].id; // Assuming the response contains the file ID
    } catch (e) {
      Logger.log('Error uploading image from Drive: ' + e.message);
      return null;
    }
  }

  // Loop through the data and send to Strapi
  for (var i = 2; i < data.length; i++) { // Start from 3rd row in the sheet (index 2)
    var row = data[i];

    // Check if the row is marked as "Ready to Upload" (column AD, index 29)
    if (row[29] !== 'Ready to Upload') {
      continue;
    }

    var payload = {
      data: {}
    };

    // Conditionally add fields to the payload if they are not empty
    if (row[0]) payload.data.name = row[0];
    if (row[1]) payload.data.designation = row[1];
    if (row[2]) payload.data.testimonial_video_link = row[2];
    if (row[3]) payload.data.linkedin_post_link = row[3];
    if (row[5]) payload.data.experience_level = row[5];
    if (row[6]) payload.data.program_chosen = row[6];

    // Handle company logo and profile picture uploads
    var companyLogoId = row[7] ? uploadImageFromDrive(row[7], 'company_logo') : null;
    var profilePictureId = row[8] ? uploadImageFromDrive(row[8], 'profile_picture') : null;
    var staticPostId = row[9] ? uploadImageFromDrive(row[9], 'static_post') : null;

    if (companyLogoId) payload.data.company_logo = companyLogoId;
    if (profilePictureId) payload.data.profile_picture = profilePictureId;
    if (staticPostId) payload.data.static_post = staticPostId;

    // Handle Google review
    if (row[10] || row[11] || row[12]) {
      payload.data.google_review = {};
      if (row[10]) payload.data.google_review.link = row[10];
      if (row[11]) payload.data.google_review.text = row[11];
      if (row[12] && !isNaN(row[12])) payload.data.google_review.rating = row[12];
    }

    // Handle tags
    if (row[13]) payload.data.Tag = [{ text: row[13] }];

    // Handle transitions
    var transitions = [];
    for (var j = 14; j < 29; j += 3) { // Columns O to AC (5 transitions)
      var fromValue = row[j];
      var toValue = row[j + 1];
      var isPrimaryValue = row[j + 2] === true || row[j + 2] === 'TRUE';

      // Ensure fromValue and toValue are strings
      if (fromValue && toValue) {
        if (typeof fromValue !== 'string') fromValue = fromValue.toString();
        if (typeof toValue !== 'string') toValue = toValue.toString();

        Logger.log('Processing Transition: from=' + fromValue + ', to=' + toValue + ', isPrimary=' + isPrimaryValue);

        transitions.push({
          from: fromValue,
          to: toValue,
          isPrimary: isPrimaryValue
        });
      }
    }
    if (transitions.length > 0) payload.data.Transition = transitions;

    // Only add hike_percentage if it's a valid non-negative number
    if (row[4] !== null && row[4] !== '' && !isNaN(row[4]) && row[4] >= 0) {
      payload.data.hike_percentage = row[4];
    }

    // Remove null values from the payload
    for (var key in payload.data) {
      if (payload.data[key] === null || payload.data[key] === undefined) {
        delete payload.data[key];
      }
    }

    var options = {
      method: 'post',
      contentType: 'application/json',
      headers: {
        'Authorization': 'Bearer ' + strapiToken
      },
      payload: JSON.stringify(payload)
    };

    try {
      var response = UrlFetchApp.fetch(strapiUrl, options);
      var responseJson = JSON.parse(response.getContentText());
      Logger.log(response.getResponseCode());
      Logger.log(response.getContentText());

      if (response.getResponseCode() === 200 || response.getResponseCode() === 201) {
        // Mark the row as done and store the ID
        sheet.getRange(i + 1, 31).setValue(responseJson.data.id); // Store the ID in column AE
        sheet.getRange(i + 1, 32).setValue('Done'); // Mark as done in column AF
      } else {
        Logger.log('Error: ' + response.getContentText());
      }
    } catch (e) {
      Logger.log('Exception: ' + e.message);
    }
  }
}
