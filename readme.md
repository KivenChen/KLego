# PyLego 使用指南



- **不用搭积木**
- 不用绕 Data Wire
- **前进、转弯都可以在 3 个字符内**
- 为什么不用 Python 来写乐高呢？



## 概述

- 基于 Python 2.7 （Python 3 目前无法使用前进/后退功能）
- 目前只有 NXT 支持
- 基于 nxt-python 
- 连接需要 pyusb 以及 pybluez 模块

## V0.91 更新

更新于 12-11-18

- **紧急修复**：蓝牙连接问题，以及蓝牙模块的安装问题。请查看文档的**安装**部分
- **新增**：实验性定位模块 `pos_utils`
- 相比 v0.9 时处于测试期的 `pos_utils`，改变了使用细节（见**定位模块的使用 - discover()**）
- 稳定性提升

## V0.9 更新
更新于 12-10-18
- 修复 bug 并提高稳定性
- 改进`f()`和`b()`的参数，使之更简洁

- **新增：图形化无法实现的重磅功能：原地旋转**
    - 关于实现请查看 `spin()` 函数
- 新增： `hold_on()`函数。开着命令行挂机，随时写点东西，不用担心 Lego 省电关机
- （**目前(2018-12-10)的 `t` 参数暂未提供支持**）

## 安装
项目中有已经有需要的环境（Windows），但因为有一些细节工作，所以提供第三方教程[教程]: -https://blog.xuezhonghao.com/2018/08/16/nxt-python.html 

### 安装第三方库

#### 连接相关

- Windows: (**修复蓝牙模块的安装问题**) 从以下链接下载并安装 VC 9.0 Compiler for Python
  - https://www.microsoft.com/en-us/download/details.aspx?id=44266

- Windows: 项目中有你需要的部分第三方库(**为确保稳定性，请使用 v0.91 最新版提供的安装文件**)，在命令行中分别进入 `pyusb` 以及 `pybluez` 文件夹，并运行 `python setup.py install`
- Mac: 请参考上述教程

#### 内核相关

- Windows：在 cmd 命令行运行：`pip install threading`
- Mac：在 terminal 中运行：`sudo pip install threading` （需要权限）

### 配置驱动
- Windows: 按照上述教程配置 USB 驱动，把乐高驱动换成 libusb-win32
- Mac：安装 libusb
- （~~测试版目前仅支持 USB 调试~~。试验性蓝牙模块已经加入）

### 导入模块
- 以下2个步骤都可以
    1. 把 nxt 文件夹放入你正在写的 python 项目文件夹
    2. 命令行执行 `pip install nxt-python` 
- 把 core.py 以及 放在你正在写的 python 项目文件夹里面


## 开始

输入以下语句即可食用以下提及的所有函数

``` python
from core import *
```

以下是默认使用的接口，如果你想改动请到 `core.py` 的 `reset()`中更改，第一次导入 `core` 模块时都会调用这个函数进行初始化。如果不想改程序，请改造你的乐高机器人。

``` python
 L-Motor: PORT_B
 R-Motor: PORT_C
 Light(PORT_3)
 Ultrasonic(PORT_2)
 Touch(PORT_4)
```

## 关于函数的设计

- 每个函数都有参数
- 每个函数的参数都有默认值
- 如果你不想要默认值，可以改其中一个、一些或者全部


## 运动类函数

### `l(r=1, p=75, t=None, b=True)`

---

向左转的函数，注意是**小写的L**
####  参数解析：
- `p`：马力。整数。默认值是75即75%马力
- `r`：转动的距离(rolls)。（**如果 `t` 被修改，那么`r`的值作废！**）
    - 如果 `r` **>=30**，会被认为是**轮子转动的角度(degree)**。比如 `r=360` 就是让右轮旋转360度（正好一圈），于是左转
    - 否则，会被认为是**轮子转动的圈数(circles of rotation)**
- `t`：转动的时间。（**如果 `t` 被修改，那么`r`的值作废！**）**目前(2018-12-10)的 `t` 参数暂未提供支持，下同**
     - 单位：秒
- `b`: 即 break, 是否转完马上刹车
    - 只能是 True 或者 False
    - 默认值 True


#### 例子
``` python
l() # 75%马力，右轮转1圈，使整体左转
l(3) # 75%马力，右轮转3圈，使整体左转
l(p=80, r=3) # 80%马力，右轮转3圈
l(r=45) # 右轮转45度
l(t=10) # 右轮转10秒
```

### `r(r=1, p=75, t=None, b=True)`

