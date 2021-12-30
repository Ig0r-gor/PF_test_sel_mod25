# content of file conftest.py

import pytest
import uuid


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
    # chrome_options.add_extension('C:\Program Files\Google\Chrome\Application\extension.crx')
    # chrome_options.add_argument('--kiosk')
    return chrome_options


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def web_browser(request, selenium):
    browser = selenium
    browser.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield browser

    # Do teardown (this code will be executed after each test):

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            browser.save_screenshot('screen' + str(uuid.uuid4()) + '.png')
            # browser.save_screenshot('result_1111.png')

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass  # just ignore any errors here

# дописано из множественного: выключить для других
# @pytest.fixture(autouse=True)
# def testing():
#    pytest.driver = webdriver.Chrome('E:\sedrv\chromedriver.exe')
#    # Переходим на страницу авторизации
#    pytest.driver.get('http://petfriends1.herokuapp.com/login')
#
#    yield
#
#    pytest.driver.quit()
