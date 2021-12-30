from selenium import webdriver
import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('E:\sedrv\chromedriver.exe')
   # Переходим на страницу авторизации

   pytest.driver.implicitly_wait(10)

   pytest.driver.get('http://petfriends1.herokuapp.com/login')
   pytest.driver.set_window_size(1500, 1000)

   yield

   pytest.driver.quit()


def test_show_my_pets():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('igor@email.com')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('orange')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   # assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"


   pytest.driver.find_element_by_css_selector('.nav-link[href="/my_pets"]').click()

   assert pytest.driver.current_url == 'http://petfriends1.herokuapp.com/my_pets'
   # assert pytest.driver.find_element_by_tag_name('h2').text == "igor-gor"
#    второй способ проверки по заранее известному имени пользователя


   images = pytest.driver.find_elements_by_css_selector('tbody img')
   matrix_of_props = pytest.driver.find_elements_by_xpath('//tr/td[not (@class)]')

   # создание списков имен, пород и возраста:
   names = matrix_of_props[0::3]
   species = matrix_of_props[1::3]
   ages = matrix_of_props[2::3]


   # num_of_pets = pytest.driver.find_elements_by_xpath('//div[@class=".col-sm-4 left"][contains(text(), ”Питомцев”)]')
   # выше указанный не работает. получаем text object, а должен быть element. через contains тоже не нашел

   num_of_pets = len(images)
   # статистику получаем из кол-ва строк

   halfpart = num_of_pets // 2

   # словари текстовых значений:
   names_t = []
   species_t = []
   ages_t = []

   # счетчик загруженный фотографий:
   have_pic = 0

   for i in range(num_of_pets):
      # assert images[i].get_attribute('src') != ''
      if images[i].get_attribute('src') != '':
         have_pic =+1
      assert names[i].text != ''
      # у всех питомцев есть имя
      names_t.append(names[i].text)
      assert species[i].text != ''
      # у всех питомцев есть порода
      species_t.append(species[i].text)
      assert ages[i].text != ''
      # у всех питомцев есть возраст
      ages_t.append(ages[i].text)


   # проверка одинаковых питомцев:
   pair = 0
   for i in range(halfpart+1):
       for j in range(num_of_pets-1, i, -1):
           if names_t[i] == names_t[j]:
               if species_t[i] == species_t[j]:
                   if ages_t[i] == ages_t[j]:
                       pair += 1

   assert have_pic >= halfpart
   #проверка что более половины имеют фото

   assert len(set(names_t)) == len(names_t)
   # проверка что все имена разные

   assert pair == 0
   # проверка одинаковых питомцев