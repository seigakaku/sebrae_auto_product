from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as Soup

import time
import os
import sys

#products_page = 'https://emissornfe.sebrae.com.br/Produtos_em_Estoque/ListaProdutos'
products_page = 'https://emissornfe.sebrae.com.br/Produtos_em_Estoque/CadastrarProdutoIndex'
cpf = '02982585871'
key = 'lQb&v_,hIVEXO?]k,qzf'

def login(driver, u, p):
    driver.get('https://emissornfe.sebrae.com.br')

    login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'kc-login')))

    username = driver.find_element(By.ID, 'username')
    password = driver.find_element(By.ID, 'password')

    username.send_keys(cpf)
    password.send_keys(key)

    login.click()

def open_product_registration(driver):
    time.sleep(7)
    driver.get(products_page)

    #driver.implicitly_wait(15)
    #register = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[2]/div[4]/button')
    #register.click()
    #driver.implicitly_wait(15)

def register_product(driver, xml):
    
    soup = Soup(xml, features="lxml")

    def try_tag_value(soup, tag):
        t = soup.find(tag.lower())
        if not t or not t.text:
            match tag:
                case 'orig':
                    return '0'
                case 'NCM':
                    return '00000000'
                case 'uCom':
                    return 'UN'
                case 'uTrib':
                    return 'UN'
                case _:
                    return None
        else:
            return str(t.text)

    def from_xml(soup, id, tag):
        elem = driver.find_element(By.ID, id)
        driver.execute_script("arguments[0].scrollIntoView(true);", elem);
        if not elem:
            return
        value = try_tag_value(soup, tag)
        if not value:
            return
        elem.send_keys(value)

    def select_from_xml(soup, id, tag):
        elem = driver.find_element(By.ID, id)
        driver.execute_script("arguments[0].scrollIntoView(true);", elem);
        elem = Select(elem)
        if not elem:
            return
        value = try_tag_value(soup, tag)
        if not value:
            return
        time.sleep(1)
        elem.select_by_value(value)

    from_xml(soup, 'codpro', 'cProd')
    from_xml(soup, 'Descri', 'xProd')
    from_xml(soup, 'Código_de_Barra', 'cEAN')
    from_xml(soup, 'NCM', 'NCM')

    select_from_xml(soup, 'Origem_do_Produto', 'orig')
    select_from_xml(soup, 'Unidade', 'uCom')
    select_from_xml(soup, 'Unidpara', 'uTrib')

    save = driver.find_element(By.XPATH, '/html/body/div[2]/div/main/div/div[3]/div/button[2]')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    save.click()
    time.sleep(3)

if __name__ == '__main__':
        
    service = Service("geckodriver")
    options = webdriver.FirefoxOptions()

    driver = webdriver.Firefox(service=service, options=options)

    login(driver, cpf, key)

    products_dir = './produtos'
    done_dir = './cadastrados'

    if not os.path.isdir(products_dir):
        print('Pasta de produtos a cadastrar nao existe.')
        sys.exit(1)

    if not os.path.isdir(done_dir):
        os.mkdir(done_dir)

    for file in os.listdir(products_dir):
        if not file.endswith('.xml'):
            continue

        actual_file = os.path.join(products_dir, file)
        done_file = os.path.join(done_dir, file)

        try:
            with open(actual_file) as f:
                xml = f.read()
                open_product_registration(driver)
                driver.implicitly_wait(10)
                register_product(driver, xml)
                os.rename(actual_file, done_file)
        except Exception as e:
            print(e)
            
            
        







    


    

