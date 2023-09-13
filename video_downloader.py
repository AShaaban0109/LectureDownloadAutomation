from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time
import pyautogui

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Change these values
USERNAME = '....'
PASSWORD = '....'

# click on a picture present on the screen
# TODO handle error if image not found
def click_on_picture(path):
    img_location = pyautogui.locateOnScreen(path)
    image_location_point = pyautogui.center(img_location)
    x, y = image_location_point
    pyautogui.click(x, y)
    return True

# install video downloader extension and setup other options such as default dl dir
def options_setup():
    chrome_options = Options()
    chrome_options.add_argument("force-dark-mode")
    chrome_options.add_extension('video_downloader_extension.crx')

    # download location can be altered if needed. Eg. for storing on a harddrive.
    prefs = {"profile.default_content_settings.popups": 0,
            "download.default_directory": os.getcwd() + "/Downloaded Lectures",
            # "download.default_directory": "/media/USERNAME/HDD/All Lectures",
            "directory_upgrade": True}
    chrome_options.add_experimental_option("prefs", prefs)
    return chrome_options

# sign in to panopto. This takes us to the final stage where we have all the vids listed
def init_and_sign_in(driver):
    driver.maximize_window()
    driver.delete_all_cookies()

    # Open panopto website and close extension welcome page
    driver.get('https://uniofbath.cloud.panopto.eu/Panopto/Pages/Sessions/List.aspx#notificationBannerShown=true&isSharedWithMe=true');
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

    # Select the id box
    login_button = driver.find_element(By.ID, 'loginButton')
    login_button.click()
    time.sleep(2)

    username_box = driver.find_element(By.ID, 'username')
    password_box = driver.find_element(By.ID, 'password')
    submit_box = driver.find_element(By.NAME, 'submit')

    username_box.send_keys(USERNAME)
    password_box.send_keys(PASSWORD)
    submit_box.click()

    time.sleep(2)

def start(username = USERNAME, password = PASSWORD, lectureCount = 10, startIndex = 0):
    # Using Chrome to access web
    chrome_options = options_setup()
    driver = webdriver.Chrome(options = chrome_options)

    init_and_sign_in(driver)

    # # sort by location and make the number of vids shown 250 per page.
    # driver.find_element(By.ID, 'listViewHeader-2').click()
    # time.sleep(1)
    # driver.find_element(By.ID, 'listViewHeader-2').click()
    # driver.find_element(By.CLASS_NAME, 'MuiSelect-root').click()
    # time.sleep(1)

    # sort by location and make the number of vids shown 250 per page.
    driver.find_element(By.ID, 'listViewHeader-8').click()
    driver.find_element(By.CLASS_NAME, 'MuiSelect-root').click()
    time.sleep(1)
    # Find the element using XPath and the data-value attribute
    per_page = "250"
    driver.find_element(By.XPATH,f'//li[@data-value="{per_page}"]').click()
    time.sleep(10)

    pagenumber=1
    for i in range(pagenumber -1):
        button_xpath = "//button[@class='MuiButtonBase-root MuiPaginationItem-root MuiPaginationItem-page' and @aria-label='Go to next page']"
        button = driver.find_element(By.XPATH,button_xpath).click()
        time.sleep(10)
        

    # List of thumbnails that when clicked, redict to the url of the lecture
    thumbnails_window = driver.current_window_handle
    thumbnails = driver.find_elements(By.CLASS_NAME, 'jss22')

    # loop through all thumbnails and dl all.
    # todownloadnext = [2,31, 51, 42, 45, 32]

    # for i in range(startIndex, startIndex + lectureCount):
    for i in range(startIndex, startIndex - lectureCount, -1):
        thumbnails[i].click()
        time.sleep(20)

        # Wait for the new tab to open
        video_page_handle = None
        while not video_page_handle:
            for handle in driver.window_handles:
                if handle != thumbnails_window:
                    video_page_handle = handle
                    break


        # Click on extension icon and get the download site.
        click_on_picture("1_extension_icon.png")
        time.sleep(1)
        click_on_picture('2_video_downloader_icon.png')
        time.sleep(5)
        click_on_picture('3_force_dl_icon.png')

        # Wait for the new tab to open
        video_dl_page_handle = None
        while not video_dl_page_handle:
            for handle in driver.window_handles:
                if handle != thumbnails_window and handle != video_page_handle:
                    video_dl_page_handle = handle
                    driver.switch_to.window(video_dl_page_handle)
                    break
        
        time.sleep(10)

        save_videos_buttons = driver.find_elements(By.ID, 'dlVsaveBtn')
        save_videos_buttons = save_videos_buttons[:-1]  # remove the last void entry button the site has

        # Iterate through the buttons and click the one that becomes visible
        for n, button in enumerate(save_videos_buttons):
            # Wait until the button becomes visible (not hidden) then click
            element = WebDriverWait(driver, 10000).until(EC.visibility_of(button))
            element.click()
            print(f'Lecture {i+1}, part {n+1}/{len(save_videos_buttons)} has been downloaded.')
            time.sleep(3)
            # handle occasional popup window asking to share with friends
            try:
                popup = driver.find_element(By.CSS_SELECTOR, ".modal.show")
                close_buttons = driver.find_elements(By.XPATH, "//button[text()='Maybe next time']")
                close_buttons[1].click() # 0 is a different button that doesnt work
                time.sleep(2)

            # if no popup continue as normal
            except:
                continue
        print(f'Lecture {i+1} download complete. \n')

        driver.close()
        driver.switch_to.window(video_page_handle)
        driver.close()
        driver.switch_to.window(thumbnails_window)
        time.sleep(2)
    print(f'{lectureCount} lectures successfully downloaded. \n')
    driver.quit()
    

# Start scipt without GUI
# start()

