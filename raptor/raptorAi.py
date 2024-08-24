import torch
import cv2
import numpy as np
from time import time
import pygame
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog, QSplashScreen, QMessageBox, QMainWindow, QAction, QStyle
import sys
import os
import time

def resource_path(relative_path):
    """Get absolute path to resource, works for development and PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class ConfigWindow(QtWidgets.QWidget):
    def __init__(self, detector, main_window):
        super().__init__()
        self.detector = detector
        self.main_window = main_window
        self.initUI()

    def initUI(self):
        """Initialize the User Interface for the configuration window"""
        self.setWindowTitle('Configuration')
        settings_icon = self.style().standardIcon(QtWidgets.QStyle.SP_ComputerIcon)
        self.setWindowIcon(settings_icon)
        self.setFixedWidth(400)

        layout = QtWidgets.QVBoxLayout()

        # Confidence Threshold
        conf_layout = QtWidgets.QHBoxLayout()
        self.conf_threshold_label = QtWidgets.QLabel("Confidence Threshold:")
        conf_layout.addWidget(self.conf_threshold_label)

        self.conf_threshold_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.conf_threshold_slider.setRange(0, 100)
        self.conf_threshold_slider.setValue(int(self.detector.conf_threshold * 100))
        self.conf_threshold_slider.valueChanged.connect(self.update_conf_threshold)
        conf_layout.addWidget(self.conf_threshold_slider)
        layout.addLayout(conf_layout)

        # Triggered Items
        self.triggered_items_label = QtWidgets.QLabel("Triggered Items:")
        layout.addWidget(self.triggered_items_label)

        self.triggered_items_list = QtWidgets.QListWidget()
        self.triggered_items_list.addItems(self.detector.triggered_items)
        layout.addWidget(self.triggered_items_list)

        # Buttons to add or remove items
        button_layout = QtWidgets.QHBoxLayout()
        self.add_item_button = QtWidgets.QPushButton("Add Item")
        self.add_item_button.clicked.connect(self.add_item)
        button_layout.addWidget(self.add_item_button)

        self.remove_item_button = QtWidgets.QPushButton("Remove Item")
        self.remove_item_button.clicked.connect(self.remove_item)
        button_layout.addWidget(self.remove_item_button)
        layout.addLayout(button_layout)

        # Alarm Sound
        self.alarm_sound_label = QtWidgets.QLabel("Alarm Sound:")
        layout.addWidget(self.alarm_sound_label)

        self.current_alarm_sound_input = QtWidgets.QLineEdit(self)
        self.current_alarm_sound_input.setText(self.detector.alarm_sound_path)
        self.current_alarm_sound_input.setReadOnly(True)
        layout.addWidget(self.current_alarm_sound_input)

        self.alarm_sound_button = QtWidgets.QPushButton("Choose Alarm Sound")
        self.alarm_sound_button.clicked.connect(self.choose_alarm_sound)
        layout.addWidget(self.alarm_sound_button)

        # Camera Source Selection
        self.camera_source_label = QtWidgets.QLabel("Camera Source:")
        layout.addWidget(self.camera_source_label)

        self.camera_source_combobox = QtWidgets.QComboBox()
        self.camera_source_combobox.addItem("Webcam")
        self.camera_source_combobox.addItem("IP Camera")
        self.camera_source_combobox.currentIndexChanged.connect(self.update_camera_source)
        layout.addWidget(self.camera_source_combobox)

        # IP Camera URL
        self.ip_camera_url_label = QtWidgets.QLabel("IP Camera URL:")
        layout.addWidget(self.ip_camera_url_label)

        # IP Camera URL Input
        self.ip_camera_url_input = QtWidgets.QLineEdit(self)
        self.ip_camera_url_input.setText("http://220.233.144.165:8888/mjpg/video.mjpg")  # default URL
        layout.addWidget(self.ip_camera_url_input)
        self.ip_camera_url_input.setReadOnly(True)

        self.ip_camera_url_input.textChanged.connect(self.update_ip_camera_url)

        # Set default camera source in dropdown
        if self.main_window.camera_source == "IP Camera":
            self.camera_source_combobox.setCurrentIndex(1)
            self.ip_camera_url_input.setReadOnly(False)
        else:
            self.camera_source_combobox.setCurrentIndex(0)
            self.ip_camera_url_input.setReadOnly(True)

        # Apply Button
        apply_button = QtWidgets.QPushButton("Apply")
        apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(apply_button)

        self.setLayout(layout)

    def update_camera_source(self):
        """Update the read-only status of the IP Camera URL input based on selected camera source"""
        if self.camera_source_combobox.currentText() == "IP Camera":
            self.ip_camera_url_input.setReadOnly(False)
        else:
            self.ip_camera_url_input.setReadOnly(True)

        self.main_window.camera_source = self.camera_source_combobox.currentText()

    def update_conf_threshold(self, value):
        """Update the confidence threshold for object detection"""
        self.detector.conf_threshold = value / 100

    def add_item(self):
        """Add a new item to the list of triggered items"""
        item, ok = QtWidgets.QInputDialog.getText(self, "Add Triggered Item", "Enter item name:")
        if ok and item:
            self.triggered_items_list.addItem(item)
            self.update_triggered_items()

    def remove_item(self):
        """Remove selected item(s) from the list of triggered items"""
        selected_items = self.triggered_items_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Warning", "No item selected for removal.")
            return
        for item in selected_items:
            self.triggered_items_list.takeItem(self.triggered_items_list.row(item))
        self.update_triggered_items()

    def update_triggered_items(self):
        """Update the list of triggered items in the detector"""
        self.detector.triggered_items = [self.triggered_items_list.item(i).text() for i in range(self.triggered_items_list.count())]

    def choose_alarm_sound(self):
        """Allow the user to choose a new alarm sound"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose Alarm Sound", "", "Audio Files (*.wav *.mp3)", options=options)
        if file_name:
            self.detector.alarm_sound = pygame.mixer.Sound(file_name)
            self.detector.alarm_sound_path = file_name
            self.current_alarm_sound_input.setText(file_name)

    def update_ip_camera_url(self, text):
        """Update the IP camera URL in the main window"""
        self.main_window.ip_camera_url = text

    def apply_changes(self):
        """Apply all configuration changes"""
        self.main_window.start_detection()


