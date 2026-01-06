import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer

IMAGE_FOLDER = "C:/Users/Administrator/Pictures/Saved Pictures/"
SLIDE_INTERVAL_MS = 5000

def get_images(folder):
    base_landscape_f = folder + "landscape/"
    base_portrait_f = folder + "portrait/"
    return {"landscape": [os.path.join(base_landscape_f, f) for f in os.listdir(base_landscape_f)
                          if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))],
            "portrait":  [os.path.join(base_portrait_f, f) for f in os.listdir(base_portrait_f)
                          if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp"))]
           }

class ScreenSaverWindow(QWidget):
    def __init__(self, geometry, image_paths):
        super().__init__()
        self.image_paths = image_paths
        self.setGeometry(geometry)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.setCursor(Qt.BlankCursor)

        self.label = QLabel(self)
        self.label.setGeometry(self.rect())
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("background-color: black")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_random_image)
        self.timer.start(SLIDE_INTERVAL_MS)

        self.show_random_image()

    def show_random_image(self):
        is_landscape = self.geometry().width() > self.geometry().height()
        path = random.choice(self.image_paths.get("landscape" if is_landscape else "portrait"))
        print(path)
        image = QPixmap(path).scaled(
            self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.label.setPixmap(image)

    def keyPressEvent(self, event):
        QApplication.quit()

    def mouseMoveEvent(self, event):
        QApplication.quit()

    def mousePressEvent(self, event):
        QApplication.quit()

def main():
    args = sys.argv[1:]  # exclude script path
    app = QApplication(sys.argv)
    image_paths = get_images(IMAGE_FOLDER)

    if not image_paths:
        print("No images found.")
        return

    # Handle SCR mode arguments
    if not args or args[0].lower() == '/s':
        # Start screensaver mode
        windows = []
        for screen in app.screens():
            # print(f"bb={screen.geometry()}")
            win = ScreenSaverWindow(screen.geometry(), image_paths)
            win.show()
            windows.append(win)
        sys.exit(app.exec_())

    elif args[0].lower().startswith('/c'):
        # Show configuration dialog (not implemented)
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.information(None, "설정", "이 스크린세이버는 설정 옵션이 없습니다.")
        sys.exit()

    elif args[0].lower().startswith('/p'):
        # Preview mode (not implemented)
        sys.exit()

if __name__ == "__main__":
    main()
