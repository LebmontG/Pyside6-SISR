import sys,os
from PySide6.QtCore import*
from PySide6.QtWidgets import*
from PySide6.QtGui import*
#from swinir import SwinIR as net
#import matplotlib.pyplot as plt
#import torch.nn as nn
#import torch
import numpy as np
#import VSTm
#import pyinstaller
import cv2


class PyPushButton(QPushButton):
    def __init__(
            self,
            text="",
            height=40,
            minimum_width=50,
            text_padding=55,
            text_color="#c3ccdf",
            icon_path="",
            icon_color="#c3ccdf",
            btn_color="#44475a",
            btn_hover="#4f5368",
            btn_pressed="#282a36",
            is_active=False
    ):
        super().__init__()

        # Set default parametros
        self.setText(text)
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.setCursor(Qt.PointingHandCursor)

        # Custom parameters
        self.minimum_width = minimum_width
        self.text_padding = text_padding
        self.text_color = text_color
        self.icon_path = icon_path
        self.icon_color = icon_color
        self.btn_color = btn_color
        self.btn_hover = btn_hover
        self.btn_pressed = btn_pressed
        self.is_active = is_active

        # Set style
        self.set_style(
            text_padding=self.text_padding,
            text_color=self.text_color,
            btn_color=self.btn_color,
            btn_hover=self.btn_hover,
            btn_pressed=self.btn_pressed,
            is_active=self.is_active
        )

    def set_active(self, is_active_menu):
        self.set_style(
            text_padding=self.text_padding,
            text_color=self.text_color,
            btn_color=self.btn_color,
            btn_hover=self.btn_hover,
            btn_pressed=self.btn_pressed,
            is_active=is_active_menu
        )

    def set_style(
            self,
            text_padding=55,
            text_color="#c3ccdf",
            btn_color="#44475a",
            btn_hover="#4f5368",
            btn_pressed="#282a36",
            is_active=False
    ):
        style = f"""
        QPushButton {{
            color: {text_color};
            background-color: {btn_color};
            padding-left: {text_padding}px;
            text-align: left;
            border: none;
        }}
        QPushButton:hover {{
            background-color: {btn_hover};
        }}
        QPushButton:pressed {{
            background-color: {btn_pressed};
        }}
        """

        active_style = f"""
        QPushButton {{
            background-color: {btn_hover};
            border-right: 5px solid #282a36;
        }}
        """
        if not is_active:
            self.setStyleSheet(style)
        else:
            self.setStyleSheet(style + active_style)

    def paintEvent(self, event):
        # Return default style
        QPushButton.paintEvent(self, event)

        # Painter
        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.Antialiasing)
        qp.setPen(Qt.NoPen)

        rect = QRect(0, 0, self.minimum_width, self.height())

        self.draw_icon(qp, self.icon_path, rect, self.icon_color)

        qp.end()

    def draw_icon(self, qp, image, rect, color):
        # Format Path
        app_path = os.path.abspath(os.getcwd())
        folder = "icons"
        path = os.path.join(app_path, folder)
        icon_path = os.path.normpath(os.path.join(path, image))

        # Draw icon
        icon = QPixmap(icon_path)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), color)
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2,
            (rect.height() - icon.height()) / 2,
            icon
        )
        painter.end()

