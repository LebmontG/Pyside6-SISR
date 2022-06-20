from PySide6.QtCore import*
from PySide6.QtWidgets import*
from PySide6.QtGui import*
import os,sys
from swinir import SwinIR as net
import torch
import numpy as np
import cv2
#import pyqtgraph

class Ui_application_pages(object):
    def setupUi(self, application_pages):
        if not application_pages.objectName():
            application_pages.setObjectName(u"application_pages")
        application_pages.resize(1056, 657)
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.verticalLayout = QVBoxLayout(self.page_1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(self.page_1)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(500, 70))
        self.frame.setMaximumSize(QSize(500, 70))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame)
        self.verticalLayout_4.setSpacing(4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"font: 700 14pt \"Segoe UI\";\n"
"color: rgb(255, 255, 255);")

        self.verticalLayout_4.addWidget(self.label_3)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setMinimumSize(QSize(0, 36))
        self.lineEdit.setMaximumSize(QSize(16777215, 36))
        self.lineEdit.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(68, 71, 90);\n"
"	padding: 8px;\n"
"	border: 2px solid #c3ccdf;\n"
"	color: rgb(255, 255, 255);\n"
"	border-radius: 10px;\n"
"}")

        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)

        self.btn_change_text = QPushButton(self.frame)
        self.btn_change_text.setObjectName(u"btn_change_text")
        self.btn_change_text.setMinimumSize(QSize(120, 36))
        self.btn_change_text.setMaximumSize(QSize(16777215, 36))
        self.btn_change_text.setStyleSheet(u"QPushButton {\n"
"	background-color: rgb(67, 133, 200);\n"
"	border: 2px solid #c3ccdf;\n"
"	color: rgb(255, 255, 255);\n"
"	border-radius: 10px;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(85, 170, 255);\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color: rgb(255, 0, 127);\n"
"}")

        self.gridLayout.addWidget(self.btn_change_text, 0, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout)


        self.verticalLayout.addWidget(self.frame, 0, Qt.AlignHCenter)

        application_pages.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_2 = QVBoxLayout(self.page_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        application_pages.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_3 = QVBoxLayout(self.page_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.page_3)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_3.addWidget(self.label)

        application_pages.addWidget(self.page_3)

        self.retranslateUi(application_pages)

        QMetaObject.connectSlotsByName(application_pages)
    # setupUi

    def retranslateUi(self, application_pages):
        application_pages.setWindowTitle(QCoreApplication.translate("application_pages", u"StackedWidget", None))
        self.label_3.setText(QCoreApplication.translate("application_pages", u"Olá...", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("application_pages", u"Escreva o seu nome", None))
        self.btn_change_text.setText(QCoreApplication.translate("application_pages", u"Alterar Texto", None))
        self.label_2.setText(QCoreApplication.translate("application_pages", u"P\u00e1gina 2", None))
        self.label.setText(QCoreApplication.translate("application_pages", u"Pagina 3", None))

class SISR(QMainWindow):
    def __init__(self, parent=None):
        super(SISR, self).__init__(parent)
        # application title and state
        self.setWindowTitle(self.tr("SISR"))
        #self.statusBar().showMessage('Rs')
        # parameters
        self.size_org=(160,120)
        self.size_res=(640,480)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.ST_path='weights/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth'
        self.impath = 'data/train/LR/1.png'
        self.outpath='res/'
        self.r_image_loc=[760,120]
        self.l_image_loc=[290,260]
        self.pre_m='VST'
        # menu and toolbar
        self.a_DAN= QAction(QIcon("icons/cil-wifi-signal-off.png"), self.tr("DAN"), self)
        self.a_DAN.triggered.connect(self.switch_DAN)
        self.a_VST= QAction(QIcon("icons/2.png"), self.tr("VST"), self)
        self.a_VST.setShortcut("Ctrl+G")
        self.a_VST.setStatusTip(self.tr("?????"))
        self.a_VST.triggered.connect(self.switch_VST)
        self.a_Gen= QAction(QIcon("icons/1.png"), self.tr("Make"), self)
        self.a_Gen.triggered.connect(self.generate)
        self.menu= self.menuBar().addMenu(self.tr("Menu"))
        self.menu.addAction(self.a_DAN)
        self.menu.addAction(self.a_VST)
        self.TB= self.addToolBar("Generate")
        self.TB.addAction(self.a_Gen)
        # button_file
        self.button_file= QPushButton(QPixmap("icons/cil-dog.png"),"Choose Image",self)
        self.button_file.setCheckable(True)
        self.button_file.setStyleSheet("background-color:green")
        self.button_file.move(20, 80)
        self.button_file.clicked.connect(self.select_file)
        # widgets
        self.wg_VST=QWidget(self)
        self.wg_DAN=QWidget(self)
        self.wg_HOME=QWidget(self)
        self.wg_stack=QStackedWidget()
        self.wg_stack.addWidget(self.wg_VST)
        self.wg_stack.addWidget(self.wg_HOME)
        self.wg_stack.addWidget(self.wg_DAN)
        self.wg_stack.setCurrentWidget(self.wg_HOME)
        self.settext(self.wg_DAN)
        # layout
        self.central_frame = QFrame()
        self.main_layout = QHBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        # pages
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("font-size: 12pt; color: #f8f8f2;")
        self.ui_pages = Ui_application_pages()
        self.ui_pages.setupUi(self.pages)
        self.pages.setCurrentWidget(self.ui_pages.page_1)
        self.ui_pages = Ui_application_pages()
        self.ui_pages.setupUi(self.pages)
        self.pages.setCurrentWidget(self.ui_pages.page_1)
        #self.content_layout.addWidget(self.pages)

        #qle = QLineEdit(self)
        #qle.move(60, 500)
        #qle.textChanged[str].connect(self.onChanged), y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));

        # self.styleSheet = QWidget(self)
        # self.styleSheet.setObjectName(u"styleSheet")
        # self.styleSheet.setStyleSheet(open("py_dracula_dark.qss", 'r').read())
        # font = QFont()
        # font.setFamily(u"Segoe UI")
        # font.setPointSize(56)
        # font.setBold(True)
        # font.setItalic(True)
        # self.styleSheet.setFont(font)
        # self.lineEdit.setStyleSheet("background-color: #6272a4;")
        # self.pushButton.setStyleSheet("background-color: #6272a4;")
        # self.plainTextEdit.setStyleSheet("background-color: #6272a4;")
        # self.tableWidget.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        # self.scrollArea.setStyleSheet("QScrollBar:vertical { background: #6272a4; } QScrollBar:horizontal { background: #6272a4; }")
        # self.comboBox.setStyleSheet("background-color: #6272a4;")
        # self.horizontalScrollBar.setStyleSheet("background-color: #6272a4;")
        # self.verticalScrollBar.setStyleSheet("background-color: #6272a4;")
        # self.commandLinkButton.setStyleSheet("color: #ff79c6;")

        self.generate()
        #self.show()
        return

    def settext(self,wd):
        # useful text
        wd.text_l='Original Image (LR)'
        wd.textlabel_l= QLabel(wd)
        #self.textlabel_l.setFont(QFont.bold)
        wd.text_r='Restored Image (HR)'
        wd.textlabel_r= QLabel(wd)
        wd.textlabel_l.move(310, 700)
        wd.textlabel_r.move(1070, 700)
        wd.textlabel_time=QLabel(wd)
        wd.textlabel_time.move(1470, 770)
        wd.textlabel_l.setText(wd.text_l)
        wd.textlabel_l.adjustSize()
        wd.textlabel_r.setText(wd.text_r)
        wd.textlabel_r.adjustSize()
        wd.day=QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
        wd.textlabel_time.setText(wd.day[-8:-3])
        wd.textlabel_r.adjustSize()
        # self.textlabel_l.setText(self.text_l)
        # self.textlabel_l.adjustSize()
        # self.textlabel_r.setText(self.text_r)
        # self.textlabel_r.adjustSize()
        # self.day=QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)
        # self.textlabel_time.setText(self.day[-8:-3])
        # self.textlabel_r.adjustSize()
        return
    # switch interface
    def switch_DAN(self):
        self.pre_m='DAN'
        self.wg_stack.setCurrentWidget(self.wg_DAN)
        return
    def switch_VST(self):
        self.pre_m='VST'
        self.wg_stack.setCurrentWidget(self.wg_VST)
        return
    # file action
    def select_file(self):
        # open file
        FileDialog = QFileDialog(self, 'Choose Image', './', 'jpg(*.jpg *.jpeg);;png(*.png);;python(*.py)')
        FileDialog.setAcceptMode(QFileDialog.AcceptOpen)
        FileDirectory = FileDialog.getOpenFileNames(FileDialog, 'Select a LR Image', './', 'jpg(*.jpg *.jpeg);;png(*.png))')
        FileDirectory = str(FileDirectory[0])
        self.impath =FileDirectory.replace('[', '').replace(']', '').replace('\'', '')
        #print(self.impath)
        return
    # make images
    def generate(self):
        par=self.pre_m
        # print images
        self.img_org=QPixmap(self.impath)
        width,height=self.img_org.width(),self.img_org.height()
        if width!=160 or height!=120:
            tmp=cv2.imread(self.impath)
            tmp=cv2.resize(tmp,(160,120))
            cv2.imwrite(self.impath,tmp)
            self.img_org=QPixmap(self.impath)
            width,height=self.img_org.width(),self.img_org.height()
        self.label_org= QLabel(self)
        self.label_org.setGeometry(self.l_image_loc[0], self.l_image_loc[1],self.l_image_loc[0]+width,self.l_image_loc[1]+height)
        self.label_org.setPixmap(self.img_org)
        # image size changes as windows size changes
        #self.label_org.setScaledContents(True)
        # boundary
        #self.label_org.setStyleSheet("border: 2px solid red")
        image_p=None
        if par=='SwinTransformer':
            image_p=self.swintransformer()
        elif par=='DAN':
            image_p=self.DAN()
        elif par=='MANet':
            image_p=self.MANet()
        elif par=='VST':
            image_p=self.VST()

        self.img_rest = QPixmap(image_p)
        width,height=self.img_rest.width(),self.img_rest.height()
        self.label_rest= QLabel(self)
        self.label_rest.setGeometry(self.r_image_loc[0], self.r_image_loc[1],self.r_image_loc[0]+width,self.r_image_loc[1]+height)
        self.label_rest.setPixmap(self.img_rest)
        #self.label_rest.setStyleSheet("border: 2px solid red")
        #self.show()
        print('Generating Finish!')
        return
    # swin-transformer
    def swintransformer(self):
        scale=4
        model = net(upscale=4, in_chans=3, img_size=64, window_size=8,
                    img_range=1., depths=[6, 6, 6, 6, 6, 6], embed_dim=180, num_heads=[6, 6, 6, 6, 6, 6],
                    mlp_ratio=2, upsampler='nearest+conv', resi_connection='1conv')
        pretrained_model = torch.load(self.ST_path)
        param_key_g = 'params_ema'
        model.load_state_dict(pretrained_model[param_key_g] if param_key_g in pretrained_model.keys() else pretrained_model, strict=True)
        model.eval()
        model = model.to(self.device)
        img_lq=cv2.imread(self.impath, cv2.IMREAD_COLOR).astype(np.float32) / 255.
        img_lq = np.transpose(img_lq if img_lq.shape[2] == 1 else img_lq[:, :, [2, 1, 0]], (2, 0, 1))
        img_lq = torch.from_numpy(img_lq).float().unsqueeze(0).to(self.device)
        window_size=8
        #print(img_lq);input()
        with torch.no_grad():
            # pad input image to be a multiple of window_size
            _, _, h_old, w_old = img_lq.size()
            h_pad = (h_old // window_size + 1) * window_size - h_old
            w_pad = (w_old // window_size + 1) * window_size - w_old
            img_lq = torch.cat([img_lq, torch.flip(img_lq, [2])], 2)[:, :, :h_old + h_pad, :]
            img_lq = torch.cat([img_lq, torch.flip(img_lq, [3])], 3)[:, :, :, :w_old + w_pad]
            output = model(img_lq)
            output = output[..., :h_old * scale, :w_old * scale]
        output = output.data.squeeze().float().cpu().clamp_(0, 1).numpy()
        output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
        output = (output * 255.0).round().astype(np.uint8)
        #plt.imshow(output);input()
        p=self.outpath+'ST.png'
        cv2.imwrite(p, output)
        return p
    # DAN
    def DAN(self):
        p=self.impath+'ST.png'
        return self.impath
    # MANet
    def MANet(self):
        p=self.outpath+'ST.png'
        return p
    # VST
    def VST(self):
        p=self.outpath+'ST.png'
        return p
    def clear(self):
        # qp = QPainter()
        # qp.begin(self)
        # col = QColor(0, 0, 0)
        # col.setNamedColor('#d4d4d4')
        # qp.setPen(col)
        # qp.setBrush(QColor(200, 0, 0))
        # qp.drawRect(1,1, 111, 111)
        # qp.drawRect(self.l_image_loc[0], self.l_image_loc[1], self.l_image_loc[0]+self.size_org[0], self.l_image_loc[1]+self.size_org[1])
        # qp.end()
        qp = QPainter()
        qp.begin(self)
        qp.setPen(Qt.GlobalColor.green)
        for x in range(self.l_image_loc[0],self.l_image_loc[0]+self.size_org[0]):
            for y in range(self.l_image_loc[1],self.l_image_loc[1]+self.size_org[1]):
                qp.drawPoint(x, y)
        for x in range(self.r_image_loc[0],self.r_image_loc[0]+self.size_res[0]):
            for y in range(self.r_image_loc[1],self.r_image_loc[1]+self.size_res[1]):
                qp.drawPoint(x, y)
        qp.end()
        return


if __name__ == "__main__":
    app =QApplication([])
    win=SISR()
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec())