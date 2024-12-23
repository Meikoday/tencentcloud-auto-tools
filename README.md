# tencentcloud-auto-tools
一切正在测试中，文中的参数fork到自己仓库修改即可
# 腾讯云cdn整站刷新工具
## tencentcloud_PurgePathCache.py
在第35行中``payload = "{\"Paths\":[\"https://www.meiko.ink/\"],\"FlushType\":\"flush\",\"UrlEncode\":false,\"Area\":\"mainland\"}"``<br/>
    修改为自己的参数  
    FlushType：  
      刷新类型  
      flush：刷新产生更新的资源  
      delete：刷新全部资源  
    UrlEncode：  
      是否对中文字符进行编码后刷新  
    Area：   
      刷新区域  
      无此参数时，默认刷新加速域名所在加速区域  
      填充 mainland 时，仅刷新中国境内加速节点上缓存内容  
      填充 overseas 时，仅刷新中国境外加速节点上缓存内容  
      指定刷新区域时，需要与域名加速区域匹配  
代码传入方式  
`python tencentcloud_PurgePathCache.py -id 你的腾讯云id -key 你的腾讯云key`  
示例：  
```bash
python tencentcloud_PurgePathCache.py -id testthisisid -key testthisiskey
```
可使用自动化部署工具  
列如：  
```bash
name: 测试部署

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
    environment: tenx
    steps:
      - name: 检出仓库
        uses: actions/checkout@v2

      - name: 克隆 coscmd 仓库
        run: |
          git clone https://github.com/Meikoday/testme.git
          cd testme
          python tencentcloud_PurgePathCache.py -id ${{ secrets.SECRET_ID }} -key ${{ secrets.SECRET_KEY }}
```