class UI_MainWindow(object):
    def setup_ui(self, parent):
        if not parent.objectName():
            parent.setObjectName("MainWindow")
        # SET INITIAL PARAMETERS
        # ///////////////////////////////////////////////////////////////
        parent.resize(1200, 720)
        parent.setMinimumSize(960, 540)

        # CREATE CENTRAL WIDGET
        # ///////////////////////////////////////////////////////////////
        self.central_frame = QFrame()

        # CREATE MAIN LAYOUT
        self.main_layout = QHBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(1,1,1,1)
        self.main_layout.setSpacing(0)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////
        self.left_menu = QFrame()
        self.left_menu.setStyleSheet("background-color: #44475a")
        self.left_menu.setMaximumWidth(50)
        self.left_menu.setMinimumWidth(50)

        # LEFT MENU LAYOUT
        self.left_menu_layout = QVBoxLayout(self.left_menu)
        self.left_menu_layout.setContentsMargins(0,0,0,0)
        self.left_menu_layout.setSpacing(0)

        # TOP FRAME MENU
        self.left_menu_top_frame = QFrame()
        self.left_menu_top_frame.setMinimumHeight(40)
        self.left_menu_top_frame.setObjectName("left_menu_top_frame")

        # TOP FRAME LAYOUT
        self.left_menu_top_layout = QVBoxLayout(self.left_menu_top_frame)
        self.left_menu_top_layout.setContentsMargins(0,0,0,0)
        self.left_menu_top_layout.setSpacing(0)

        # TOP BTNS
        self.toggle_button = PyPushButton(
            text = "Menu",
            icon_path = "cil-account-logout.png"
        )
        self.btn_1 = PyPushButton(
            text = "VST",
            is_active = True,
            icon_path = "cil-dog.png"
        )
        self.btn_2 = PyPushButton(
            text = "MANet",
            icon_path = "cil-3d.png"
        )
        self.btn_3 = PyPushButton(
            text = "DAN",
            icon_path = "cil-4k.png"
        )
        self.btn_4 = PyPushButton(
            text = "SwinIR",
            icon_path = "cil-alarm.png"
        )
        self.btn_5 = PyPushButton(
            text = "EDSR",
            icon_path = "cil-face-dead.png"
        )

        # ADD BTNS TO LAYOUT
        self.left_menu_top_layout.addWidget(self.toggle_button)
        self.left_menu_top_layout.addWidget(self.btn_1)
        self.left_menu_top_layout.addWidget(self.btn_2)
        self.left_menu_top_layout.addWidget(self.btn_3)
        self.left_menu_top_layout.addWidget(self.btn_4)
        self.left_menu_top_layout.addWidget(self.btn_5)

        # MENU SPACER
        # ///////////////////////////////////////////////////////////////
        self.left_menu_spacer = QSpacerItem(20,20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # BOTTOM FRAME MENU
        # ///////////////////////////////////////////////////////////////
        self.left_menu_bottom_frame = QFrame()
        self.left_menu_bottom_frame.setMinimumHeight(40)
        self.left_menu_bottom_frame.setObjectName("left_menu_bottom_frame")

        self.left_menu_bottom_layout = QVBoxLayout(self.left_menu_bottom_frame)
        self.left_menu_bottom_layout.setContentsMargins(0,0,0,0)
        self.left_menu_bottom_layout.setSpacing(0)

        # BOTTOM BTNS
        self.settings_btn = PyPushButton(
            text = "Developers",
            icon_path = "icon_settings.svg"
        )

        # ADD BTNS TO LAYOUT
        self.left_menu_bottom_layout.addWidget(self.settings_btn)

        # LABEL VERSION
        # ///////////////////////////////////////////////////////////////
        # self.left_menu_label_version = QLabel("v1.0.0")
        # self.left_menu_label_version.setAlignment(Qt.AlignCenter)
        # self.left_menu_label_version.setMinimumHeight(30)
        # self.left_menu_label_version.setMaximumHeight(30)
        # self.left_menu_label_version.setStyleSheet("color: #c3ccdf")

        # ADD TO LAYOUT
        # ///////////////////////////////////////////////////////////////
        self.left_menu_layout.addWidget(self.left_menu_top_frame)
        self.left_menu_layout.addItem(self.left_menu_spacer)
        self.left_menu_layout.addWidget(self.left_menu_bottom_frame)
        #self.left_menu_layout.addWidget(self.left_menu_label_version)

        # CONTENT
        # ///////////////////////////////////////////////////////////////
        self.content = QFrame()
        self.content.setStyleSheet("background-color: #282a36")

        # Content Layout
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setSpacing(0)

        # TOP BAR
        # ///////////////////////////////////////////////////////////////
        self.top_bar = QFrame()
        self.top_bar.setMinimumHeight(30)
        self.top_bar.setMaximumHeight(30)
        self.top_bar.setStyleSheet("background-color: #21232d; color: #6272a4")
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(10,0,10,0)

        # Left label
        self.top_label_left = QLabel("Single Image Super Resolution")

        # Top spacer
        self.top_spacer = QSpacerItem(20,20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Right label
        self.top_label_right = QLabel("HUST.AIA Pattern  Recognition")
        self.top_label_right.setStyleSheet("font: 700 9pt 'Segoe UI'")

        # Add to layout
        self.top_bar_layout.addWidget(self.top_label_left)
        self.top_bar_layout.addItem(self.top_spacer)
        self.top_bar_layout.addWidget(self.top_label_right)

        # Application pages
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("font-size: 12pt; color: #f8f8f2;")
        self.ui_pages = Ui_application_pages()
        self.ui_pages.setupUi(self.pages)
        self.pages.setCurrentWidget(self.ui_pages.page_1)

        # BOTTOM BAR
        # ///////////////////////////////////////////////////////////////
        self.bottom_bar = QFrame()
        self.bottom_bar.setMinimumHeight(30)
        self.bottom_bar.setMaximumHeight(30)
        self.bottom_bar.setStyleSheet("background-color: #21232d; color: #6272a4")

        self.bottom_bar_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_bar_layout.setContentsMargins(10,0,10,0)

        # Left label
        self.bottom_label_left = QLabel("LebmontG")

        # Top spacer
        self.bottom_spacer = QSpacerItem(20,20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Right label
        self.bottom_label_right = QLabel(QDateTime.currentDateTime().toString(Qt.DateFormat.ISODate)[:-3])

        # Add to layout
        self.bottom_bar_layout.addWidget(self.bottom_label_left)
        self.bottom_bar_layout.addItem(self.bottom_spacer)
        self.bottom_bar_layout.addWidget(self.bottom_label_right)

        # Add to content layout
        self.content_layout.addWidget(self.top_bar)
        self.content_layout.addWidget(self.pages)
        self.content_layout.addWidget(self.bottom_bar)

        # ADD WIDGETS TO APP
        # ///////////////////////////////////////////////////////////////
        self.main_layout.addWidget(self.left_menu)
        self.main_layout.addWidget(self.content)

        # SET CENTRAL WIDGET
        parent.setCentralWidget(self.central_frame)

class Ui_application_pages(object):
    def setupUi(self, application_pages):
        if not application_pages.objectName():
            application_pages.setObjectName(u"application_pages")
        self.r_image_loc=[760,120]
        self.l_image_loc=[290,260]
        self.impath = 'data/train/LR/1.png'

        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.verticalLayout =QVBoxLayout(self.page_1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.addStretch(1)
        self.frame = QFrame(self.page_1)
        self.frame.setObjectName(u"frame")
        self.label_1 = QLabel(self.frame)
        self.label_1.setAlignment(Qt.AlignCenter)

        self.label_12 = QLabel(self.page_1)
        self.label_12.move(280, 560)
        self.label_122 = QLabel(self.page_1)
        self.label_122.move(950, 660)
        # file
        self.button_file= QPushButton(QPixmap("icons/1.png"),"Choose Image",self.frame)
        self.button_file.setObjectName(u"btn_change_text")
        self.button_file.setCheckable(True)
        self.button_file.setStyleSheet("background-color:green")
        self.button_file.move(200, 180)
        self.verticalLayout.addWidget(self.button_file)
        application_pages.addWidget(self.page_1)

        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.move(310, 560)
        self.label_22 = QLabel(self.page_2)
        self.label_22.setObjectName(u"label_2")
        self.label_22.move(980, 660)

        # self.label_21 = QLabel(self.page_2)
        # self.label_21.setObjectName(u"label_21")
        # self.label_21.setGeometry(self.l_image_loc[0], self.l_image_loc[1],self.l_image_loc[0]+160,self.l_image_loc[1]+120)
        # img_org=QPixmap(self.impath)
        # self.label_21.setPixmap(img_org)

        self.button_2= QPushButton(QPixmap("icons/cil-dog.png"),"Choose Image",self.page_2)
        self.button_2.setObjectName(u"btn_change_text")
        self.button_2.setCheckable(True)
        self.button_2.setStyleSheet("background-color:green")
        self.button_2.move(30, 680)

        application_pages.addWidget(self.page_2)

        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.label_3 = QLabel(self.page_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.move(310, 560)
        self.label_32 = QLabel(self.page_3)
        self.label_32.setObjectName(u"label_3")
        self.label_32.move(980, 660)
        self.button_32= QPushButton(QPixmap("icons/cil-dog.png"),"Choose Image",self.page_3)
        self.button_32.setObjectName(u"btn_change_text")
        self.button_32.setCheckable(True)
        self.button_32.setStyleSheet("background-color:green")
        self.button_32.move(30, 680)
        application_pages.addWidget(self.page_3)

        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.label_4 = QLabel(self.page_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.move(310, 560)
        self.label_42 = QLabel(self.page_4)
        self.label_42.setObjectName(u"label_4")
        self.label_42.move(980, 660)
        self.button_42= QPushButton(QPixmap("icons/cil-dog.png"),"Choose Image",self.page_4)
        self.button_42.setObjectName(u"btn_change_text")
        self.button_42.setCheckable(True)
        self.button_42.setStyleSheet("background-color:green")
        self.button_42.move(30, 680)
        application_pages.addWidget(self.page_4)


        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.label_5 = QLabel(self.page_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.move(310, 560)
        self.label_52 = QLabel(self.page_5)
        self.label_52.setObjectName(u"label_5")
        self.label_52.move(980, 660)
        self.button_52= QPushButton(QPixmap("icons/cil-dog.png"),"Choose Image",self.page_5)
        self.button_52.setObjectName(u"btn_change_text")
        self.button_52.setCheckable(True)
        self.button_52.setStyleSheet("background-color:green")
        self.button_52.move(30, 680)
        application_pages.addWidget(self.page_5)

        self.retranslateUi(application_pages)

        QMetaObject.connectSlotsByName(application_pages)
    # setupUi
    def retranslateUi(self, application_pages):
        application_pages.setWindowTitle(QCoreApplication.translate("application_pages", u"StackedWidget", None))
        #self.label_3.setText(QCoreApplication.translate("application_pages", u"Select a LR Image Please", None))
        #self.lineEdit.setPlaceholderText(QCoreApplication.translate("application_pages", u"Escreva o seu nome", None))
        self.button_file.setText(QCoreApplication.translate("application_pages", u"Select a LR Image Please", None))
        self.button_2.setText(QCoreApplication.translate("application_pages", u"Select a LR Image Please", None))
        self.button_32.setText(QCoreApplication.translate("application_pages", u"Select a LR Image Please", None))
        self.button_42.setText(QCoreApplication.translate("application_pages", u"Select a LR Image Please", None))
        self.button_52.setText(QCoreApplication.translate("application_pages", u"Select a LR Image Please", None))
        #self.button_32.setText(QCoreApplication.translate("application_pages", u"Select a LR Image Please", None))
        self.label_2.setText(QCoreApplication.translate("application_pages", 'Original Image (LR)', None))
        self.label_22.setText(QCoreApplication.translate("application_pages", 'Restored Image (HR)', None))
        self.label_3.setText(QCoreApplication.translate("application_pages", 'Original Image (LR)', None))
        self.label_32.setText(QCoreApplication.translate("application_pages", 'Restored Image (HR)', None))
        self.label_5.setText(QCoreApplication.translate("application_pages", 'Original Image (LR)', None))
        self.label_42.setText(QCoreApplication.translate("application_pages", 'Restored Image (HR)', None))
        self.label_4.setText(QCoreApplication.translate("application_pages", 'Original Image (LR)', None))
        self.label_52.setText(QCoreApplication.translate("application_pages", 'Restored Image (HR)', None))
        self.label_12.setText(QCoreApplication.translate("application_pages", 'LR', None))
        self.label_122.setText(QCoreApplication.translate("application_pages", 'HR', None))
        #self.label.setText(QCoreApplication.translate("application_pages", u"Pagina 3", None))
    # retranslateUi

class QCImageViewer(QGraphicsView):
    files_changed = Signal(list)
    state_changed = Signal(str)

    def __init__(self):
        QGraphicsView.__init__(self)

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setSceneRect(-5000, -5000, 10000, 10000)

        self.setBackgroundBrush(QBrush(QColor("#222225"), Qt.SolidPattern))

        self.pixmaps = []

        self.aspectRatioMode = Qt.KeepAspectRatio
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.single_image_mode = True

        self.items_selectable = False

        self.is_flipped = False

        self.is_rotating = False
        self.rotation = 0
        self.rotation_step = 5

        self.scale_factor = 1
        self.resize_lock = False

        self.img_paths_displayed = []  # the image files being displayed in the scene
        self.img_paths_dir = []  # the loadable image files in the currant directory
        self.img_dirname = None
        self.img_filename = None

        self.SUPPORTED_FILE_TYPES = [".png", ".jpg", ".jfif", ".webp"]

    def load_single_image(self, path):
        if os.path.isfile(path):
            for pixmap in self.pixmaps:
                self.scene.removeItem(pixmap)

            self.pixmaps = []
            self.img_paths_displayed = []

            pixmap = QPixmap(path)
            pixmap_item = self.add_image(pixmap)

            self.pixmaps.append(pixmap_item)

            self.img_dirname = os.path.dirname(path)
            self.img_filename = os.path.basename(path)
            self.img_paths_displayed.append(os.path.join(self.img_dirname, self.img_filename))
            self.img_paths_dir = []

            # thie following 4 lines could be a list comprehension, thank me later
            for filename in os.listdir(self.img_dirname):
                abs_path = os.path.join(self.img_dirname, filename)
                if os.path.splitext(abs_path)[-1] in self.SUPPORTED_FILE_TYPES:
                    self.img_paths_dir.append(abs_path)

            self.reset_viewer(zoom=True, rotation=True, flip=True)

            self.files_changed.emit(self.img_paths_displayed)
            self.single_image_mode = True
            self.state_changed.emit("single")

    def load_additional_image(self, path):
        if os.path.isfile(path):
            if self.single_image_mode:
                self.single_image_mode = False
                self.state_changed.emit("multiple")

            self.img_paths_displayed.append(path)

            self.files_changed.emit(self.img_paths_displayed)

            pixmap = QPixmap(path)
            pixmap_item = self.add_image(pixmap)

            self.reset_viewer(zoom=True, rotation=True, flip=True)

            self.pixmaps.append(pixmap_item)

    def add_image(self, pixmap):
        item = self.scene.addPixmap(pixmap)

        self.toggle_selectable(False)
        self.reset_viewer(zoom=True)

        return item

    def flip_image(self):
        self.scale(-1, 1)
        self.is_flipped = not self.is_flipped

    def toggle_rotating(self):
        self.is_rotating = not self.is_rotating

    def reset_viewer(self, rotation=False, zoom=False, flip=False):
        if flip:
            if self.is_flipped:
                self.flip_image()
            self.is_flipped = False

        if rotation:
            # dont touch this it works somehow idk why
            if self.is_flipped:
                self.rotate(self.rotation)
            else:
                self.rotate(self.rotation * -1)
            self.rotation = 0

        if zoom:
            # self.setSceneRect(self.scene.itemsBoundingRect())
            self.fitInView(self.scene.itemsBoundingRect(), self.aspectRatioMode)
            self.scale_factor = 1

    # returns the viewport as pixmap
    def export_image(self):
        pixmap = QPixmap(self.viewport().size())
        self.viewport().render(pixmap)

        return pixmap

    def step(self, direction):
        if self.single_image_mode:
            index = self.img_paths_dir.index(self.img_paths_displayed[0])

            if direction == "left":
                if index == 0:
                    return
                new_img_path = self.img_paths_dir[index - 1]

            elif direction == "right":
                if index + 1 == len(self.img_paths_dir):
                    return
                new_img_path = self.img_paths_dir[index + 1]

            self.load_single_image(new_img_path)

    def toggle_selectable(self, value):
        for pixmap in self.pixmaps:
            pixmap.setFlag(QGraphicsItem.ItemIsSelectable, value)
            pixmap.setFlag(QGraphicsItem.ItemIsMovable, value)
        self.items_selectable = value

    def change_opacity(self, value):
        if self.single_image_mode:
            self.pixmaps[0].setOpacity(value)
        elif len(self.scene.selectedItems()) == 1:
            self.scene.selectedItems()[0].setOpacity(value)

    # Events
    def resizeEvent(self, event):
        if self.resize_lock:
            self.resize_lock = not self.resize_lock
            return

        self.reset_viewer(zoom=True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.is_dragging = True

        QGraphicsView.mousePressEvent(self, event)

        if self.items_selectable and len(self.scene.selectedItems()) > 0:
            for item in self.pixmaps:
                item.setZValue(0)
            self.scene.selectedItems()[0].setZValue(1)

    def mouseReleaseEvent(self, event):
        QGraphicsView.mouseReleaseEvent(self, event)

        if event.button() == Qt.LeftButton:
            self.setDragMode(QGraphicsView.NoDrag)
            self.is_dragging = False

        QGraphicsView.mouseReleaseEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.RightButton:
            self.reset_viewer(rotation=True, zoom=True)

        QGraphicsView.mouseDoubleClickEvent(self, event)

    def wheelEvent(self, event):
        # dont touch it it works idk why but it works
        if self.is_rotating:
            if event.angleDelta().y() > 0:
                if self.is_flipped:
                    self.rotate(-self.rotation_step)
                    self.rotation += self.rotation_step
                else:
                    self.rotate(self.rotation_step)
                    self.rotation += self.rotation_step

            else:
                if self.is_flipped:
                    self.rotate(self.rotation_step)
                    self.rotation -= self.rotation_step
                else:
                    self.rotate(-self.rotation_step)
                    self.rotation -= self.rotation_step

        else:
            self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)  # AnchorUnderMouse # AnchorViewCenter

            scale_factor = 1.05
            if event.angleDelta().y() > 0:
                self.scale(scale_factor, scale_factor)
                self.scale_factor *= scale_factor
            else:
                self.scale(1.0 / scale_factor, 1.0 / scale_factor)
                self.scale_factor *= 1.0 / scale_factor

            self.zoom_rect = self.mapToScene(self.viewport().rect())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Alt and not self.single_image_mode:
            self.toggle_selectable(not self.items_selectable)
        elif event.key() == Qt.Key_Delete and self.scene.selectedItems() != 0:
            for item in self.scene.selectedItems():
                self.scene.removeItem(item)
                self.pixmaps.remove(item)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Alt and not self.single_image_mode:
            self.toggle_selectable(False)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.impath = 'test/'
        self.size_org=(160,120)
        self.size_res=(640,480)
        self.r_image_loc=[50,620]
        self.l_image_loc=[120,200]
        self.pre_m='VST'
        self.outpath='res/'
        if not os.path.exists(self.outpath):os.makedirs(self.outpath)
        #self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        #self.ST_path='weights/003_realSR_BSRGAN_DFO_s64w8_SwinIR-M_x4_GAN.pth'
        self.setWindowTitle("SISR")
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)
        self.pre_page=self.ui.ui_pages.page_1
        # buttons
        self.ui.toggle_button.clicked.connect(self.toggle_button)
        self.ui.btn_1.clicked.connect(self.show_page_1)
        self.ui.btn_2.clicked.connect(self.show_page_2)
        self.ui.btn_3.clicked.connect(self.show_page_3)
        self.ui.btn_4.clicked.connect(self.show_page_4)
        self.ui.btn_5.clicked.connect(self.show_page_5)
        #self.ui.settings_btn.clicked.connect(self.show_page_3)
        # select
        self.ui.ui_pages.button_file.clicked.connect(self.select_file)
        self.ui.ui_pages.button_2.clicked.connect(self.select_file)
        self.ui.ui_pages.button_32.clicked.connect(self.select_file)
        self.ui.ui_pages.button_42.clicked.connect(self.select_file)
        self.ui.ui_pages.button_52.clicked.connect(self.select_file)
        # image viewer widget
        #self.ui.imageViewer = QCImageViewer()
        #self.ui.imageViewer.setStyleSheet("border-width: 0px; border-style: solid")
        self.show()
    # image
    def show_image(self, path = None):
        if path is None:
            return
        self.ui.imageViewer.load_single_image(path)
        self.ui.imageViewer.setFocus(Qt.OtherFocusReason)
    # file action
    def select_file(self):
        # open file
        FileDialog = QFileDialog(self, 'Choose Image', './', 'png(*.png)')
        FileDialog.setAcceptMode(QFileDialog.AcceptOpen)
        FileDirectory = FileDialog.getOpenFileNames(FileDialog, 'Select a LR Image', './', 'png(*.png)')
        FileDirectory = str(FileDirectory[0]).replace('[', '').replace(']', '').replace('\'', '')
        self.impath='test/'+os.path.split(FileDirectory)[-1]
        #self.impath=os.path.split(self.impath)[0][-12:]+'/'+os.path.split(self.impath)[-1]
        #print(self.impath);input()
        image=cv2.imread(self.impath)
        if not os.path.exists(self.impath):return
        (h,w,c)=image.shape
        #img = cv2.resize(image, (160, 120))
        frame = QImage(image, w,h, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        item11 = QGraphicsPixmapItem(pix)
        scene11 = QGraphicsScene()  # 创建场景
        scene11.addItem(item11)
        view11=QGraphicsView(self.pre_page)
        view11.resize(400, 400)
        view11.move(self.l_image_loc[1],self.l_image_loc[0])
        view11.setScene(scene11)
        view11.show()

        p=self.generate()

        if not os.path.exists(p):return
        image=cv2.imread(p)
        #if image==None:return
        #print(image.shape);input()
        (h,w,c)=image.shape
        #if h!=480 or w!=640:img =cv2.resize(image, (640, 480),interpolation=cv2.INTER_LANCZOS4)
        #(h,w,c)=image.shape
        #cv2.resize
        frame2 = QImage(image,w,h, QImage.Format_RGB888)
        pix2= QPixmap.fromImage(frame2)
        item12= QGraphicsPixmapItem(pix2)
        scene12= QGraphicsScene()  # 创建场景
        scene12.addItem(item12)
        view12=QGraphicsView(self.pre_page)
        view12.resize(800, 600)
        view12.move(self.r_image_loc[1],self.r_image_loc[0])
        view12.setScene(scene12)
        view12.show()
        # frame = QImage(img, 160,120, QImage.Format_RGB888)
        # pix = QPixmap.fromImage(frame)
        # self.item11 = QGraphicsPixmapItem(pix)
        # self.scene11 = QGraphicsScene()  # 创建场景
        # self.scene11.addItem(self.item11)
        # self.view11=QGraphicsView(self.pre_page)
        # self.view11.setScene(self.scene11)
        # self.view11.show()
        #self.show_image(self.impath)
        #print(self.impath)
        return
    # def change_text(self):
    #     text = self.ui.ui_pages.lineEdit.text()
    #     new_text = "Olá, " + text
    #     self.ui.ui_pages.label_3.setText(new_text)
    # Reset BTN Selection
    def reset_selection(self):
        for btn in self.ui.left_menu.findChildren(QPushButton):
            try:
                btn.set_active(False)
            except:
                pass
    # Btn home function
    def show_page_1(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.page_1)
        self.ui.btn_1.set_active(True)
        self.pre_page=self.ui.ui_pages.page_1
        self.pre_m='VST'
    # Btn widgets function
    def show_page_2(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.page_2)
        self.ui.btn_2.set_active(True)
        self.pre_page=self.ui.ui_pages.page_2
        self.pre_m='MANet'
    # Btn pase gettings
    def show_page_3(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.page_3)
        self.ui.settings_btn.set_active(True)
        self.pre_page=self.ui.ui_pages.page_3
        self.pre_m='DAN'
    def show_page_4(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.page_4)
        self.ui.settings_btn.set_active(True)
        self.pre_page=self.ui.ui_pages.page_4
        self.pre_m='SwinTransformer'
    def show_page_5(self):
        self.reset_selection()
        self.ui.pages.setCurrentWidget(self.ui.ui_pages.page_5)
        self.ui.settings_btn.set_active(True)
        self.pre_page=self.ui.ui_pages.page_5
        self.pre_m='EDSR'
    # Toggle button
    def toggle_button(self):
        # Get menu width
        menu_width = self.ui.left_menu.width()
        # Check with
        width = 50
        if menu_width == 50:
            width = 240
        # Start animation
        self.animation = QPropertyAnimation(self.ui.left_menu, b"minimumWidth")
        self.animation.setStartValue(menu_width)
        self.animation.setEndValue(width)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutCirc)
        self.animation.start()
    # make images
    def generate(self):
        par=self.pre_m
        # print images
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
        elif par=='EDSR':
            image_p=self.EDSR()
        #self.label_rest.setStyleSheet("border: 2px solid red")
        #self.show()
        print('Generating Finish!')
        return image_p
    # swin-transformer
    def swintransformer(self):
        # scale=4
        # model = net(upscale=4, in_chans=3, img_size=64, window_size=8,
        #             img_range=1., depths=[6, 6, 6, 6, 6, 6], embed_dim=180, num_heads=[6, 6, 6, 6, 6, 6],
        #             mlp_ratio=2, upsampler='nearest+conv', resi_connection='1conv')
        # pretrained_model = torch.load(self.ST_path)
        # param_key_g = 'params_ema'
        # model.load_state_dict(pretrained_model[param_key_g] if param_key_g in pretrained_model.keys() else pretrained_model, strict=True)
        # model.eval()
        # model = model.to(self.device)
        # img_lq=cv2.imread(self.impath, cv2.IMREAD_COLOR).astype(np.float32) / 255.
        # img_lq = np.transpose(img_lq if img_lq.shape[2] == 1 else img_lq[:, :, [2, 1, 0]], (2, 0, 1))
        # img_lq = torch.from_numpy(img_lq).float().unsqueeze(0).to(self.device)
        # window_size=8
        # #print(img_lq);input()
        # with torch.no_grad():
        #     # pad input image to be a multiple of window_size
        #     _, _, h_old, w_old = img_lq.size()
        #     h_pad = (h_old // window_size + 1) * window_size - h_old
        #     w_pad = (w_old // window_size + 1) * window_size - w_old
        #     img_lq = torch.cat([img_lq, torch.flip(img_lq, [2])], 2)[:, :, :h_old + h_pad, :]
        #     img_lq = torch.cat([img_lq, torch.flip(img_lq, [3])], 3)[:, :, :, :w_old + w_pad]
        #     output = model(img_lq)
        #     output = output[..., :h_old * scale, :w_old * scale]
        # output = output.data.squeeze().float().cpu().clamp_(0, 1).numpy()
        # output = np.transpose(output[[2, 1, 0], :, :], (1, 2, 0))
        # output = (output * 255.0).round().astype(np.uint8)
        # #plt.imshow(output);input()
        # p=self.outpath+'ST.png'
        # #print(p,output);input()
        # cv2.imwrite(p, output)
        #print(self.outpath+'ST_'+os.path.split(self.impath)[-1]);input()
        return self.outpath+'SwinIR'+os.path.split(self.impath)[-1]
    # DAN
    def DAN(self):
        return self.outpath+os.path.split(self.impath)[-1][:-4]+'_x4.png'
    # MANet
    def MANet(self):
        return self.outpath+os.path.split(self.impath)[-1]
    # VST
    def VST(self):
        # m= VSTm.VST(img_size=(120, 160), patch_size=1, in_chans=3,
        #             embed_dim=36, depths=[6, 6, 6, 6],
        #             num_heads=[6, 6, 6, 6, 6, 6, 6, 6],
        #             window_size=7, mlp_ratio=4.,
        #             qkv_bias=True, qk_scale=None, drop_rate=0.,
        #             attn_drop_rate=0., drop_path_rate=0.1,
        #             norm_layer=nn.LayerNorm, ape=False,
        #             patch_norm=True, use_checkpoint=False,
        #             upscale=4, img_range=1., upsampler='',
        #             resi_connection='1conv')
        # checkpoint = torch.load('weights/m_VST.pth')
        # m.load_state_dict(checkpoint['net'])
        # tmp=cv2.imread(self.impath)
        # with torch.no_grad():
        #         x=torch.Tensor(tmp).unsqueeze(0).permute(0, 3, 1, 2)
        #         y=m(x)
        #         y=y.permute(0,2,3,1).cpu().numpy()[0]
        #         p=self.outpath+'VST.png'
        #         cv2.imwrite(p,y)
        return self.outpath+'VST_'+os.path.split(self.impath)[-1]
    def EDSR(self):
        return self.outpath+'EDSR_'+os.path.split(self.impath)[-1]

app = QApplication(sys.argv)
app.setWindowIcon(QIcon("icons/1.png"))
window = MainWindow()
sys.exit(app.exec())