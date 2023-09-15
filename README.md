# Apple Gift Card Purchase Automation

## 简介

这个项目是一个使用 Playwright 进行自动化的 Python 脚本，主要用于自动购买 Apple 礼品卡。

## 安装指南

### 环境需求

- Python 3.x
- Playwright

### 安装步骤

1. 克隆这个仓库到本地：
    ```bash
    git clone https://github.com/your_username/apple-gift-card-automation.git
    ```

2. 进入项目目录：
    ```bash
    cd apple-gift-card-automation
    ```

3. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```

## 依赖说明

- `Playwright`: 用于模拟浏览器操作。
- `json`: 用于处理 JSON 格式的配置文件。
- `logging`: 用于日志记录。

## 配置指南

配置文件模板位于 `config-template.json`。请确保填写以下字段：

- `toName`: 收件人姓名
- `toEmail`: 收件人邮箱
- `fromName`: 发件人姓名
- `fromEmail`: 发件人邮箱

## 使用示例

在配置好 `config-template.json` 文件后，另存为`config.json`并运行以下命令以启动脚本：

```bash
python test.py
```

## 常见问题与解决方案

- 如果遇到超时问题，尝试增加超时时间。
- 确保所有依赖都已经安装。

## 联系方式

如果您有任何问题或建议，请联系：
- 邮箱：ztm0929@icloud.com

## 许可证信息

本项目遵循 MIT 许可证。请查阅附带的 `LICENSE` 文件以获取更多信息。
