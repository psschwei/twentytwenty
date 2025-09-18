#!/usr/bin/env python3

import sys
import time
import signal
import logging
import threading
import argparse
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, QAction,
                           QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox)
from PyQt5.QtCore import QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QFont, QCursor, QColor

# Configure logging (will be updated in main() based on debug flag)
logger = logging.getLogger(__name__)


class TimerSignals(QObject):
    break_time = pyqtSignal()
    timer_update = pyqtSignal(int)


class TwentyTwentyApp:
    def __init__(self, debug_mode=False):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.signals = TimerSignals()
        self.signals.break_time.connect(self.show_break_notification)
        self.signals.timer_update.connect(self.update_tray_icon)

        # Timer state
        self.timer_running = False
        self.minutes_remaining = 20
        self.break_dialog = None

        # Setup system tray
        self.setup_tray()

        # Setup main timer (checks every minute)
        self.main_timer = QTimer()
        self.main_timer.timeout.connect(self.timer_tick)

        # Debug mode from command line argument
        self.debug_mode = debug_mode

    def create_tray_icon(self, minutes_remaining):
        """Create a simple icon with minutes remaining"""
        pixmap = QPixmap(64, 64)

        # Set background color based on timer state
        if self.timer_running:
            pixmap.fill(QColor(46, 52, 64))  # Dark blue-gray background when active
        else:
            pixmap.fill(QColor(255, 255, 255))  # White background when inactive

        painter = QPainter(pixmap)
        painter.setFont(QFont('Arial', 24, QFont.Bold))

        # Change text color based on timer state and time remaining
        if not self.timer_running:
            painter.setPen(QColor(136, 136, 136))  # Gray text when inactive
        elif minutes_remaining <= 5:
            painter.setPen(QColor(255, 68, 68))  # Bright red when urgent
        elif minutes_remaining <= 10:
            painter.setPen(QColor(255, 170, 68))  # Bright orange when warning
        else:
            painter.setPen(QColor(68, 255, 68))  # Bright green when plenty of time

        painter.drawText(pixmap.rect(), 1, str(minutes_remaining))
        painter.end()

        return QIcon(pixmap)

    def setup_tray(self):
        """Setup system tray icon and menu"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            QMessageBox.critical(None, "Error", "System tray not available")
            sys.exit(1)

        self.tray_icon = QSystemTrayIcon()
        self.tray_icon.setIcon(self.create_tray_icon(20))
        self.tray_icon.setToolTip("20-20-20 Eye Break Timer")

        # Create tray menu
        tray_menu = QMenu()

        self.start_action = QAction("Start Timer", self.app)
        self.start_action.triggered.connect(self.start_timer)
        tray_menu.addAction(self.start_action)
        logger.debug("Start action created and connected")

        self.stop_action = QAction("Stop Timer", self.app)
        self.stop_action.triggered.connect(self.stop_timer)
        self.stop_action.setEnabled(False)
        tray_menu.addAction(self.stop_action)

        tray_menu.addSeparator()

        quit_action = QAction("Quit", self.app)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)

        # Enable left-click to show menu too
        self.tray_icon.activated.connect(self.tray_icon_activated)

        self.tray_icon.show()

    def tray_icon_activated(self, reason):
        """Handle tray icon clicks"""
        if reason == QSystemTrayIcon.Trigger:  # Left click
            # Show the context menu at cursor position
            self.tray_icon.contextMenu().popup(QCursor.pos())

    def start_timer(self):
        """Start the 20-minute timer"""
        logger.info("Starting 20-minute timer")
        self.timer_running = True
        self.minutes_remaining = 20

        # For testing: 1-second intervals instead of 60 seconds
        if self.debug_mode:
            self.main_timer.start(1000)  # 1 second for testing
            logger.debug("Timer started in debug mode (1-second intervals)")
        else:
            self.main_timer.start(60000)  # 60 seconds for production

        self.start_action.setEnabled(False)
        self.stop_action.setEnabled(True)

        self.update_tray_icon(20)
        logger.debug("Timer setup complete")

    def stop_timer(self):
        """Stop the timer"""
        self.timer_running = False
        self.main_timer.stop()
        self.minutes_remaining = 20

        self.start_action.setEnabled(True)
        self.stop_action.setEnabled(False)

        self.update_tray_icon(20)

    def timer_tick(self):
        """Called every minute (or 1 second in debug mode)"""
        if not self.timer_running:
            return

        self.minutes_remaining -= 1
        logger.debug(f"Timer tick - {self.minutes_remaining} minutes remaining")
        self.signals.timer_update.emit(self.minutes_remaining)

        if self.minutes_remaining <= 0:
            logger.info("Timer finished - triggering break")
            self.timer_running = False
            self.main_timer.stop()
            self.signals.break_time.emit()

    def update_tray_icon(self, minutes):
        """Update tray icon with remaining minutes"""
        self.tray_icon.setIcon(self.create_tray_icon(minutes))
        self.tray_icon.setToolTip(f"20-20-20 Timer: {minutes} minutes remaining")

    def show_break_notification(self):
        """Show break time notification"""
        # Show break dialog
        self.break_dialog = BreakDialog()
        self.break_dialog.finished.connect(self.break_finished)
        self.break_dialog.show()

    def break_finished(self):
        """Called when break dialog is closed"""
        self.start_action.setEnabled(True)
        self.stop_action.setEnabled(False)
        self.update_tray_icon(20)

    def quit_app(self):
        """Quit the application"""
        self.app.quit()

    def run(self):
        """Run the application"""
        return self.app.exec_()


class BreakDialog(QDialog):
    """Dialog shown during the 20-second break"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Eye Break Time")
        self.setFixedSize(400, 200)
        self.setModal(True)

        # Make it stay on top
        self.setWindowFlags(self.windowFlags() | 0x00008000)  # Qt.WindowStaysOnTopHint

        self.seconds_remaining = 20
        self.setup_ui()

        # Timer for countdown
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.countdown_tick)
        self.countdown_timer.start(1000)  # 1 second

    def setup_ui(self):
        """Setup the break dialog UI"""
        layout = QVBoxLayout()

        # Instructions
        instruction_label = QLabel("Time for a 20-second eye break!\nLook at something 20 feet away.")
        instruction_label.setStyleSheet("font-size: 14px; margin: 20px;")
        layout.addWidget(instruction_label)

        # Countdown
        self.countdown_label = QLabel("20 seconds remaining")
        self.countdown_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #0066cc;")
        layout.addWidget(self.countdown_label)

        # Done button (for early exit)
        self.done_button = QPushButton("Done Early")
        self.done_button.clicked.connect(self.accept)
        layout.addWidget(self.done_button)

        self.setLayout(layout)

    def countdown_tick(self):
        """Update countdown every second"""
        self.seconds_remaining -= 1

        if self.seconds_remaining <= 0:
            self.countdown_timer.stop()
            self.countdown_label.setText("Break complete!")
            self.done_button.setText("Start Next Timer")
            # Auto-close after 2 seconds
            QTimer.singleShot(2000, self.accept)
        else:
            self.countdown_label.setText(f"{self.seconds_remaining} seconds remaining")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='20-20-20 Eye Break Timer')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode (1-second intervals instead of 20-minute)')
    args = parser.parse_args()

    # Configure logging based on debug flag
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = TwentyTwentyApp(debug_mode=args.debug)

    # Allow Ctrl+C to work by processing events periodically
    timer = QTimer()
    timer.start(500)  # Check every 500ms
    timer.timeout.connect(lambda: None)  # Just process events

    sys.exit(app.run())


if __name__ == "__main__":
    main()