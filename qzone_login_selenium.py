from config import config, AUTO_UPDATE_USER, AUTO_UPDATE_PASS
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def update_cookies(headless=False):
    print("Updating cookies...")

    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--disable-extensions")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--incognito")
    options.add_argument("--disable-plugins-discovery")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")

    if headless:
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    driver.get("https://qzone.qq.com/")

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """
        },
    )

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login_frame"))
    )
    driver.switch_to.frame("login_frame")
    driver.find_element(By.ID, "switcher_plogin").click()

    driver.find_element(By.ID, "u").clear()
    driver.find_element(By.ID, "u").send_keys(AUTO_UPDATE_USER)
    driver.find_element(By.ID, "p").clear()
    driver.find_element(By.ID, "p").send_keys(AUTO_UPDATE_PASS)

    driver.execute_script(
        "document.getElementById('login_button').parentNode.hidefocus=false;"
    )

    driver.find_element(By.XPATH, '//*[@id="loginform"]/div[@class="submit"]/a').click()
    driver.find_element(By.ID, "login_button").click()

    try:
        WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))
    except TimeoutException:
        print("login timeout")
        with open("login_timeout.html", "w") as f:
            f.write(driver.page_source)
        with open("login_timeout.png", "wb") as f:
            f.write(driver.get_screenshot_as_png())
        exit(1)

    try:
        WebDriverWait(driver, 10).until_not(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="mod_loading"]/img')
            )
        )
    except TimeoutException:
        print("page load timeout")
        with open("page_load_timeout.html", "w") as f:
            f.write(driver.page_source)
        with open("page_load_timeout.png", "wb") as f:
            f.write(driver.get_screenshot_as_png())

    config.set_cookies(
        "; ".join(
            [f"{cookie['name']}={cookie['value']}" for cookie in driver.get_cookies()]
        )
    )

    print("Cookies updated.")

    driver.quit()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    update_cookies(args.headless)
