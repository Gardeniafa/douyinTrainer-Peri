# douyin Trainer Peri
## 抖音养号助手  
### 自动点赞、关注转发高颜值小姐姐  

基于百度智能云api、图像识别、adb等应用平台

申请百度智能云API，配置config.yaml开始使用  
百度智能云人脸检测api目前仅0.0004元/次，充三四块够调一万次了  

### 快速上手
 - 下载源代码
   - git clone
   - 下载zip
 - 安装依赖
   - python环境：py3.11
   - 安装pip包 `pip install -r requirements.txt`
 - 注册、购买百度云人脸识别api
   - 链接：[百度智能云人脸识别](https://console.bce.baidu.com/)
   - 控制台首页-左上角菜单-产品服务-人工智能-人脸识别
   - 创建应用-人脸识别（选择基础服务-人脸检测就行了）
 - 填写配置
   - 将应用的appkey和secret填写到config.yaml的相应位置
 - 启动！
   - `python ./main.py`
 - 解决错误信息
   - 根据配置文件描述，结合自己设备，打开开发者模式，或者使用auto js慢慢量像素吧~
 

### 配置参数说明：  
- 应用名称和口令
```
application:
  token: '999999999999999999999'
  secret: '666666666666666666666'
```
- 配置信息  
```
settings:
  global_config:
    size:   -------------------> 允许的人脸最小的宽高，如果小于这个数值则不算在结果中（防止头像或者远处的人被算进来）
      width:
        min: 100
      height:
        min: 100
    beauty:   -----------------> 颜值分级，不同等级对应不同操作
      good: 30
      greet: 39
      excellent: 50
      amazing: 60
    cut:   --------------------> 切图（从屏幕截图截取有效部分上传到百度api），尽量把抖音左下方的信息（作者名称、文字信息）和右侧操作按钮（头像、点赞、评论等）截出去
      from:   ----------> 区域左上角坐标
        x: 0
        y: 290
      to:    -----------> 区域右下角坐标
        x: 915
        y: 1910

  age_range:   ----------------> 年龄分段 可爱女鹅和年轻漂亮小姐姐
    lovely_daughter:
      age:
        min: 5
        max: 10
    young_beauty:
      age:
        min: 17
        max: 30
```
- 设备操作配置  
以下配置中的数字适用于2388x1080启用全面屏手势的屏幕
```
device_manipulate:
  click:
    like:   -------------------> 点赞（双击的坐标）
      x: 800
      y: 1269
    follow:  ------------------> 关注按钮的两个坐标，由于抖音的合集、推广功能会独占一行，所以操作区按钮有的时候会被顶上去，造成了不同情况下按钮的位置发生变化
      high:  ------> 低处坐标（没有独占一行的组件出现时，按钮没被顶上去，所以y坐标值更大，靠下面）
        x: 988
        y: 1193
      low:   ------> 高处坐标（有独占一行组件的时候按钮被顶上去，y值变小，靠上面） == 请区分这里的high1指的是y坐标的绝对值，而不是感官上的高低 ==
        x: 988
        y: 1073
    share:  -------------------> 分享，三个步骤：1、点击分享 2、点击第一个好友 3、点击确定分享
      btn:  -------> 分享按钮的坐标，注意这个按钮也会受到影响，因为其较关注按钮大多了，所以按钮上浮前和上浮后有一个重叠区域，这个坐标即为这个区域里面的坐标，所以无论是否上浮都可以确保被点击到
        x: 993
        y: 1860
      friend:  ----> 第一个朋友的坐标
        x: 316
        y: 1806
      ensure:  ----> 确认分享
        x: 689
        y: 2301
  swipe:  ---------------------> 下滑下一条视频
    next:
      from:  ------> 起点
        x: 733
        y: 1813
      to:  --------> 终点
        x: 906
        y: 1416
      time: 100  --> 耗时
```

> 本项目依据[DouyinFaceTech](https://github.com/tomxin7/DouYinFaceTech)修改而来  
> 感谢Microsoft bing聊天模式的突出贡献