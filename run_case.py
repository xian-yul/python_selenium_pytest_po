import os

import pytest

case_path = os.path.join("Testcase")  # 测试集合路径
pytest.main([case_path, "-s"])  # 运行 test_case下所有测试用例
