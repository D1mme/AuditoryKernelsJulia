from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "/home/dimme/DelftBlueScratch/CommonVoice20/"}
options.add_experimental_option("prefs", prefs)

browser = webdriver.Chrome(options=options)
browser.maximize_window()
browser.get('https://commonvoice.mozilla.org/en/datasets')

sleep(3)



el = browser.find_element(By.XPATH,"/html/body/div/div[3]/main/div/div/div[1]/div[1]/div[2]/div/div[2]/label/div/select")

# e = browser.find_element(By.XPATH, "//*[@id="content"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/table/tbody/tr[2]/td[1]")

select = Select(el)

#posible_values = [o.text for o in select.options]
posible_values = ['Abkhaz', 'Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Asturian', 'Azerbaijani', 'Basaa', 'Bashkir', 'Basque', 'Belarusian', 'Bengali', 'Breton', 'Bulgarian', 'Cantonese', 'Catalan', 'Central Kurdish', 'Chinese (China)', 'Chinese (Hong Kong)', 'Chinese (Taiwan)', 'Chuvash', 'Czech', 'Danish', 'Dhivehi', 'Dholuo', 'Dioula', 'Dutch', 'English', 'Erzya', 'Esperanto', 'Estonian', 'Finnish', 'French', 'Frisian', 'Galician', 'Georgian', 'German', 'Greek', 'Guarani', 'Haitian', 'Hakha Chin', 'Hausa', 'Hebrew', 'Hill Mari', 'Hindi', 'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Interlingua', 'Irish', 'IsiNdebele (South)', 'Italian', 'Japanese', 'Kabyle', 'Kalenjin', 'Kazakh', "Kidaw'ida", 'Kinyarwanda', 'Korean', 'Kurmanji Kurdish', 'Kyrgyz', 'Lao', 'Latgalian', 'Latvian', 'Ligurian', 'Lithuanian', 'Luganda', 'Macedonian', 'Malayalam', 'Maltese', 'Marathi', 'Meadow Mari', 'Moksha', 'Mongolian', 'Nepali', 'Northern Sotho', 'Norwegian Nynorsk', 'Occitan', 'Odia', 'Ossetian', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Quechua Chanka', 'Romanian', 'Romansh Sursilvan', 'Romansh Vallader', 'Russian', 'Sakha', 'Santali (Ol Chiki)', 'Saraiki', 'Sardinian', 'Serbian', 'Setswana', 'Sindhi', 'Slovak', 'Slovenian', 'Sorbian, Upper', 'Southern Sotho', 'Spanish', 'Swahili', 'Swedish', 'Taiwanese (Minnan)', 'Tamazight', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tigre', 'Tigrinya', 'Toki Pona', 'Turkish', 'Turkmen', 'Twi', 'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Votic', 'Welsh', 'Western Sierra Puebla Nahuatl', 'Xhosa', 'Xitsonga', 'Yiddish', 'Yoruba', 'Zaza', 'Zulu']

#posible_values = ['Zulu']


print(len(posible_values))
"""
sleep(120)
f = 1
N = 0
for i in posible_values[:N]:
    print("skipping ", i)
sleep(12)    
"""
for i in posible_values:
    print("Downloading ", i)
    try:
        
        select.select_by_visible_text(i)

        sleep(1)

        text_to_find = "Common Voice Corpus 20.0"

        corp = browser.find_element(By.XPATH, f"//td[contains(text(), '{text_to_find}')]")
        par = corp.find_element(By.XPATH, "..")

        sleep(1)

        # browser.execute_script("arguments[0].click();", par)
        browser.execute_script("console.log(arguments[0]);", corp)
        browser.execute_script("x = arguments[0];", corp)

        ActionChains(browser).scroll_by_amount(0,300).perform()

        sleep(1)

        browser.execute_script('x.scrollIntoView({"block":"center"});')
        
        sleep(1)

        browser.execute_script("x.click();")


        sleep(2)

        if f:
            f = 0
            

            mail = browser.find_element(By.XPATH, '//*[@id="content"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[1]/label[1]/input')
            mail.send_keys("test@test.nl")

            selector1 = browser.find_element(By.XPATH, '//*[@id="content"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[1]/label[2]/span[1]/input')
            selector1.click()
            selector2 = browser.find_element(By.XPATH, '//*[@id="content"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[1]/label[3]/span[1]/input')
            selector2.click()

            
        
        # else:
        #     mail = browser.find_element(By.XPATH, '//*[@id="content"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[1]/label[1]/input')
        #     mail.send_keys(" ")

        download_btn = browser.find_element(By.XPATH, '//*[@id="content"]/div/div/div[1]/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/div[1]/a')
        download_btn.click()

        sleep(3)

        x_button = browser.find_element(By.XPATH, '/html/body/div[4]/div/div/div/button/img')
        x_button.click()
    
    except Exception as e:
        print(e)
        print("exception in ", i)
    sleep(3)
    

while 1:
    pass

