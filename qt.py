from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit, QMessageBox, QLabel
import apply

def handleClicked() :
    index = textEdit.toPlainText()
    if (len(index) == 0) :
        QMessageBox.critical(window, 'Error', '请输入网页的索引')
    else :
        window.setWindowTitle('waiting....')
        result = apply.predict(index)
        window.setWindowTitle('赛果预测')
        QMessageBox.about(window, '预测结果', result)

#导入相关的类
app = QApplication([])#创建一个对象  作用事提供整个图形界面的管理

window = QMainWindow() #创建一个主窗口对象
window.setObjectName("wkWgt")  # 替换背景图片只对当前窗口生效 核心代码
window.setStyleSheet("#wkWgt{border-image:url(Messi.png);}")  # 替换图片路径  核心代码
window.resize(600, 500) #窗口大小 （宽度，高度）
window.move(900, 400) #控制窗口显示的时候出现在屏幕显示器的位置
window.setWindowTitle('赛果预测') #把薪资统计设置在标题栏上

textEdit = QPlainTextEdit(window) #创建纯文本空间
textEdit.setPlaceholderText("请输入比赛网址的索引，例如 \n https://dongqiudi.com/liveDetail/53573455这场比赛，仅需输入53573455即可")#创建提示文本
textEdit.move(50,50)#在窗口处位置  如果有副窗口就显示在副窗口位置
textEdit.resize(500,80) #指定大小

button = QPushButton('开始预测', window) #设置按键
button.move(200,200) #位置
button.resize(200,100)
button.clicked.connect(handleClicked)

window.show() #显示界面，想要显示就必须要执行这一段代码
app.exec_() #进入QApplication的事件处理循环  如果不加这句话，界面就会一闪而过
