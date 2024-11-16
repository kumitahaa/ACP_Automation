# --------------------------------- Import -------------------------------------
import time, pandas as pd, random, traceback, os, sys
# from selenium import webdriver as uc
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from fake_useragent import UserAgent





# --------------------------------- Initializing Variables -------------------------------------
driver = ""
df = pd.DataFrame()
remaining_df = pd.DataFrame()
line_break = "=" * 60

zip_input ="85716"
address_input = "3632 E Lee St"
long_input = "32.4"
lat_input = "12.42"

email_input = "abc@gmail.com"
phone_input = "5205432459"
first_time_adrs = True

# We handle DOB as Day/Month/Year    OR Day-Month-Year

result_msg = ""


def get_data_from_csv():
    print("Getting Data from CSV...")
    global df, remaining_df
    df = pd.read_csv("input.csv", )
    df.to_csv("prev_input.csv", index= False)
    remaining_df = df.copy()
    print(df.head())

def init():
    global driver
    print("Opening with unique profile...")
    ua = UserAgent()
    user_agent = ua.random
    options = uc.ChromeOptions()
    options.add_argument(f'user-agent={user_agent}')
    width = random.randint(1024, 1920)
    height = random.randint(720, 1080)
    options.add_argument(f'--window-size={width},{height}')
    options.add_argument('--disable-webrtc')
    if random.choice([True, False]):
        options.add_argument("--disable-javascript")
    driver = uc.Chrome(options=options)
    print("Opened WebPage in new tab with unique fingerprint...")
    driver.delete_all_cookies()
    return driver

# --------------------------------- Open WebPage -------------------------------------
def open_page():
    search_url = f"https://enroll.excesstelecom.com/"
    driver.get(search_url)
    print("Opened WebPage in new tab...")
    print("="*70)

# --------------------------------- Start Function -------------------------------------
def start():
    global result_msg
    print(line_break)
    print("Start of Start Function")

    for index, person in df.iterrows():
        result_msg = ""
        
        print(line_break)
        print(line_break)
    
        print(f"Processing {index}th Record...")
        print(person)
    
        print(line_break)
        print(line_break)

        # Actual Operations
        back_to_personal_info()

        personal_info(person)
        addressPage(person)

        if is_duplicate_lead():
            print("DUP_LEAD Funtion TRUE...")
            print(result_msg)
            write_to_file(index)
            print("Written to File... Continuing to Next")
            continue

        q1_page(person)
        choose_plan_page(index)

        if is_sim_page():
            choose_plan_page(index)

        open_national_verifier()
        get_result()

        write_to_file(index)
        print("Written to File... Continuing to Next")


    print("End of Start Function")
    print(line_break)

# --------------------------------- Login Function -------------------------------------
def login(zip = zip_input, email = email_input):
    print(line_break)
    print("Start of Login Function")

    try:
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "enroll_first_name")))
        print("Already Logged In... Continuing to next page...")
        return True
    except:
        pass

    try:
        zip_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "enrollment_zipcode_popup")))
        email_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "enrollment_email_id_step_1_popup")))
        try:
            zip_field.clear()
            email_field.clear()
            time.sleep(1)
            zip_field.send_keys(zip)
            email_field.send_keys(email)
            print("ZIP & Email Entered...")
            try:
                next_btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((
                    By.XPATH, "/html/body/div[4]/div[1]/div/div/div/div[2]/div/div[4]/p/button")))
                time.sleep(2)
                try:
                    next_btn.click()
                    time.sleep(5)
                except:
                    print("Can't click Next button")
            except:
                print("Can't Find Next Button...")
                if not isLoggedIn():
                    login()
                    return 0
        except:
            print("Can't Type Email, and ZIP...")
            if not isLoggedIn():
                login()
                return 0
    except:
        print("Can't find ZIP Field")
        if not isLoggedIn(zip, email):
            login()
            return 0

    print("End of Login Function")
    print(line_break)

# --------------------------------- Check if Logged In Already -------------------------------------
def isLoggedIn():
    try:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "enroll_first_name")))
        print("We are Logged In Now...")
        return True
    except:
        print("Not Logged In, Calling Login Function again...")
        login()
        return False

