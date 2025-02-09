# tencentcloud-auto-tools
一切正在测试中，文中的参数fork到自己仓库修改即可
# TencentCloud CDN 自动化工具

## 📖 项目概述
腾讯云CDN缓存刷新自动化工具，支持通过API快速刷新指定路径下的缓存资源。适用于CI/CD流程集成，可配合GitHub Actions实现自动化部署后刷新。

## 🚀 快速开始

### 环境要求
- Python 3.6+
- 腾讯云账号（需配置SecretId/SecretKey）

### 🔧 安装方式
```bash
git clone https://github.com/yourname/tencentcloud-auto-tools
cd tencentcloud-auto-tools
```

### 🛠 参数配置表

| 参数 | 缩写  | 必填 | 默认值 | 说明 |
|--------------|-------|------|--------|------------------|
| --secret_id  | -id   | ✅   | 无 | 腾讯云账户SecretID |
| --secret_key | -key  | ✅   | 无 | 腾讯云账户SecretKey |
| --region | -r| ❌   | 空 | 服务区域代码   |
| --token  | -t| ❌   | 空 | 临时安全令牌   |

### 📝 脚本参数配置

修改 `tencentcloud_PurgePathCache.py` 第35行：

```python
payload = {
"Paths": ["https://yourdomain.com/"],  # 替换为你的域名
"FlushType": "flush", # 刷新类型
"UrlEncode": False,   # 中文编码处理
"Area": "mainland"# 加速区域配置
}
```

#### 刷新类型说明
- `flush`: 仅刷新更新资源
- `delete`: 强制刷新全部资源

#### 区域配置指南
| 区域值   | 覆盖范围 |
|----------|--------------|
| mainland | 中国大陆节点 |
| overseas | 海外节点 |
| (空值)   | 默认加速区域 |

### ⚡ 执行示例
```bash
python tencentcloud_PurgePathCache.py -id YOUR_ID -key YOUR_KEY
```

### 🤖 GitHub Actions 集成
### ⚠️ 请先fork到自己仓库修改必要的```payload ```信息再运行！
### ```SECRET_ID ```以及```SECRET_KEY ```在环境变量中设置
```yaml
name: 自动部署

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  install-and-run:
    runs-on: ubuntu-latest
    environment: tenx #这里是环境变量
    steps:

      - name: 执行刷新
        run: |
          git clone https://github.com/Meikoday/tencentcloud-auto-tools 
          cd testme
          python tencentcloud_PurgePathCache.py -id ${{ secrets.SECRET_ID }} -key ${{ secrets.SECRET_KEY }}
```

### 🔒 安全提醒
- 敏感凭证必须通过 GitHub Secrets 配置
- 建议使用子账户密钥并分配最小权限
- 定期轮换 API 密钥
