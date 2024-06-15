import os
import sys
import shutil
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QMessageBox, QFileDialog, QPushButton, QTextEdit
from PyQt5.QtGui import QPixmap, QIcon, QBrush, QPalette, QPainter, QPainterPath, QTextCharFormat, QFont
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QTextFormat

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("나만의 냉장고")
        self.setGeometry(0, 0, 1200, 820)

        # 배경 이미지 파일 경로
        self.background_image_path = "background.png"
        self.circular_image_path = "Fridge/picture.png"
        self.image_paths = [
            "Fridge/image.png",
            "Fridge/save.png",
        ]

        # 이미지 로드
        self.background_img = self.load_image(self.background_image_path, (1200, 820))
        self.circular_img = self.load_image(self.circular_image_path, (500, 500))  # 크기를 키움
        self.image_labels = []  # 이미지 라벨들을 담을 리스트

        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 배경 이미지 설정
        self.draw_background_image()

        # 원형 이미지 버튼 생성
        if self.circular_img:
            self.circular_button = QPushButton(self.central_widget)
            self.circular_button.setIcon(QIcon(self.circular_img))
            self.circular_button.setIconSize(self.circular_img.size())
            self.circular_button.setGeometry(30, 150, self.circular_img.width(), self.circular_img.height())
            self.circular_button.setStyleSheet("border: none; background-color: transparent;")
            self.circular_button.clicked.connect(self.open_image_dialog)

        # 이미지 라벨들 생성 및 위치 설정
        label1 = QLabel(self.central_widget)
        label1.setGeometry(570, 30, 700, 700)
        pixmap1 = self.load_image(self.image_paths[0], (700, 700))
        if pixmap1:
            label1.setPixmap(pixmap1)
        self.image_labels.append(label1)

        # 저장 버튼 생성
        self.save_button = QPushButton("저장", self.central_widget)
        self.save_button.setGeometry(890, 730, 100, 60)
        self.save_button.clicked.connect(self.save_action)

        # 닫기 버튼 생성
        self.close_button = QPushButton("닫기", self.central_widget)
        self.close_button.setGeometry(1000, 730, 100, 60)
        self.close_button.clicked.connect(self.close_action)

        # 메모 입력 위젯 생성
        self.memo1_input = QTextEdit(self.central_widget)
        self.memo1_input.setGeometry(800, 100, 250, 50)
        self.set_cursor_style(self.memo1_input)  # 처음 한 번만 설정

        self.memo2_input = QTextEdit(self.central_widget)
        self.memo2_input.setGeometry(800, 200, 250, 50)
        self.set_cursor_style(self.memo2_input)  # 처음 한 번만 설정

        self.memo3_input = QTextEdit(self.central_widget)
        self.memo3_input.setGeometry(800, 310, 250, 50)
        self.set_cursor_style(self.memo3_input)  # 처음 한 번만 설정

        self.memo4_input = QTextEdit(self.central_widget)
        self.memo4_input.setGeometry(630, 470, 420, 200)
        self.set_cursor_style(self.memo4_input)  # 처음 한 번만 설정

    def set_cursor_style(self, text_edit):
        # 이미 설정된 폰트 크기가 있는지 확인 후 적용
        cursor = text_edit.textCursor()
        if not cursor.hasSelection():  # 선택된 텍스트가 없을 때만 설정
            format = QTextCharFormat()
            current_format = cursor.charFormat()
            font = QFont()
            if current_format.hasProperty(QTextFormat.FontPointSize):
                font_size = current_format.fontPointSize()
            else:
                font_size = 16  # 기본 폰트 크기 설정
            font.setPointSize(font_size)
            format.setFont(font)
            cursor.setCharFormat(format)
            text_edit.setTextCursor(cursor)

    def draw_background_image(self):
        if self.background_img:
            palette = self.palette()
            brush = QBrush(self.background_img)
            palette.setBrush(QPalette.Background, brush)
            self.setPalette(palette)

    def load_image(self, image_path, size):
        try:
            pixmap = QPixmap(image_path).scaled(size[0], size[1], Qt.KeepAspectRatio, Qt.SmoothTransformation)
            return pixmap
        except Exception as e:
            QMessageBox.critical(None, "이미지 로드 오류", f"이미지를 로드하는 동안 오류가 발생했습니다: {e}")
            return None

    def open_image_dialog(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_path:
            self.update_button_image(file_path)

    def update_button_image(self, image_path):
        pixmap = QPixmap(image_path).scaled(500, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        circular_pixmap = self.create_circular_pixmap(pixmap, 500)
        self.circular_button.setIcon(QIcon(circular_pixmap))
        self.circular_button.setIconSize(QSize(500, 500))
        self.circular_button.setFixedSize(QSize(500, 500))

        # 선택한 이미지를 저장할 경로 설정
        self.selected_image_path = image_path

    def create_circular_pixmap(self, pixmap, size):
        circular_pixmap = QPixmap(size, size)
        circular_pixmap.fill(Qt.transparent)  # 배경을 투명으로 설정

        painter = QPainter(circular_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # 원형 배경을 하얀색으로 채우기
        painter.setBrush(Qt.white)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(0, 0, size, size)

        # 클리핑 경로를 원형으로 설정
        path = QPainterPath()
        path.addEllipse(0, 0, size, size)
        painter.setClipPath(path)

        # 이미지를 중앙에 배치
        painter.drawPixmap((size - pixmap.width()) // 2, (size - pixmap.height()) // 2, pixmap)
        painter.end()

        return circular_pixmap

    def save_action(self):
        # 저장 버튼 클릭 시 메모와 이미지 저장
        memo_text1 = self.memo1_input.toPlainText().strip()
        memo_text2 = self.memo2_input.toPlainText().strip()
        memo_text3 = self.memo3_input.toPlainText().strip()
        memo_text4 = self.memo4_input.toPlainText().strip()

        # 모든 메모가 비어있는지 확인
        if not memo_text1 or not memo_text2 or not memo_text3 or not memo_text4:
            QMessageBox.warning(self, "저장 실패", "모든 메모를 입력해야 합니다.")
            return

        # 네 개의 메모 내용을 하나의 텍스트로 합치기
        combined_text = f"메모 1:\n{memo_text1}\n\n메모 2:\n{memo_text2}\n\n메모 3:\n{memo_text3}\n\n메모 4:\n{memo_text4}"

        # 텍스트 파일로 저장
        file_name = f"{memo_text1}.txt"
        file_path = os.path.join("saved_data", file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(combined_text)

        # 선택한 이미지 파일 복사해서 저장
        if hasattr(self, 'selected_image_path') and os.path.isfile(self.selected_image_path):
            image_file_name = f"{memo_text1}_image.png"  # 이미지는 PNG 형식으로 저장 예시
            image_save_path = os.path.join("saved_data", image_file_name)
            shutil.copyfile(self.selected_image_path, image_save_path)

            QMessageBox.information(self, "저장 완료", f"\'{memo_text1}\' 저장되었습니다.\n텍스트 파일 경로: {file_path}\n이미지 파일 경로: {image_save_path}")
        else:
            QMessageBox.warning(self, "저장 실패", "이미지 파일을 선택해주세요.")

    def close_action(self):
        # 닫기 버튼 클릭 시 수행할 동작을 여기에 구현
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())