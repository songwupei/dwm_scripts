from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def go_to_next_page(driver):
    """
    尝试翻到下一页
    """
    # 使用XPath定位下一页按钮，更稳定
    next_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x-tbar-page-next')]"))
    )
    
    if 'disabled' in next_button.get_attribute('class'):
        logger.info("已到达最后一页")
        return False
        
    logger.info("点击下一页按钮")
    next_button.click()
    
    # 等待下一页加载完成
    WebDriverWait(driver, 10).until(
        EC.staleness_of(next_button)
    )
    
    # 额外等待以确保数据加载完成
    time.sleep(2)
    return True
            

# 使用系统安装的geckodriver
service = Service('/usr/bin/geckodriver')

# 设置Firefox选项（有头模式）
options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(service=service, options=options)


def scrape_page():
    # 等待表格加载
    # 获取表格标题
 
    table_header = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'ext-gen12'))
    )
    
    # 获取表格内容
    table_body = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, 'ext-gen13'))
    )
    
    # 提取数据
    companies = []
    try:
        # 等待表格内容加载
        WebDriverWait(driver, 300).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.x-grid3-row'))
        )
        
        rows = driver.find_elements(By.CSS_SELECTOR, 'div.x-grid3-row')
        if not rows:
            logger.warning("未找到任何数据行")
            return companies
            
        for row in rows:
            try:
                # 获取公司名称（第4列）
                company_name = row.find_element(
                    By.CSS_SELECTOR, 'td.x-grid3-td-4 div.x-grid3-cell-inner'
                ).text.strip()
                
                # 获取机构编号（第2列）
                company_code = row.find_element(
                    By.CSS_SELECTOR, 'td.x-grid3-td-2 div.x-grid3-cell-inner'
                ).text.strip()
                
                # 获取流水号（第3列）
                serial_number = row.find_element(
                    By.CSS_SELECTOR, 'td.x-grid3-td-3 div.x-grid3-cell-inner'
                ).text.strip()
                
                # 获取批准日期（第6列）
                approval_date = row.find_element(
                    By.CSS_SELECTOR, 'td.x-grid3-td-6 div.x-grid3-cell-inner'
                ).text.strip()
                
                # 获取发证日期（第7列）
                issue_date = row.find_element(
                    By.CSS_SELECTOR, 'td.x-grid3-td-7 div.x-grid3-cell-inner'
                ).text.strip()
                
                # 获取机构类型（第5列）
                company_type = institution_type  # 直接使用当前选择的机构类型
                
                companies.append([company_name, company_type, company_code, approval_date, issue_date, serial_number])
            except Exception as e:
                logger.warning(f"无法提取行数据，错误：{str(e)}")
                continue
                
        if not companies:
            logger.warning("未提取到任何有效数据")
            logger.debug("当前页面HTML内容：")
            print(driver.page_source)
            
        return companies
        
    except Exception as e:
        logger.error(f"数据提取失败，原因：{str(e)}")
        logger.debug("当前页面HTML内容：")
        print(driver.page_source)
        return companies

try:
    # 访问目标URL
    driver.get('https://xkz.nfra.gov.cn/jr/')
    
    # 等待页面加载完成
    time.sleep(30)
    
    # 按下ESC键
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.ESCAPE)
    time.sleep(5)
    body.send_keys(Keys.ESCAPE)
    
    # 定义要选择的机构类型列表
    institution_types = ['财务公司']#, ]'开发性金融机构', '政策性银行', ]#'商业银行']
    
    # 遍历每种机构类型
    for institution_type in institution_types:
        # 点击图片打开下拉菜单
        trigger = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'ext-gen48'))
        )
        trigger.click()
        time.sleep(1)  # 等待下拉菜单展开
        
        # 选择当前机构类型
        option = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{institution_type}')]"))
        )
        option.click()
        
        # 点击查询按钮
        query_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'reportSearch'))
        )
        query_button.click()
        
        # 等待数据加载并避免频繁查询
        logger.info(f"正在处理 {institution_type} 数据，请稍候...")
        for i in range(10):  # 10秒倒计时
            logger.info(f"剩余等待时间: {10 - i}秒")
            time.sleep(1)
        logger.info("继续处理...")
    
        # 点击查询按钮
        query_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, 'reportSearch'))
        )
        query_button.click()
        
        # 等待数据加载并检查页面状态
        logger.info("正在等待数据加载...")
        try:
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.x-grid3-row'))
            )
            logger.info("数据加载完成")
            
            # 打印表格内容进行调试
            table_html = driver.find_element(By.CSS_SELECTOR, 'div.x-grid3-body').get_attribute('innerHTML')
            logger.debug("表格内容：")
            print(table_html)
            
        except Exception as e:
            logger.error(f"数据加载失败: {str(e)}")
            logger.debug("当前页面HTML内容：")
            print(driver.page_source)
            continue
        
        # 初始化结果列表和页码计数器
        all_companies = []
        page_count = 0
        
        while True:
            # 获取当前页数据
            companies = scrape_page()
            all_companies.extend(companies)
            
            # 每10页暂停2分钟
            if page_count % 10 == 0 and page_count > 0:
                logger.info(f"已读取{page_count}页，暂停2分钟...")
                time.sleep(120)
            
            # 尝试翻页
            if not go_to_next_page(driver):
                break
            time.sleep(20)
                
            page_count += 1
        
        # 按批准日期升序排序
        all_companies.sort(key=lambda x: x[3])
        
        # 保存数据到CSV文件
        try:
            filename = f'{institution_type}.csv'
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['公司名称', '机构类型','机构编号','批准日期','发证日期','流水号'])
                writer.writerows(all_companies)
            logger.info(f"成功保存{len(all_companies)}家金融机构信息到{filename}")
        except Exception as e:
            logger.error(f"保存文件时发生错误: {str(e)}")

finally:
    # 关闭浏览器
    driver.quit()