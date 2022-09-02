# csgo_yolov3_aimbot

基于yolov3的csgo自瞄ai

**使用方法**

首先启动游戏，如果在启动游戏之前运行此脚本，脚本会因为找不到窗口句柄而异常退出

游戏设置->视频设置->显示模式==**窗口模式**

游戏设置->键盘/鼠标->原始数据输入==**关闭**

目前脚本延时较高，建议使用的测试地图，创意工坊中的：**Skills Training Map**

调整这里的数字，```boxes[min_at][3]/7```打头，```boxes[min_at][3]/2```打胸

```py
y = int(boxes[min_at][1] + boxes[min_at][3]/7) + rect[1]# For head shot
```

**关于权重和配置**

你可以在[这里](https://pjreddie.com/darknet/yolo/)下载模型权重和配置文件, 你可以在aimbot.py更具你的需要更改它

经过实测将cfg文件的train模式改为test模式可以将神经网络时延减少70ms，此版本已更改

```py
CONFIG_FILE = './yolov3_416.cfg'
WEIGHT_FILE = './yolov3_416.weights'
```

**关于模型**

网络模型来自opencv库，但是opencv默认无GPU版本，如果你已经配置好了GPU版本的版本的opencv，你可能会有更好的游戏体验

```py
#如果你使用的cv2支持GPU
if cv2.cuda.getCudaEnabledDeviceCount():    
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    print("您使用的opencv支持GPU，当前GPU模式运行")
#如果你使用的opencv只支持CPU
else:   
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    print("您使用的opencv不支持GPU，当前CPU模式运行")
```

提示，你可以使用如下代码检查opencv是否使用GPU

```py
import cv2
count = cv2.cuda.getCudaEnabledDeviceCount()
print(count)
```

**关于win32api**

如果你配置不好win32api，你可以使用pyautogui，但是要**注意**：

使用win32api移动鼠标并射击的时间是5-10ms，使用pyautogui则是200ms

```py
win32api.SetCursorPos((x, y))
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
# pyautogui.moveTo(x,y)
# pyautogui.click()
```

**改进中......**

目前我使用CPU，跑网络+框人大约要500ms，如下。。。持续优化ing

```
get_window_time:0.0
get_screen_time:0.051331520080566406
run net time:0.4056708812713623
get enemy box time:0.06399965286254883
Detected animies:3
get front sight axis time0.00099945068359375
move mouse and shoot time:0.009003639221191406
tortoal time:0.5310051441192627
```



