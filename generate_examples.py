#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
示例数据生成脚本
用于创建用于测试文件差异比较功能的示例Excel文件
"""

import pandas as pd
import os
import random
from datetime import datetime, timedelta

def generate_sample_data():
    """生成示例数据"""
    
    # 创建示例数据目录
    examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples")
    if not os.path.exists(examples_dir):
        os.makedirs(examples_dir)
    
    # 示例数据1: 员工信息表
    employees_data = {
        '员工ID': [f'EMP{1000+i}' for i in range(1, 21)],
        '姓名': [f'员工{i}' for i in range(1, 21)],
        '部门': ['技术部', '市场部', '财务部', '人事部'] * 5,
        '职位': ['工程师', '经理', '专员', '主管'] * 5,
        '入职日期': [
            (datetime.now() - timedelta(days=random.randint(30, 1000))).strftime('%Y-%m-%d')
            for _ in range(20)
        ],
        '薪资': [random.randint(5000, 20000) for _ in range(20)]
    }
    
    # 创建原始员工表
    employees_df = pd.DataFrame(employees_data)
    employees_df.to_excel(os.path.join(examples_dir, 'employees_original.xlsx'), index=False)
    
    # 创建修改后的员工表
    modified_employees = employees_df.copy()
    # 修改一些数据
    modified_employees.loc[0, '薪资'] = 12000  # 修改薪资
    modified_employees.loc[5, '部门'] = '研发部'  # 修改部门
    modified_employees.loc[10, '职位'] = '高级工程师'  # 修改职位
    # 添加一行新数据
    new_employee = {
        '员工ID': 'EMP1021',
        '姓名': '新员工',
        '部门': '技术部',
        '职位': '实习生',
        '入职日期': datetime.now().strftime('%Y-%m-%d'),
        '薪资': 4000
    }
    modified_employees = pd.concat([modified_employees, pd.DataFrame([new_employee])], ignore_index=True)
    # 删除一行数据
    modified_employees = modified_employees.drop(15).reset_index(drop=True)
    
    modified_employees.to_excel(os.path.join(examples_dir, 'employees_modified.xlsx'), index=False)
    
    # 示例数据2: 产品销售表
    products_data = {
        '产品ID': [f'PRD{2000+i}' for i in range(1, 16)],
        '产品名称': [f'产品{i}' for i in range(1, 16)],
        '类别': ['电子产品', '家居用品', '服装', '食品', '图书'] * 3,
        '单价': [random.randint(50, 500) for _ in range(15)],
        '库存量': [random.randint(10, 100) for _ in range(15)],
        '供应商': ['供应商A', '供应商B', '供应商C'] * 5
    }
    
    # 创建原始产品表
    products_df = pd.DataFrame(products_data)
    products_df.to_excel(os.path.join(examples_dir, 'products_original.xlsx'), index=False)
    
    # 创建修改后的产品表
    modified_products = products_df.copy()
    # 修改一些数据
    modified_products.loc[2, '单价'] = 299  # 修改单价
    modified_products.loc[7, '库存量'] = 50  # 修改库存
    modified_products.loc[12, '供应商'] = '供应商D'  # 修改供应商
    # 添加一行新数据
    new_product = {
        '产品ID': 'PRD2016',
        '产品名称': '新产品',
        '类别': '电子产品',
        '单价': 399,
        '库存量': 30,
        '供应商': '供应商E'
    }
    modified_products = pd.concat([modified_products, pd.DataFrame([new_product])], ignore_index=True)
    # 删除一行数据
    modified_products = modified_products.drop(8).reset_index(drop=True)
    
    modified_products.to_excel(os.path.join(examples_dir, 'products_modified.xlsx'), index=False)
    
    # 创建说明文件
    readme_content = """# 示例数据说明

本目录包含了用于测试文件差异比较功能的示例Excel文件。

## 文件列表

1. **employees_original.xlsx** - 原始员工信息表
2. **employees_modified.xlsx** - 修改后的员工信息表
3. **products_original.xlsx** - 原始产品销售表
4. **products_modified.xlsx** - 修改后的产品销售表

## 数据差异说明

### 员工信息表差异
- 修改了员工ID为EMP1001的薪资
- 修改了员工ID为EMP1006的部门
- 修改了员工ID为EMP1011的职位
- 添加了新员工EMP1021
- 删除了员工ID为EMP1016

### 产品销售表差异
- 修改了产品ID为PRD2003的单价
- 修改了产品ID为PRD2008的库存量
- 修改了产品ID为PRD2013的供应商
- 添加了新产品PRD2016
- 删除了产品ID为PRD2009

## 使用方法

1. 启动文件差异比较工具
2. 选择对应的原始文件和修改后的文件
3. 点击"比较"按钮查看差异结果
4. 可以将结果导出为CSV文件

## 生成脚本

这些示例数据是通过 `generate_examples.py` 脚本自动生成的。如需重新生成，可以运行：

```
python generate_examples.py
```
"""
    
    with open(os.path.join(examples_dir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("示例数据已生成到 examples 目录:")
    print("- employees_original.xlsx")
    print("- employees_modified.xlsx")
    print("- products_original.xlsx")
    print("- products_modified.xlsx")
    print("- README.md")

if __name__ == "__main__":
    generate_sample_data()