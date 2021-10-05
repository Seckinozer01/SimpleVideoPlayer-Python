from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,\
    QHBoxLayout,QVBoxLayout,QLabel,QSlider,QStyle,QSizePolicy,QFileDialog

import sys
from PyQt5.QtMultimedia import QMediaPlayer , QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon,QPalette
from PyQt5.QtCore import Qt , QUrl


class Window(QWidget):
    def __init__(self):
        super().__init__()




        self.setWindowTitle("Python Media Player")
        self.setGeometry(350,100,700,500)


        p = self.palette()
        p.setColor(QPalette.Window, Qt.black )
        self.setPalette(p)

        self.init_ui()

        self.show()

    def init_ui(self):
        self.mediaPlayer = QMediaPlayer(None,QMediaPlayer.VideoSurface)

        videowidget = QVideoWidget()

        openbutton = QPushButton("Open Video")
        openbutton.clicked.connect(self.open_file)


        self.playbtn = QPushButton()
        self.playbtn.setEnabled(False)
        self.playbtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playbtn.clicked.connect(self.play_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)


        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred , QSizePolicy.Maximum)


        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)

        hbox.addWidget(openbutton)
        hbox.addWidget(self.playbtn)
        hbox.addWidget(self.slider)


        vbox = QVBoxLayout()
        vbox.addWidget(videowidget)
        vbox.addLayout(hbox)
        vbox.addWidget(self.label)

        self.setLayout(vbox)

        self.mediaPlayer.setVideoOutput(videowidget)


        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)



    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self , "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playbtn.setEnabled(True)


    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()

    def mediastate_changed(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playbtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.playbtn.setIcon(
                self.style().standardIcon( QStyle.SP_MediaPlay )
            )


    def position_changed(self,position):
        self.slider.setValue(position)

    def duration_changed(self,duration):
        self.slider.setRange(0,duration)


    def set_position(self,position):
        self.mediaPlayer.setPosition(position)


app = QApplication(sys.argv)
window = Window()
sys.exit(app.exec_())