---

右转的函数。请参考 `l` 的说明

### `spin(r=1, p=75)`

---

顺时针原地旋转（**v0.9 的更新内容**）
参数请参考上面的函数


### `f(r=1, p=75, t=None)`

---

前进(forward)的函数
#### 参数解析
- ~~`unlimited`：是否无限前进，直到下一个操作发生。要不 True 要不 False~~（现已取消）
- 当 `r` 的值为 **1** 或者 **None**，无限前进，直到 `stop()` 被执行
- 其余请参考 `l`
- **在 p > 75 的情况下，长时间移动可能导致电压过低，Brick 重启**
#### 例子
```python
f() # 两边轮子转1圈前进
f(3) # 两边轮子转3圈前进
f(0)
f(None) # 一直前进直到 stop 被调用
#其余参考 l（）函数
```


### `b(r=1, p=100, t=None)`

---

后退(backward）的函数，参考 `f()`


## 功能类函数

### `reset(remote=True)`

---

执行 `from core import *` 时，模块会自动调用这个函数进行初始化，并自动检测连接方式，**如果两种方式都行，优先 USB**（见参数解析）。

如果出现连接错误，请调用它重新连接。或者可以使用参数把连接方式重置为另一种。使用蓝牙方式`reset(True)` 配合 Python 命令行食用风味更佳，敲下来的命令可以立即执行。

#### 使用方法
- 默认值： USB
- True： 蓝牙
- False: USB


### `sound()`

---

发出声音**（尚不稳定）**


### `hold_on()`

---

挂机专用，防止乐高圣殿关机


## 传感类函数

### `distance() -> int`

---

获取一个整数：即超声波传感器的读数
单位 **cm**

### `brightness() -> int`

---

获取一个整数：光传感器的读数
区间：0 ~ 100

### `hit()`

---

判断是否撞到物体（**传感器被按下，或者是距离<5cm**）
返回值:
- True：是的，撞到了
- False： 不，~

### `black() -> bool`

---

判断地面是否为黑色。是则返回 True，否则 False。

### `green() -> bool`

---

判断地面是否是绿色。参考上一个

### `white() -> bool`

---

白色


## 定位模块的使用

方位检测的基础实现在 **pos_utils.py** 中，~~与 PyLego 的核心 **core.py** 为相互依赖关系~~ 在 v0.91 中，转为 core 对 pos_utils 的单向依赖。使用时只需要导入 **core.py** 即可食用 。详见下文的 `pos` 和 `boxes`
``` python
from core import *
```

### pos
一个 `Position`类的对象。
core 模块会使用 `pos` 自动记录机器人在规范化移动之后的位置，注意：只记录以下情况的位置变化——

- 原地转特殊角
- 直行

包含相对原点 x, y 坐标，以及相对原始位置的转角 `d`，单位为顺时针角度，0~360

#### `Position` 的子类 `Box`
已经发现的块为 `Box` 类型，隶属 `Position` 的子类，比 `Position` 多了 `new`参数。
- 当 `new` 为 True, 代表这个块被发现，但不知道是不是得分块，可以一去
- 否则，代表这个块**不是**得分块 / 已经碰过

这个继承关系使 `Position` 能兼容 `Box`（见 `dist()`）

#### **dist(self, position/box)**  (Position / Box 的成员函数)
检测自身与某个位置 / 某个box 的距离

例子：
``` python
boxes.discover()  # 检查周围的块
boxes[0].dist(pos)  # 机器人与第 1 个被发现的块的距离
pos.dist(boxes[0])  # 和第二个等价 
```
### boxes
一个被定制过的列表，用于存储已经发现的块。

#### **nearest() -> Box**
返回一个 Box。在被 `boxes` 记录在案的 boxes 中寻找：
- `new = True`
- 而且离机器人最近的

#### **overlapped(target_pos, threshold=14) -> bool**
如果你检测到一个 box，但是担心重复检测，可以用这个函数。

`threshold`：默认如果距离小于 **14 cm** 即重叠

### core 中集成的函数

#### **discover(boxes)**
**v0.91 更新：将 discover 从 boxes 类的成员函数转为 core 模块的静态函数**

控制机器人旋转360度，并记录各个方向上的块。此函数会过滤重复检测的结果。

#### 定位模块的例子：一个流程
``` python
while True():
    discover(boxes)  # 检测物块。
	target = boxes.nearest()  # 挑最近的，没去过的
	'''go to the target ...'''
	target.new = False  # 标记为已去过
```

