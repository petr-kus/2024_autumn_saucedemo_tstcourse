from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, random, logging, datetime

#TODO Lektor - Bylo hodne komentovane na lekci tak jen par poznamek. Neni zmineno vse... .
#TODO Lektor - nma error uzivateli mi ten test neselze do konzole... nic tam nevidim. To je docela problem... . 

logging.basicConfig(filename="my_log.log", level=logging.DEBUG)
logging.info(f"Test executed on {datetime.datetime.now()}.")

class User: #Create test user obj
    def __init__(self, userName, password, firstName, secondName, zip):
        self.userName = userName
        self.password = password
        self.firstName = firstName
        self.secondName = secondName
        self.zip = zip

class Navigation(): #Create web navigation obj
    class Fields():
        userNameField = (By.ID, "user-name")
        passwordField = (By.ID, "password")
        firstNameField =(By.ID, "first-name")
        lastNameField = (By.ID, "last-name")
        zipField = (By.ID, "postal-code")
    class Btns():
        loginBtn = (By.ID, "login-button")
        addToCartBtn = (By.CLASS_NAME, "btn_primary")
        cartBtn = (By.ID, "shopping_cart_container")
        firstCheckoutBtn = (By.ID, "checkout")
        secondCheckoutBtn = (By.ID, "continue")
        lastCheckoutBtn = (By.ID, "finish")
    class OtherEls():
        itemsInCartAmount = (By.CLASS_NAME, "cart_quantity")
        checkoutComplete = (By.XPATH, "//*[contains(., 'Thank you')]")

#TODO Lektor - Pochvala za OOP ktere v sobe zahrnuje adresaci prvku vcetne ID! Jen to melo byt oddeleno do speare souboru. 
#TODO Lektor - Jen to melo byt oddeleno do speare souboru a nejspise stejne jako funkce nize... . 

def wait(seconds=2):
    time.sleep(seconds)
    
#TODO Lektor - Pochvala za parametrizaci waitu.
def setup(testPage):
    Option = Options()
    Option.add_argument("start-maximized")
    driver = testDriver
    logging.debug("Driver started.")
    driver.get(testPage)
    return driver

def loginTest(userName, password):
    try:
        driver.find_element(*Navigation.Fields.userNameField).send_keys(userName)
        driver.find_element(*Navigation.Fields.passwordField).send_keys(password)
        driver.find_element(*Navigation.Btns.loginBtn).click()
    except Exception as err:
        logging.debug(f"Error occured: {err}")
    logging.debug("Logged in.")
    #TODO Lektor - hmmm to se ale vypise i kdyz chyba nastane... 

def addToCartTest(additions):
    numAddedItems = 0 #Keeps track of products added during the test
    for x in range(additions): 
        AtCs=driver.find_elements(*Navigation.Btns.addToCartBtn)
        randomAtC = AtCs[random.randrange(0,len(AtCs)-1)] if len(AtCs) > 1 else AtCs[0]
        try:
            randomAtC.click()
        except Exception as err:
            logging.debug(f"Error occured while adding{randomAtC}: {err}!")
        numAddedItems += 1
        logging.debug(f"{randomAtC} was added to the cart!")
    return numAddedItems

def checkoutTest(fisrtName, lastName, zip, itemsAmount):
    driver.find_element(*Navigation.Btns.cartBtn).click()
    cartItems = driver.find_elements(*Navigation.OtherEls.itemsInCartAmount)
    cartAmount = 0
    for item in cartItems: #Checks for the amount of items currently in the cart
        itemAmount = int(item.get_attribute("innerText"))
        cartAmount += itemAmount

    if cartAmount < itemsAmount: #Compares items in the cart with items added during the test
        logging.debug("Some items weren't added to the cart.")
    elif cartAmount > itemsAmount: 
        logging.debug("There were items in the cart that were not added during this test.")
    else:
        logging.debug(f"There were {cartAmount} items added to the cart during this test.")
     #TODO Lektor - zbytecne moc upodminkovane... stacil jeden assert a jeden log...

    driver.find_element(*Navigation.Btns.firstCheckoutBtn).click() #Starting checkout
    try:
        driver.find_element(*Navigation.Fields.firstNameField).send_keys(fisrtName)
        driver.find_element(*Navigation.Fields.lastNameField).send_keys(lastName)
        driver.find_element(*Navigation.Fields.zipField).send_keys(zip)
    except Exception as error:
        logging.warning(f"Error occured: {error}")

    driver.find_element(*Navigation.Btns.secondCheckoutBtn).click()
    logging.debug("Second checkout step executed!")

    driver.find_element(*Navigation.Btns.lastCheckoutBtn).click()
    logging.debug("Last checkout step executed!")

    if driver.current_url == "https://www.saucedemo.com/checkout-complete.html" and driver.find_element(*Navigation.OtherEls.checkoutComplete):
        logging.info(f"Checkout test completed successfully on {datetime.datetime.now()}. ")
        #TODO Lektor - to je supoer ten date time ale uz je vetsioonou soucasti logu...
    else:
        logging.warning("Checkout failed!")
        #TODO Lektor - to je spis error

def teardown():
    wait
    driver.close
    driver.quit


#Test data
testPage = "https://www.saucedemo.com/"
testUser = User("standard_user", "secret_sauce", "Joe", "Doe", "111") #(login name, password, first name, last name, zip code)
numItemsToOrder = 2
testDriver = webdriver.Chrome()

#TODO Lektor - velka pochvala za oddeleni testovacich dat! jen to melo byt asi spis nahore?

#Test execution
try: 
    driver = setup(testPage)
    loginTest(testUser.userName, testUser.password)
    numAddedItems = addToCartTest(numItemsToOrder)
    checkoutTest(testUser.firstName, testUser.secondName, testUser.zip, numAddedItems)
    teardown()
except Exception as err:
    logging.warning (f"Test failed: {err}!")
    #TODO Lektor - to je spis error