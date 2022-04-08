import configparser
import csv
import time
import sys
import urllib.request
import os
from wsgiref.util import setup_testing_defaults
import zipfile
import random
import string
from datetime import date
from getpass import getpass

try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.firefox.options import Options
    import cryptocode
except ImportError:
    print('Installing Required Dependancies')
    import sys
    try:
        import subprocess
        print('Installing Python dependancies')
        packages=['solenium','cryptocode']
        for package in packages:
            try:
                print('installing ',package)
                subprocess.check_call([sys.executable, "-m", "pip", "install",package])
            except:
                pip=subprocess.run(['curl', 'https://bootstrap.pypa.io/get-pip.py','-o get-pip.py'])
                print(pip.stdout)
                print('instralling pip package manager')
                subprocess.run('get-pip.py')
                os.remove('get-pip.py')
                print('pip installed')
                print('installing required dependancies')
                subprocess.check_call([sys.executable, "-m", "pip", "install",package])

    except:
        print('failed to install dependancies')
months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
path=os.getcwd()
setting_file=path+'/MVSettings.ini'
def set_config():
    print('setting file var: ',setting_file)
    if os.path.exists(setting_file):
        get_config()
    else:
        print('Now Loading First Run Setup')
        print('These settings will only be asked for on the first run.')
        operating_system=sys.platform
        if operating_system=='darwin'or operating_system=='Darwin':
            print('Operating system is:', operating_system)
            browser='safari'
            wdriver='y'
        elif operating_system=='windows' or operating_system=='Windows' or operating_system=='win32':
            print('have you previously installed the solenium web driver? (y/n')
            wdriver=input()
            if wdriver == 'n' or wdriver == 'N' or wdriver == 'no' or wdriver =='No':
                print('Do you have firefox installed on your system?')
                ff=input()
                if ff=='n' or ff=='N' or ff== 'no' or ff=='No':
                    print('Do You have Google Chrome installed on your system?(y/n)')
                    gchome=input()
                    if gchome == 'y' or gchome == 'Y' or gchome == 'Yes' or gchome == 'yes':
                        browser='chrome'
                    elif gchome == 'n' or gchome =='N' or gchome =='No' or gchome =='no':
                        print('please install either google chrome or firefox to use this tool')
                    else:
                        print('Invalid Selection')
                elif ff =='y' or ff=='Y' or ff=='Yes' or ff=='yes':
                    browser='firefox'
        elif operating_system=='linux'or operating_system=='Linux' or operating_system=='linux2':
            browser='firefox'
        print('Please enter your ManyVids Username')
        username=input()
        print('Please enter your Manyvids password')
        password=getpass()
        print('Do You Have 2fa Enabled? (Y/N)')
        confirm=input()
        if confirm == "y" or confirm == 'Y' or confirm == 'yes' or confirm == 'Yes' or confirm =="YES":
            fa=True
        elif confirm=="no" or confirm=="No" or confirm=="N"or confirm == 'n':
            fa=False
        else:
            print('Invalid Selection, Please Restrart App')
            time.sleep(120)
            exit()
        char_set = string.ascii_uppercase + string.digits
        seed=''.join(random.sample(char_set*6, 6))
        print('Encrypting password, please wait')
        cipher = cryptocode.encrypt(password,seed)
        config = configparser.ConfigParser()
        config['MV_Settings'] = {'username':username,'hash': cipher,'seed':seed,'2fa':fa,'browser':browser}
        with open('MVSettings.ini', 'w') as configfile:
            config.write(configfile)
        if wdriver == 'n' or wdriver == 'N' or wdriver == 'no' or wdriver =='No' and browser == 'chrome' or browser=='firefox':
            cwd=os.getcwd()
            print('Getting Dependancies, Please Wait')
            get_browser()
            downloadpath=cwd+f'\\{browser}.zip'
            time.sleep(5)
            os.remove(downloadpath)
            print('Saving Config File, Please wait')
            time.sleep(5)
        
def get_config():
    config = configparser.ConfigParser()
    config.sections()
    config.read('MVSettings.ini')
    username = config['MV_Settings']['username']
    cipher = config['MV_Settings']['hash']
    seed = config['MV_Settings']['seed']
    fa = config['MV_Settings']['2fa']
    browser=config['MV_Settings']['browser']
    paswd=cryptocode.decrypt(cipher,seed)
    time.sleep(3)
    return username,paswd,fa,browser
def get_browser():
        config=get_config()
        browser=config[3]
        print(browser)
        if browser == 'chrome':
            downloadpath=os.getcwd()+'\\chrome.zip'
            print('downloading file')
            urllib.request.urlretrieve('https://chromedriver.storage.googleapis.com/100.0.4896.60/chromedriver_win32.zip',downloadpath)
            with zipfile.ZipFile(downloadpath,'r') as zip_ref:
                zip_ref.extractall(os.getcwd()+'\\')
        elif browser == 'firefox':
            downloadpath=os.getcwd()+'\\firefox.zip'
            urllib.request.urlretrieve('https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-win64.zip',downloadpath)
            with zipfile.ZipFile(downloadpath,'r') as zip_ref:
                zip_ref.extractall(os.getcwd()+'\\')
        print('unzip completed')
