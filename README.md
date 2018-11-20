# camcardPhotoSaver
This script is made for collecting name card images on camcard.com site.
Because, camcard.com does not provide any method for downloading "MY namcard" images at once.

# Prepare to use
Before using this code, following tools must be installed on your system.

* Python 3.x
* [Chrome driver](http://chromedriver.chromium.org/downloads)
* Chrome

## Dependency
This code also need following pip libraries.

* selenium
* urllib3

## How to use
1. Set your login information on line 69, 72.

```(python)
driver\
    .find_element_by_xpath('//*[(@id = "input_email")]')\
    .send_keys('ID') # Set your camcard ID
driver\
    .find_element_by_xpath('//*[(@id = "input_pwd")]')\
    .send_keys('PASSWORD') # Set your camcard Password
```

2. Set directory for saving name card images on line 118.

```(python)
get_image(driver, pic_url, 'SAVE TO DIRECTORY') # Set directory to save files.
```

3. Put chromdriver file into 'libs' directory and Run script.

## Notice
This script's working might be regarded as attack by www.camcard.com.



