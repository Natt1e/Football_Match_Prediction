from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit, QMessageBox, QLabel
from PySide2.QtGui import QFont
import apply

class MyWindow(QMainWindow) :
    def __init__(self):
        super().__init__()
        self.setWindowTitle('赛果预测')
        self.resize(600, 750)
        self.move(900, 400)

def handleClicked() :
    index = textEdit.toPlainText()
    if (len(index) == 0) :
        QMessageBox.critical(window, 'Error', '请输入网页的索引')
    else :
        font_14 = QFont()
        font_14.setPointSize(14)
        label = QLabel(window)
        label.setText("正在抓取相关数据并进行预测，请您等待.......")
        label.setFont(font_14)
        label.setFixedSize(600, 30)
        label.move(50, 25)
        label.show()
        window.repaint()
        window.setWindowTitle('waiting....')

        team1, team2, result = apply.predict(index)
        window.setWindowTitle("赛果预测")
        label.setText("预测成功，请您查看结果")
        label.move(180, 25)
        QMessageBox.about(window, '%s vs %s' % (team1, team2), result)

#导入相关的类
app = QApplication([])#创建一个对象  作用事提供整个图形界面的管理
app.setStyle("Fusion")
window = MyWindow()
window.setObjectName("wkWgt")  # 替换背景图片只对当前窗口生效
window.setStyleSheet("#wkWgt{border-image:url(Messi.png);}")  # 替换图片路径

textEdit = QPlainTextEdit(window) #创建纯文本空间
textEdit.setPlaceholderText("请输入比赛网址的索引，例如 \n https://dongqiudi.com/liveDetail/53573455这场比赛，仅需输入53573455即可")#创建提示文本
textEdit.move(50,70)#在窗口处位置  如果有副窗口就显示在副窗口位置
textEdit.resize(500,80)

button = QPushButton('开始预测', window) #设置按键
button.move(250,200)
button.resize(100,50)
button.clicked.connect(handleClicked)

window.show() #显示界面，想要显示就必须要执行这一段代码
app.exec_() #进入QApplication的事件处理循环  如果不加这句话，界面就会一闪而过
