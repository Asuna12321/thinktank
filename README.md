## 智库项目图表数据处理

### 目前进度
- [x] 数据读取至dataframe
- [ ] 数据读取至SQL
- [ ] 机构地理位置映射等
- [ ] 

### Project Structure

1. \Config.py

    数据储存路径
    
2. \Pipeline.py
    
    * `parsetxt2df`
    
    Academic Social Networks数据读取（Authors及Papers）
    
    * `parsejson2df`
    
    DBLP Citation数据读取
    
3. \process.py
    
    Dataframe处理
    
dblp数据集中有keywords从其提取词云