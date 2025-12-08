# 贡献指南

感谢您对文件差异比较工具的关注！我们欢迎各种形式的贡献，包括但不限于：

- 报告错误
- 提出新功能建议
- 提交代码改进
- 完善文档
- 分享使用经验

## 开发环境设置

1. **Fork 项目**
   ```bash
   # 在GitHub上Fork项目，然后克隆到本地
   git clone https://github.com/your-username/file-diff-tools.git
   cd file-diff-tools
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **运行测试**
   ```bash
   python test.py
   ```

## 代码贡献流程

1. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **进行开发**
   - 遵循现有代码风格
   - 添加必要的注释
   - 确保代码通过测试

3. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

4. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **创建Pull Request**
   - 在GitHub上创建Pull Request
   - 填写详细的PR描述
   - 等待代码审查

## 代码规范

- 使用PEP 8作为Python代码风格指南
- 函数和类应有文档字符串
- 变量和函数名使用小写字母和下划线
- 类名使用驼峰命名法
- 常量使用大写字母和下划线

## 提交信息规范

使用以下格式作为提交信息：

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

类型包括：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(gui): 添加文件拖放功能

- 支持从文件管理器拖放文件到应用窗口
- 自动识别文件类型并填充相应输入框

Closes #123
```

## 问题报告

使用GitHub Issues报告问题时，请提供以下信息：

1. **问题描述**
   - 清晰描述遇到的问题
   - 提供重现步骤
   - 描述期望行为和实际行为

2. **环境信息**
   - 操作系统
   - Python版本
   - 相关依赖版本

3. **附加信息**
   - 错误截图（如有）
   - 相关日志文件
   - 最小可重现示例

## 功能请求

提出新功能建议时，请考虑：

1. **功能描述**
   - 清晰描述功能需求
   - 说明使用场景
   - 描述预期效果

2. **实现建议**
   - 如有想法，可提供实现方案
   - 考虑与现有功能的兼容性

## 文档贡献

文档是项目的重要组成部分，欢迎以下贡献：

- 改进README.md
- 添加使用示例
- 翻译文档
- 创建教程

## 发布流程

项目维护者负责版本发布，流程如下：

1. 更新版本号
2. 更新CHANGELOG.md
3. 创建Git标签
4. 构建发布包
5. 发布到GitHub Releases

## 行为准则

请遵循以下行为准则：

- 尊重所有参与者
- 保持友好和专业
- 接受建设性反馈
- 专注于对社区最有利的事情

## 联系方式

如有疑问，可通过以下方式联系：

- 创建GitHub Issue
- 发送邮件至项目维护者

感谢您的贡献！