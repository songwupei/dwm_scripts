import unittest
from unittest.mock import MagicMock, patch
from get_financial_companies import go_to_next_page
import logging
import time

class TestGoToNextPage(unittest.TestCase):
    def setUp(self):
        # 配置日志
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        
        # 创建模拟的driver对象
        self.driver = MagicMock()
        
    @patch('selenium.webdriver.support.ui.WebDriverWait')
    def test_successful_page_turn(self, mock_wait):
        """测试成功翻页"""
        # 模拟下一页按钮
        mock_button = MagicMock()
        mock_button.get_attribute.return_value = ''
        
        # 配置WebDriverWait返回值
        mock_wait.return_value.until.return_value = mock_button
        
        # 执行测试
        result = go_to_next_page(self.driver)
        
        # 验证结果
        self.assertTrue(result)
        mock_button.click.assert_called_once()
        self.driver.find_element.assert_not_called()
        
    @patch('selenium.webdriver.support.ui.WebDriverWait')    
    def test_last_page(self, mock_wait):
        """测试到达最后一页"""
        # 模拟禁用状态的下一页按钮
        mock_button = MagicMock()
        mock_button.get_attribute.return_value = 'disabled'
        
        # 配置WebDriverWait返回值
        mock_wait.return_value.until.return_value = mock_button
        
        # 执行测试
        result = go_to_next_page(self.driver)
        
        # 验证结果
        self.assertFalse(result)
        mock_button.click.assert_not_called()
        
    @patch('selenium.webdriver.support.ui.WebDriverWait')
    def test_failed_page_turn_with_retries(self, mock_wait):
        """测试翻页失败并重试"""
        # 模拟元素查找失败
        mock_wait.return_value.until.side_effect = Exception('Element not found')
        
        # 执行测试
        start_time = time.time()
        result = go_to_next_page(self.driver)
        elapsed_time = time.time() - start_time
        
        # 验证结果
        self.assertFalse(result)
        self.assertGreaterEqual(elapsed_time, 10)  # 至少等待了重试时间
        self.assertEqual(mock_wait.return_value.until.call_count, 3)  # 重试3次
        
    @patch('selenium.webdriver.support.ui.WebDriverWait')
    def test_page_load_timeout(self, mock_wait):
        """测试页面加载超时"""
        # 模拟按钮点击后页面加载超时
        mock_button = MagicMock()
        mock_wait.return_value.until.side_effect = [
            mock_button,  # 第一次找到按钮
            Exception('Timeout')  # 第二次等待页面加载超时
        ]
        
        # 执行测试
        result = go_to_next_page(self.driver)
        
        # 验证结果
        self.assertFalse(result)
        mock_button.click.assert_called_once()

if __name__ == '__main__':
    unittest.main()