def get_sales():
    config=get_config()
    username=config[0]
    paswd=config[1]
    fa=config[2]
    browser=config[3]
    print('Browser is: ',browser)
    print(f'Logging in as {username}')
    print("Get sales for this month or previous?")
    print("Press 1 for this month")
    print("press 2 for previous month")
    print('peress 3 to export a custom month')
    year = date.today().strftime('%Y')
    userin=input()
    if int(userin) == 1:
        month=date.today().strftime('%b')
        print(f'Getting Sales for {month}')
    elif int(userin) == 2:
        prev_month=date.today().month - 1
        prev_month=months[prev_month-1]
        month=prev_month
        print(f'Getting sales for {prev_month}')
    elif int(userin) ==3:
        print("\nEnter the month you would like to export\n3 character format such as Jan, Feb,Mar etc.\nPlease ensure the first letter is capitalized")
        monthin=input()
        if monthin in months:
            month=monthin
    else:
        print('Invalid Selection, Please Restrart')
    if sys.platform != 'darwin':
        print('Show the browser?(Y/N) \nNOTE: Show browser must be Y when using 2fa')
        use_browser=input()
        if use_browser == 'y' or use_browser == 'Yes' or use_browser =='Y' or use_browser == 'yes':
            if browser=='firefox':
                headOption = webdriver.FirefoxOptions()
                headOption.headless=False
            elif browser =='chrome':
                from selenium.webdriver.chrome.options import Options
                options = Options()
        elif use_browser == 'n' or use_browser =='N' or use_browser =='No' or use_browser=='no':
            if browser == 'firefox':
                headOption = webdriver.FirefoxOptions()
                headOption.headless=True
            elif browser =='chrome':
                from selenium.webdriver.chrome.options import Options
                options = Options()
                options.add_argument('--headless')
                options.add_argument('--disable-gpu') 
            else:
                print("Invalid Selection, Please Restart")
                time.sleep(120)
                exit()
    print('Starting Browser, Please wait')
    if browser == 'firefox':
        bot = webdriver.Firefox(options=headOption,executable_path=path+'\\geckodriver.exe',service_log_path=path+'\\geckodriver.log')
    elif browser == 'chrome':
        bot = webdriver.Chrome(chrome_options=options,executable_path=path+'\\chromedriver.exe',service_log_path=path+'\\log.txt')
        bot.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    elif browser == 'safari':
        bot = webdriver.Safari(executable_path='/usr/bin/safaridriver')
    url=bot.get('https://www.manyvids.com/Login/')
    time.sleep(3)
    print('waiting for login page to load')
    email= bot.find_element(By.ID,'triggerUsername')
    password = bot.find_element(By.ID,'triggerPassword')
    email.clear()
    password.clear()
    email.send_keys(username)
    password.send_keys(paswd)
    if fa == True:
        print('Please enter your 2fa code on the Manyvids website and press any key to continue')
        resume=input()
    else:
        password.send_keys(Keys.RETURN)
    print('Waiting for page to load')
    time.sleep(3)
    url='https://manyvids.com/View-my-earnings/#recentSalesBody'
    bot.get(url)
    time.sleep(3)
    if bot.find_element(By.CLASS_NAME,value='js-cancel-announcement'):
        bot.find_element(By.CLASS_NAME,value='js-cancel-announcement').click()
    else:
        print('No Banner Found')
    
    while url != url:
        bot.get(url)
    print(f'Collecting Sales Data For {month}')
    sales=[]
    print('should be opening for loop')
    for row in bot.find_elements(by=By.XPATH,value='//tr[contains(@id,"earnings_video_")]'):
        cells= row.find_elements(by=By.CSS_SELECTOR,value='td')
        links = cells[1].get_attribute('innerHTML')              
        username = links[links.find("<b>")+3:links.find("</b>")]
        pm = links[links.find('<a href="/Inbox/New')+9:links.find('" class')]
        sale = cells[0].text.strip()
        s=sale.replace(' at','')
        sale_date=s.replace(',','')
        sale_date=sale_date[:11]
        sdate=sale_date.strip()
        purchase = cells[3].text.encode("ascii", "ignore").decode()
        purchased=purchase.replace('Read review','')
        bought=purchased.replace('\n','')
        promocode=cells[4].text
        amount=cells[5].text.strip('$')
        amount=float(amount)
        fields=['Sale Date','Purchase Amount','Promo Code','Purchased Item','Customer Name']
        sales_data=(sdate,amount,promocode,bought,username)
        if month in sdate and year in sdate:
            print(f'month {month} found in sdate {sdate}')
            sales_data=(sdate,amount,promocode,bought,username)
            sales.append(sales_data)
    print(len(sales), 'sales in list')
    with open(f'{month}_MV_Sales.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        i=0
        for s in sales:
            write.writerows(sales)
            i+=1
    print('Sale Export Complete.')
def welcome():
    print('##################################################################################')
    print('#                                                                                #')
    print('#                              Welcome To MV_Sales2CSV                           #')
    print('#                                                                                #')
    print('#                  If you find this program useful, please consider              #')
    print('#                           Tipping me on ManyVids                               #')
    print('#                           KingMarti.Manyvids.com                               #')
    print('#                                                                                #')
    print('################################################################################## \n\n')
if __name__=='__main__':
    welcome()
    set_config()
    get_sales()