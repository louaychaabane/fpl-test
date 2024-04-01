from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
from flask import Flask, jsonify
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

@app.route('/')
def index():
    start_time = time.time()
    driver = webdriver.Firefox()

    my_list = []

    # Function to append strings to the list only if they are not already present
    def append_unique(string):
        if string not in my_list:
            my_list.append(string)

    ids = ['823558', '399058', '1296012']
    result = []
    j=0
    for id in ids:
        j=j+1

        my_list.clear()
        # Construct URL with the current ID
        url = f'https://fantasy.premierleague.com/entry/{id}/transfers'

        # Open URL in the browser
        driver.get(url)

        # Add necessary waiting time if required for the page to load

        # Example: Waiting for 5 seconds
        time.sleep(8)
        try:
            name = driver.find_element(By.CLASS_NAME, 'cMEsev')

            table = driver.find_element(By.CLASS_NAME,'dUELIG')
            tbody = table.find_element(By.TAG_NAME,'tbody')
            rows = tbody.find_elements(By.TAG_NAME,'td')
            date = rows[0]

            i=0
            while(i<len(rows)):
                # print(rows[i+3].text)
                append_unique(rows[i+3].text)
                i=i+4
            l=len(my_list)
            m = int(my_list[-1][2:])

            result.append(f'{j} - {name.text} | {date.text} | {my_list[-1]} | {30 - m - l}')
        except:
            result.append(f'ID: {id}, Element not found')

    driver.quit()
    end_time = time.time()
    execution_time = end_time - start_time
    result.append(f'Execution time: {execution_time} seconds')

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)