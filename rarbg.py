from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pytesseract
import cv2
import pyautogui as gui
import os


# Method to save screenshot to /main/screens/ path
def make_screenshot():
    img = gui.screenshot(region=(960, 400, 140, 70))
    dir = os.path.dirname(__file__)
    time_start = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    make_screenshot.path = os.path.join(dir + '\\screens', str(time_start) + '.png')
    img.save(make_screenshot.path)
    print('Screenshot saved to: ' + make_screenshot.path)


# 0. Fill path to your ChromeDriver file
driver = webdriver.Chrome(executable_path=r'PATH_TO_CHROMEDRIVER_FILE')
wait = WebDriverWait(driver, 10)

# 1. Open website and wait for captcha
driver.get("http://rarbgmirror.org/threat_defence.php")
driver.maximize_window()
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[lazyload]")))

# 2. Save screenshot using PyAutoGUI
make_screenshot()

# 3. Get text from screenshot using OCR Tesseract
image = cv2.imread(make_screenshot.path)
pytesseract.pytesseract.tesseract_cmd = r'PATH_TO_TESSERACT_EXE_FILE'
text = pytesseract.image_to_string(image)
print('Captcha is: ' + text)

# 4. Fill text to the field using Selenium
elem = driver.find_element_by_css_selector('#solve_string')
elem.send_keys(text)

# 5. Check that page was changed
assert driver.current_url != 'http://rarbgmirror.org/threat_defence.php'

driver.quit()
