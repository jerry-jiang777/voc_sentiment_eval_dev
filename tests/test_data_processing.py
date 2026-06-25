"""数据处理模块单元测试"""
import pytest
from pathlib import Path
from src.data_processing.get_origin_data import read_excel

def test_read_excel_not_exists():
    """测试读取不存在的文件"""
    with pytest.raises(FileNotFoundError):
        read_excel(Path("fake_file.xlsx"))