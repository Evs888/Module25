import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome("C:\Program Files\Google\Chrome\Application/chromedriver.exe")
def testing():

    pytest.driver.get('https://petfriends.skillfactory.ru/login')
    pytest.driver.find_element_by_id('email').send_keys('yayaya@ya.ru')
    pytest.driver.find_element_by_id('pass').send_keys('qwerty123')
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()

    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"

    yield

    pytest.driver.quit()


def test_show_my_pets():
    pytest.driver.find_element_by_id('email').send_keys('yayaya@ya.ru')
    pytest.driver.find_element_by_id('pass').send_keys('qwerty123')
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"


images = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
names = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')

for i in range(len(names)):
    assert images[i].get_attribute('src') != ''
    assert names[i].text != ''
    assert descriptions[i].text != ''
    assert ', ' in descriptions[i]
    parts = descriptions[i].text.split(", ")
    assert len(parts[0]) > 0
    assert len(parts[1]) > 0


def test_my_pets():
    pytest.driver.get('https://petfriends.skillfactory.ru/my_pets')
    pets_text = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]'))
    )

    assert 'Питомцев:' in pets_text.text

    pets_amount = int(pets_text.text.split('\n')[1].split(':')[1])
    rows = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH,
                                             '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr'))
    )
    rows_amount = len(rows)
    assert pets_amount == rows_amount
    rows = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH,
                                             '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr/th/img'))
    )
    photo_amount = 0
    for row in rows:
        if row.get_attribute('src') != '':
            photo_amount += 1

    assert photo_amount >= pets_amount / 2

    elements = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH,
                                             '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr/td'))
    )
    assert pets_amount * 4 == len(elements)
    data_filled = True
    for element in elements:
        text = element.text
        if text.isspace():
            data_filled = False
            break

    assert data_filled

    data_list = []
    rows = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH,
                                             '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr'))
    )
    for row in rows:
        cells = row.text.split()
        data = tuple([cells[0], cells[1], cells[2]])
        data_list.append(data)

    data_set = set(data_list)

    assert len(data_list) == len(data_set)

    name_list = []
    rows = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH,
                                             '//div[@id="all_my_pets"]/table[@class="table table-hover"]/tbody/tr'))
    )
    for row in rows:
        cells = row.text.split()
        name_list.append(cells[0])

    name_set = set(name_list)

    assert len(name_list) == len(name_set)

pytest.driver.quit()