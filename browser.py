# using selenium, transfer cookies and session information with selenium
import sqlite3
import os 
import re

from http.cookiejar import Cookie
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from time import sleep, gmtime
from traceback import print_exc


# this is where your firefox profile will be, generated from    $ firefox --ProfileManager
PROFILE_DIR = "/home/box/.mozilla/firefox/8wbgzkd7.Blackboard"




# Headless browser class
class Browser:

    # Constructor 
    def __init__(self, url: str):

        self.url = url
        self.domain = re.findall(r"https://(\S*?)\.", url)[0]

        self.options = None
        self.driver = None
        

    # waits until the page is loaded
    def wait_until_done(self):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )    


    # gets webdriver options for headless operation
    def get_headless_options(self):
        o = Options()
        o.add_argument("--headless")
        o.add_argument("--profile")
        o.add_argument(PROFILE_DIR)
        return o

    # gets webdriver options for logging into outlook via the browser GUI
    def get_login_options(self):
        o = Options()
        o.add_argument("--profile")
        o.add_argument(PROFILE_DIR)
        return o


    # scrolls down the page by a whole page view
    def scroll_down_page(self):
        if self.driver != None:
            print("[+] Scrolling down page now.")

            current_height = self.driver.execute_script("return document.body.scrollHeight")

            
            
            self.driver.execute_script(f"window.scrollBy({current_height}, {current_height*2});")
            
            current_height = self.driver.execute_script("return document.body.scrollHeight")
            print(f"[+] New Height: {current_height}")


            
    # gets all course names and their elements from the main BSU page 
    # TODO: ISSUE -> get_courses() can only gather 5 courses at a time from the home page in "headless" mode
    def get_courses(self):
        if self.driver != None:

            # TODO: page scroll test
            # document = self.driver.find_ele.ments(By.TAG_NAME, "html")
            # document.send_keys(ARROW_DOWN)
            
            print("[+] Getting courses now, waiting 10 seconds first")

            # Implicit Wait  SRC: https://selenium-python.readthedocs.io/waits.html
            self.driver.implicitly_wait(10)

            self.scroll_down_page()
            self.driver.implicitly_wait(10)

            # matches webelements containing the classname "course-title" on the courses page
            # SRC: https://selenium-python.readthedocs.io/locating-elements.html

            wait = WebDriverWait(self.driver, 20)
            
            wait.until(                                                                                                                                                                                        
               EC.presence_of_all_elements_located((By.CLASS_NAME, "course-title"))                                                                                                                          
            )  

            
            found_elements = {}
            class_cnt = 0
            prev_cnt = None
            
            while len(found_elements.keys()) < 6:
                classes = self.driver.find_elements(By.CLASS_NAME, "course-title")
                class_cnt = len(classes) 
                

                visible = len(found_elements)
                
                for cla in classes:
                    if cla.text != "" and cla.text not in found_elements.keys():
                        found_elements[cla.text] = cla
                        print("\n".join([f for f in found_elements.keys()]), end = "\n\n")
                        
                if prev_cnt == len(found_elements):
                    self.scroll_down_page()
                    self.wait_until_done()
                    
                else:
                    prev_cnt = len(found_elements)

                

            print(visible)
            print("[+] Successfully found all classes")
            for name, cla in found_elements.items():
                print(name)
            
                    

        
    # loads the webdriver in modes: "login", "headless"
    def load_driver(self, mode):

        # ff_cap = DesiredCapabilities.FIREFOX
        # TODO: ff_capabilities["marionette"] = True
        
        # get mode of operation
        if mode == "headless":  
            self.options = self.get_headless_options()
            
        elif mode == "login":
            self.options = self.get_login_options()

        # add all desired capabilities
        for key, value in DesiredCapabilities.FIREFOX.items():
            self.options.set_capability(key, value)

        self.options.add_argument("--start-maximized")      
         
        # create firefox webdriver
        self.driver = webdriver.Firefox(
            options = self.options,
        )
        
        
        # hide javascript automation
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


    # if the webdrivewr gets caught at a login page handle it by asking user to login
    def login(self):
        # load the driver
        self.load_driver("login")

        # go to the url
        self.driver.get(self.url)
        
        self.wait_until_done()
        
        current_url = self.driver.current_url
        
        while self.url not in self.driver.current_url:
            

            if self.driver.current_url != current_url:
                    # self.record_session(current_url)
                    current_url = self.driver.current_url
            else:
                continue


        self.wait_until_done()
        
        print("[+] Press enter once you have finished logging in")

        self.driver.close()
        
  
    # gets the url
    def start(self):


        

        self.load_driver("login")
        self.driver.get(self.url)

        self.wait_until_done()
        current_url = self.driver.current_url

        if self.url not in self.driver.current_url:
            print("[+] didnt login sad!")
            self.driver.close()
            self.login()
            self.start()
            return
            
        else:
            print(f"[+] Driver Successfully made it to {self.driver.current_url}")
            self.get_courses()
        #TODO: here will be the extraction of courses and recurse into them
        
        # class page:

        #   PARSING FOLDERS: get by classname click-to-invoke-container

        #   PARSING CONTENT LINKS(PDF, DOCX): 
        #       get elements by attribute  data-analytics-id = content.item.course.outline.courseContent.link  -> extract text for filename
        #       click button with attribute data-analytics-id = component.directives.content-item-base.overflowMenu.showMenu.button
        #       click button with attribute data-analytics-id = component.directives.content-item-base.overflowMenu.global.download.link
        #       how to download files using selenium?

        # 
        # self.wait_until_done()
        # 
        # 
        # # matches webelements containing the classname "course-title" on the courses page
        # classes = self.driver.find_elements(By.CLASS_NAME, "course-title")
        # 
        # 
        # wait = WebDriverWait(self.driver, timeout=50)
        # 
        # wait.until(lambda _: classes[0].is_displayed())
        # 
        # for cla in classes:
        #     # cla.click()
        #     # self.wait_until
        #     print(cla.text)




  # closes the driver and all resources 
    def close(self):
        try:
            print("Quitting...")
            self.driver.close()
            
            
        except:
            return

        
    # Main 
    def main(self):

        print("\n\nSTART\n")
        
        try:

            self.start()
            
        except Exception as err:
        
            # print error information
            print_exc()
            print(f"\n\n[ ERROR ]: {err}")
            
            self.close()
            
        print("\nDONE\n\n")






# main script
if __name__ == "__main__":

    browser = Browser("https://bridgew.blackboard.com/ultra/course")

    
    browser.main()

    browser.close()
    
    
   
