## 写在前面
感谢 @Capco707 @bjzhb666 和 @hangzhiyiwei 三位大佬带我摸鱼[旺柴]

# Intelli power

- Intelli power is a software based on Python3, calculating complicated system power flow with high accuracy in a few seconds.
- We design delicate GUI and hopefully you can use it intuitively.
- No released .exe provided and you may run IntelliPower.py in PyCharm directly.

## Instructions
- The window dragging function can only be implemented in the toolbar (the second row), when the mouse becomes a hand-shaped ICON
- From left to right on the toolbar, add VA, PV, PQ, transformer, and transmission line. After adding, double-click to modify and view parameters.
- For transmission lines and transformers, you need to click on the toolbar and drag to add them. If you don't want to add them after clicking, press ESC
- The transmission line icon is a solid line, and the transformer icon is a dashed line
- After the input is complete, click the green arrow to calculate
- Click S and △S to view the calculation result of power flow
- File --> save file save as back_up.txt file, File --> open file to open mission.txt file, and calculate directly after loading

## Program Flowchart
![Untitled Diagram](https://user-images.githubusercontent.com/60430692/204129103-4aaa665a-a300-4568-993a-d243460eef01.png)
## User interface
### 1 GUI structure
![111](https://user-images.githubusercontent.com/60430692/204129120-6d519ea8-51c5-47e3-8774-32a53369eb44.png)
### 2 Overview
![截图](https://user-images.githubusercontent.com/60430692/204129122-c52abe10-7cc0-4e6b-8992-01a43e355eea.png)
### 3 Dialog
![va](https://user-images.githubusercontent.com/60430692/204129323-26d3e386-5cd6-41b2-84a5-270cd08bc860.png)
![保存](https://user-images.githubusercontent.com/60430692/204129326-a8aeaff5-7584-4acd-af20-ea05ae2b3e9a.png)

## 使用说明
- 窗口拖拽功能只能在工具栏(第二行)实现，届时鼠标变成手型ICON
- 工具栏从左到右依次为 VA，PV，PQ，变压器，传输线的添加，添加后双击修改和查看参数。
- 传输线和变压器需要点击工具栏后拖拽添加，点击后不想添加则按ESC
- 传输线图标为实线，变压器图标为虚线
- 输入完成后点击绿色箭头进行计算
- 计算结果点击 S 和 △S 查看功率流计算结果
- File --> save file 保存为back_up.txt文件，File --> open file 打开mission.txt文件，载入后直接计算

### 项目地址：https://github.com/XavierXYG/Powerflow_Calc.git