# --------------------------------- Enter Personal Info of the person -------------------------------------
def personal_info(person):

    print(line_break)
    print("Start of Personal_Info Function")

    try:
        WebDriverWait(driver,2).until(EC.presence_of_element_located((By.ID, "enrollment_zipcode_popup")))
        print("We are on Login Page, going back to login.")
        login()
        personal_info(person)
        return 0
    except:
        pass

    first_name = person["first"]
    last_name = person["last"]
    ssn = person["ssn"]
    dob = person["dob"]
    phone_no = phone_input
    try:
        b = dob.split("/")
    except:
        b = dob.split("-")
    finally:
        day = int(b[0])
        month = int(b[1])
        year = int(b[2])
        print(f"Month: {month:02}, Day: {day:02}, Year: {year}")

    try:
        first_name_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "enroll_first_name")))
        last_name_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "enroll_last_name")))
        ssn_field =  WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "enroll_ssn")))
        phone_field = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "personal_contact_number")))
        try:
            month_dd = Select(driver.find_element(By.ID, "enroll_month"))
            day_dd = Select(driver.find_element(By.ID, "enroll_day"))
            year_dd = Select(driver.find_element(By.ID, "enroll_year"))
        except:
            print("Error while Selecting Date fields with SELECT...")
        time.sleep(1)
        try:
            # Clear Fields
            first_name_field.clear()
            last_name_field.clear()
            ssn_field.clear()
            phone_field.clear()
            time.sleep(1)

            # Start Sending Keys
            first_name_field.send_keys(first_name)
            time.sleep(1)
            last_name_field.send_keys(last_name)
            time.sleep(1)
            ssn_field.send_keys(ssn)
            time.sleep(1)
            phone_field.send_keys(phone_no)
            time.sleep(1)

            print("Filled Personal Info fields")

            driver.execute_script("""if (!document.getElementById("text_checkbox_best_way").checked){document.getElementById("text_checkbox_best_way").click()}""")
            # text_msg_checkbox.click()
            print("Checked Message Box")
            time.sleep(1)
            try:
                print("Trying to set dates")
                month_dd.select_by_value(f"{month:02}")
                day_dd.select_by_value(f"{day:02}")
                year_dd.select_by_value(f"{year}")
                print("DOB all Set...")
            except:
                print("Error Setting dates.")
        except:
            print("Error inputting Personal Info Fields.")
    except:
        print("Can't Find Personal Info fields. Check if we are still on Login page...")
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "enrollment_zipcode_popup")))
            print("We are on Login Page, going back to login.")
            login()
            personal_info(person)
            return 0
        except:
            print("Not on Log in page as well.")
    try:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-next1")))
        driver.execute_script("""document.getElementsByClassName("btn-next1")[1].click()""")
        print("Clicked CONTINUE BUTTON on PERSONAL INFO PAGE")
        time.sleep(5)
    except:
        print("Can't Click Continue Button")

    print("End of Personal_Info Function")
    print(line_break)

# --------------------------------- Check if Personal_INFO Page -------------------------------------
def isPersonalInfoPage():
    try:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "enroll_first_name")))
        print("We are On Personal INFO Page In Now...")
        return True
    except:
        print("Not On Personal Info Page... Going Next...")
        return False

# --------------------------------- Enter Address -------------------------------------
def addressPage(person, address = address_input):
    global first_time_adrs

    try:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "another_adult")))
        print("Already on Q1 Page...")
        return 0
    except:
        pass

    print(line_break)
    print("Start of AddressPage Function")
    try:
        address_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "enroll_address1")))
        time.sleep(1)
        try:
            if first_time_adrs:
                address_field.clear()
                time.sleep(1)
                address_field.send_keys(address)
                time.sleep(1)
                first_time_adrs = False
                
            try:
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-next1")))
                driver.execute_script("""document.getElementsByClassName("btn-next1")[3].click()""")
                time.sleep(5)
            except:
                print("Can't Click Continue Button")
        except:
            print("Can't Send input address...")
            addressPage(person, address= address_input)
            return 0
    except:
        print("Can't find Address field")
        if isPersonalInfoPage():
            personal_info(person)
            addressPage(person)
            return 0 

    print("End of AddressPage Function")
    print(line_break)

# --------------------------------- Check if Duplicate Lead -------------------------------------
def is_duplicate_lead():
    print(line_break)
    print("Start of IS_DUPLICATE_LEAD Function")
    try:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "another_adult")))
        print("Already on Q1, passing Duplicheck")
        print("End of IS_DUPLICATE_LEAD Function")
        print(line_break)
    except:
        global result_msg
        try:
            WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "swal-title")))
            result_msg = driver.find_elements(By.CLASS_NAME, "swal-title")[0].text
            print("Duplicate Found...")
            print("End of IS_DUPLICATE_LEAD Function")
            print(line_break)
            return True
        except:
            print("Not Duplicate...")
            print("End of IS_DUPLICATE_LEAD Function")
            print(line_break)
            return False

# --------------------------------- Not Living with Another Adult -------------------------------------
def q1_page(person):
    global first_time_adrs
    print(line_break)
    print("Start of Q1_Page Function")
    
    try:
        try:
            WebDriverWait(driver,3).until(EC.presence_of_element_located((By.ID, "another_adult")))
        except:
            address_field = WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.ID, "enroll_address1")))
            print("Still on Addrss Page...")
            time.sleep(1)
            first_time_adrs = True
            addressPage(person)
    except:
        pass

    try:
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "another_adult")))
        try:
            driver.execute_script("""document.getElementsByClassName("btn-next1")[1].click()""")
            print("Clicked NO BUTTON...")
            time.sleep(5)
        except:
            print("Can't Click Continue Button")
    except:
        print("Can't Find Field with Another_Adult as ID")
    
    print("End of Q1_Page Function")
    print(line_break)

