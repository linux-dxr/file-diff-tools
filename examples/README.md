# 示例数据说明

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
