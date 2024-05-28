# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time


# driver = webdriver.Chrome('')
# url = 'https://rt.molit.go.kr/pt/xls/xls.do?mobileAt='

# driver.get(url)
# time.sleep(3)

# driver.switch_to.window(driver.window_handles[0])
# driver.find_element(
#     By.XPATH, value='/html/body/div/div[2]/div/section/div/form/div[2]/div[1]/ul/li[3]/a').click()  # li[4]<숫자만 바꾸면 아파트>오피스텔 이런식으로 바꿀수있음
# for j in range(2021, 2024):
#     driver.find_element(
#         By.XPATH, value='/html/body/div/div[2]/div/section/div/form/div[2]/div[2]/div[1]/div[1]/ul/li/input').click()
#     driver.find_element(
#         By.XPATH, value='/html/body/div/div[2]/div/section/div/form/div[2]/div[2]/div[1]/div[1]/ul/li/input').send_keys(f'{j}0101')
#     driver.find_element(
#         By.XPATH, value='/html/body/div/div[2]/div/section/div/form/div[2]/div[2]/div[1]/div[2]/ul/li/input').click()
#     driver.find_element(
#         By.XPATH, value='/html/body/div/div[2]/div/section/div/form/div[2]/div[2]/div[1]/div[2]/ul/li/input').send_keys(f'{j}1231')
#     for i in range(2, 19):
#         select_xpath = f'/html/body/div/div[2]/div/section/div/form/div[2]/div[2]/div[2]/div[2]/ul/li/select/option[{i}]'
#         driver.find_element(By.XPATH, value=select_xpath).click()
#         driver.find_element(
#             By.XPATH, value='/html/body/div/div[2]/div/section/div/form/div[2]/div[2]/div[6]/button[2]').click()
#         time.sleep(3)
#     time.sleep(3)

# driver.close()


from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome('')
url = 'https://rt.molit.go.kr/pt/xls/xls.do?mobileAt='

driver.get(url)
driver.switch_to.window(driver.window_handles[0])
driver.find_element(
    By.XPATH, value='/html/body/div/div[2]/div/section/div/form/div[2]/div[1]/ul/li[3]/a').click()
driver.find_element(
    By.XPATH, value='/html/body/div/div[2]/div/section/div/form/div[2]/div[2]/div[1]/div[1]/ul/li/input').click()
driver.find_element(
    By.XPATH, value='/html/body/div/div[2]/div/section/div/form/div[2]/div[2]/div[1]/div[1]/ul/li/input').send_keys(20240101)
driver.find_element(
    By.XPATH, value='/html/body/div/div[2]/div/section/div/form/div[2]/div[2]/div[1]/div[2]/ul/li/input').click()
driver.find_element(
    By.XPATH, value='/html/body/div/div[2]/div/section/div/form/div[2]/div[2]/div[1]/div[2]/ul/li/input').send_keys(20240520)
for i in range(2, 19):
    select_xpath = f'/html/body/div/div[2]/div/section/div/form/div[2]/div[2]/div[2]/div[2]/ul/li/select/option[{i}]'
    driver.find_element(By.XPATH, value=select_xpath).click()
    driver.find_element(
        By.XPATH, value='/html/body/div/div[2]/div/section/div/form/div[2]/div[2]/div[6]/button[2]').click()
    time.sleep(5)
time.sleep(5)
driver.close()