class ObjectDetection:
    def __init__(self):
        """Initialize the object detection model and other settings"""
        self.model = self.load_model()
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)
        pygame.mixer.init()
        self.alarm_sound_path = resource_path("assets/alarm.wav")
        self.alarm_sound = pygame.mixer.Sound(self.alarm_sound_path)
        self.conf_threshold = 0.2
        self.triggered_items = ['knife', 'gun', 'scissors', 'hammer', 'box cutter']

    def load_model(self):
        """Load the pre-trained object detection model"""
        try:
            model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
            print("Model loaded successfully")
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            sys.exit(1)

    def score_frame(self, frame):
        """Perform object detection on a frame and return the results"""
        frame = [frame]
        results = self.model(frame)
        labels, cord = results.xyxyn[0][:, -1].numpy(), results.xyxyn[0][:, :-1].numpy()
        return labels, cord

    def class_to_label(self, x):
        """Convert class ID to label name"""
        return self.model.names[int(x)]

    def plot_boxes(self, results, frame):
        """Draw bounding boxes and labels on the frame"""
        labels, cord = results
        n = len(labels)
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        triggered_detected = False

        for i in range(n):
            row = cord[i]
            if row[4] >= self.conf_threshold:
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
                bgr = (0, 255, 0)
                label = self.class_to_label(labels[i])

                if label in self.triggered_items:
                    bgr = (0, 0, 255)
                    triggered_detected = True

                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        if triggered_detected:
            self.alarm_sound.play()

        return frame

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.detector = ObjectDetection()
        self.camera_source = "Webcam"
        self.ip_camera_url = "http://220.233.144.165:8888/mjpg/video.mjpg"
        self.config_window = None
        self.initUI()

        # Automatically start detection on startup
        self.start_detection()

    def initUI(self):
        self.setWindowTitle('RAPTOR: Hunt down every detail')
        self.setGeometry(100, 100, 800, 600)

        icon_path = resource_path('assets/window_icon.png')
        icon = QtGui.QIcon(icon_path)
        self.setWindowIcon(icon)

        self.video_label = QtWidgets.QLabel(self)
        self.video_label.setGeometry(10, 30, self.width() - 20, self.height() - 40)
        self.video_label.setAlignment(QtCore.Qt.AlignCenter)

        self.init_menu()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_video_label()

    def update_video_label(self):
        window_size = self.size()
        window_width, window_height = window_size.width(), window_size.height()
        video_aspect_ratio = 4 / 3  # Adjust if necessary to match the video aspect ratio

        # Calculate the new size maintaining the aspect ratio
        if window_width / window_height > video_aspect_ratio:
            new_width = int(window_height * video_aspect_ratio)
            new_height = window_height
        else:
            new_width = window_width
            new_height = int(window_width / video_aspect_ratio)

        # Center the video label
        x_offset = (window_width - new_width) // 2
        y_offset = (window_height - new_height) // 2

        # Set the geometry of the video label
        self.video_label.setGeometry(x_offset, y_offset, new_width, new_height)

    def init_menu(self):
        menubar = self.menuBar()

        config_action = QAction("Configuration", self)
        config_action.triggered.connect(self.show_config_window)
        menubar.addAction(config_action)

        help_menu = menubar.addMenu('Help')

        system_instructions_action = QAction('System Instructions', self)
        system_instructions_action.triggered.connect(self.show_system_instructions)
        help_menu.addAction(system_instructions_action)

        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_config_window(self):
        if self.config_window is None:
            self.config_window = ConfigWindow(self.detector, self)
        self.config_window.show()

    def show_system_instructions(self):
        instructions_msg = QMessageBox(self)
        instructions_msg.setIcon(QMessageBox.Information)
        instructions_msg.setText(
            "Object Detection Application\n\n"
            "1. Raptor will Start automatically:\n"
            "   - 'Webcam' by default is selected, the application will use your computer's default webcam.\n"
            "   - If 'IP Camera' is selected, the application wasn't able to access your webcam, \n" 
                " and will use a Default URL for the IP camera stream.\n\n"
            "2. Configuration: Opens a window to configure detection settings such as:\n"
            "   - Confidence threshold: Adjust the sensitivity of the detection.\n"
            "   - Triggered items: Add or remove items that should trigger the alarm.\n"
            "   - Alarm sound: Choose a custom sound to play when a triggered item is detected.\n"
            "   - Camera Source: Select between 'Webcam' or 'IP Camera'. If 'IP Camera' is selected, "
            " a default IP is used. You can provide a valid URL to stream video from an IP camera.\n"
            "   - Apply button: Applies all changes immediately\n"
        )
        instructions_msg.setWindowTitle("System Instructions")
        instructions_msg.setFixedWidth(600)
        instructions_msg.exec_()

    def show_about(self):
        about_msg = QMessageBox(self)
        about_msg.setIcon(QMessageBox.Information)
        about_msg.setText(
            "RAPTOR AI is an intelligent object detection system designed to enhance safety \n "
            "by identifying potentially hazardous items in real-time. \n"
            "It offers reliable monitoring for various environments, \n"
            " making it an essential tool for maintaining security."
            "RAPTOR is a Computer vision project powered by Pytorch and OpenCV.\n"
            "RAPTOR is developed by Noah Bibin Markose.\n"
            "This is a submission for the Premier's Coding Challenge 2024 #digitalinnovationqld"
        )
        about_msg.setWindowTitle("About")
        about_msg.setFixedWidth(600)
        about_msg.exec_()

    def start_detection(self):
        self.timer.stop()

        if self.camera_source == "Webcam":
            try:
                self.cap = cv2.VideoCapture(0)
                if not self.cap.isOpened():
                    raise Exception("Webcam not accessible.")
            except:
                self.camera_source = "IP Camera"
                self.start_detection()
                return

        if self.camera_source == "IP Camera":
            self.cap = cv2.VideoCapture(self.ip_camera_url)

        self.timer.start(1000 // 30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            results = self.detector.score_frame(frame)
            frame = self.detector.plot_boxes(results, frame)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QtGui.QImage(frame_rgb.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
            pixmap = QtGui.QPixmap.fromImage(convert_to_qt_format)
            self.video_label.setPixmap(pixmap.scaled(self.video_label.width(), self.video_label.height(), QtCore.Qt.KeepAspectRatio))

    def closeEvent(self, event):
        self.timer.stop()
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        if self.config_window is not None:
            self.config_window.close()  # Close the configuration window if it's open
        super().closeEvent(event)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    splash_image_path = resource_path('assets/RaptorAIsplashscreen.jpg')
    splash_pix = QtGui.QPixmap(splash_image_path)
    splash = QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()

    time.sleep(2)  # Display the splash screen for 2 seconds

    main_window = MainWindow()
    main_window.show()

    splash.finish(main_window)

    sys.exit(app.exec_())
