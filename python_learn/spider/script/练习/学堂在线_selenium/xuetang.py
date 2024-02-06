import logging
import os
import re
from tqdm import tqdm
import csv
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# 配置日志记录
# logging.basicConfig(
#     filename="test.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     encoding="utf-8",
# )
# 创建logger对象
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# 创建FileHandler，设置编码为UTF-8
file_handler = logging.FileHandler("test.log", encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

# 将FileHandler添加到logger
logger.addHandler(file_handler)


###################
# 隐藏由测试工具控制#
###################
# 创建Chrome参数对象
options = webdriver.ChromeOptions()
# 添加试验性参数
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
# 创建Chrome浏览器对象并传入参数
browser = webdriver.Chrome(options=options)
# 执行Chrome开发者协议命令（在加载页面时执行指定的JavaScript代码）
browser.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {"source": 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'},
)

# browser = webdriver.Chrome()#选择用chrome还是edge
# browser = webdriver.Edge()
School_List = {}
DOWNLOAD_PATH = "images"
if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)


def SaveMessage(browser, Schools_Infos):
    for school in Schools_Infos:
        school_name = school.find_element(By.CLASS_NAME, "name_cn").text
        school_class_count = school.find_element(By.CLASS_NAME, "count").text
        style_attribute = school.find_element(By.CLASS_NAME, "logo").get_attribute(
            "style"
        )
        logo_url_match = re.search(r'url\("([^"]+)"\)', style_attribute)
        logo_url = logo_url_match.group(1) if logo_url_match else "No logo found"
        ##motto被隐藏使用ActionChains执行悬停操作
        ActionChains(browser).move_to_element(school).perform()
        # 等待悬停后的元素（如motto）出现
        # 注意：这里的选择器".remark > span"需要根据实际情况调整
        try:
            WebDriverWait(school, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".remark > span"))
            )
            school_motto = school.find_element(By.CSS_SELECTOR, ".remark > span").text
        except:
            school_motto = "Nothing"
            logging.warning(f"{school_name} dose not have motto!!")
            # print("Motto not found for this school, moving to the next.")

        ##保存school logo
        try:
            # 处理学校名称，确保其作为文件名是有效的
            safe_school_name = re.sub(r'[\\/*?:"<>|]', "", school_name)
            file_path = os.path.join(DOWNLOAD_PATH, safe_school_name + ".png")
            # 发送请求下载图像
            response = requests.get(logo_url)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    file.write(response.content)
                logging.info(f"Logo for {school_name} saved successfully.")
                # print(f"Logo for {school_name} saved successfully.")
            else:
                logging.warning(f"Failed to download logo for {school_name}.")
                # print(f"Failed to download logo for {school_name}.")
        except Exception as e:
            logging.warning(f"Error downloading logo for {school_name}: {e}")
            # print(f"Error downloading logo for {school_name}: {e}")
        # print(school_name)
        # print(school_motto)
        # print(logo_url)
        School_List[school_name] = {
            "Course_count": school_class_count,
            "Motto": school_motto,
            "Logo_url": logo_url,
        }


def SaveToCSV(School_List):
    with open("Schools_Info.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["School Name", "Course Count", "Motto", "Logo Path"])
        for school, info in School_List.items():
            writer.writerow(
                [school, info["Course_count"], info["Motto"], info["Logo_url"]]
            )


def getHTML(url, maxpage):
    try:
        currentpage = 1
        browser.get(url)
        while currentpage <= maxpage:
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "school"))
            )
            # 使用f-string格式化日志消息
            logging.info(f"Climbing page {currentpage},all {maxpage} pages")
            print(f"Climbing page {currentpage},all {maxpage} pages")
            Schools_Infos = browser.find_elements(By.CLASS_NAME, "school")
            SaveMessage(browser, Schools_Infos)
            # 尝试点击下一页
            try:
                next_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-next"))
                )
                next_button.click()
                currentpage += 1
            except Exception as e:
                logging.error("No more pages or error occurred: %s", e)
                break
    finally:
        browser.quit()
        SaveToCSV(School_List)
        logging.info("Data saved to CSV.")


def main():
    maxpage = 1
    url = "https://www.xuetangx.com/university/all"
    getHTML(url, maxpage)


if __name__ == "__main__":
    main()