# --------------------------------- Choose Plan for Aid Page -------------------------------------
def choose_plan_page(index):
    print(line_break)
    print("Start of Choose_Plan_Page Function")

    try:
        driver.execute_script("""document.getElementsByClassName("mylinknationalverifier")[1].remove()""")
        time.sleep(1)
        driver.execute_script("""document.getElementsByClassName("mylinknationalverifier")[1].remove()""")
    except:
        print("Error removing National Verifier Button...")
        df.loc[index, 'national_veri_btn_error'] = "Error Processing This Lead..."
        return False
    try:
        time.sleep(5)
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "tickDIV_1")))
        try:
            time.sleep(1)
            driver.execute_script("""document.getElementById("tickDIV_1").click()""")
            print("Supplement Plan Chosen...")
            time.sleep(1)
            try:
                driver.execute_script("""document.getElementsByClassName("btn-next1")[1].click()""")
                print("Clicked CONTINUE BUTTON...")
                time.sleep(10)
            except:
                print("Can't Click Continue Button")
        except:
            print("Can't Clcik Supplemental Plan")
    except:
        print("Can't Find Choose Supplemental Plan")
    
    print("End of Choose_Plan_Page Function")
    print(line_break)

# --------------------------------- Check if SIM PAGE appears -------------------------------------
def is_sim_page():
    print(line_break)
    print("Start of IS_SIM_PAGE Function")

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "mobile_box_plan")))
        print("SIM Page Found")
        driver.execute_script("""document.getElementsByClassName("btn-next1")[0].click();""")
        time.sleep(5)
    except:
        print("All Good, No SIM Page...")

    print("End of IS_SIM_PAGE Function")
    print(line_break)

# --------------------------------- Open National Verifier Page -------------------------------------
def open_national_verifier():
    print(line_break)
    print("Start of open_national_verifier Function")
    
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "mylinknationalverifier")))
        ntn_veri_btn = driver.find_elements(By.CLASS_NAME, "mylinknationalverifier")[0]
        ntn_veri_btn.click()
        print("National Verifier Button Clicked")
        time.sleep(15)
    except:
        print("Can't Find National Verifier Button... Don't Know What to do now.")
    
    print("End of open_national_verifier Function")
    print(line_break)

# --------------------------------- Get Result on National Verifier Page -------------------------------------
def get_result():
    global result_msg
    print(line_break)
    print("Start of GET_RESULT Function")
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "h1")))
        result_msg = driver.find_elements(By.TAG_NAME, "h1")[0].text
        print(result_msg)
    except:
        print("Can't find H1 on Result Page...")
        try:
            driver.execute_script("""document.getElementById("nextBtn").click();""")
            print("Clicked Next Button On Result Page Once...")
            time.sleep(5)
            try:
                WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "h1")))
                result_msg = driver.find_elements(By.TAG_NAME, "h1")[0].text
                print(result_msg)
            except:
                print("Can't Get H1 2nd time...")
        except:
            print("Can't Click Next on Result Page...")

    print("End of GET_RESULT Function")
    print(line_break)

# --------------------------------- Come back to first page after processing -------------------------------------
def back_to_personal_info():
    url = "https://enroll.excesstelecom.com/enrollment2/personal_info.php"
    driver.get(url)
    print("Starting from Personal Info Page...")

# --------------------------------- Write to File -------------------------------------
def write_to_file(index):
    print("=="*50)
    # Writing result message to the result message Column of Output file
    df.loc[index, 'result_message'] = result_msg
    print(f"Writing {result_msg} to CSV...")
    print("=="*50)
    # Dropping current Index from Remaining File
    remaining_df.drop(index, inplace=True)

# --------------------------------- Function for file names -------------------------------------
def find_non_existing_file(file_name):
    counter = 1
    while os.path.exists(file_name):
        base, ext = os.path.splitext(file_name)
        file_name = f"{base}_{counter}{ext}"
        counter += 1
    return file_name

# --------------------------------- Driver function for program -------------------------------------
def driver():
    print("Driving Now...")
    get_data_from_csv()
    init()
    open_page()
    login()
    start()

# --------------------------------- Running the program -------------------------------------
try:
    exception_caused = False
    driver()
except Exception as e:
    exception_caused = True
    print("==="*30)
    print("==="*30)
    print("Caused an EXCEPTION === ENDING BOT...")
    print("==="*30)
    print("==="*30)
    print(f"Exception occured: {e}")
    traceback.print_exc()
else:
    pass
finally:
    print("==="*30)
    print("==="*30)
    print("FINALLY... ENDING....")
    print("==="*30)
    print("==="*30)
    driver.quit()
    
    filtered_df = df[(df['result_message'].notna())]
  
    output_name = "output.csv"

    # Check if file already exists and find a non-existing file name
    output_file = find_non_existing_file(output_name)

    # Save the filtered DataFrame to a CSV file without including the index
    filtered_df.to_csv(output_file, index=False)
    print("Created output file.")


    remaining_df.to_csv("input.csv", index=False)
    print("Created Remaining File..")
    
    print("===========Finished===========")
    if exception_caused:
        sys.exit(1)
    else:
        sys.exit(0)