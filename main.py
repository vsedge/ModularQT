import sys
import subprocess
import ctypes
import os
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QCheckBox, QPushButton, QLabel, 
                            QGridLayout, QFrame, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(command):
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c {command}", None, 1)
        return True
    return False

def run_without_admin(command):
    batch_content = f"""
@echo off
set command={command}
start cmd /c "%command%"
    """
    with open('temp_command.bat', 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    subprocess.run(['explorer.exe', 'temp_command.bat'], shell=True)
    
    try:
        time.sleep(1)
        os.remove('temp_command.bat')
    except:
        pass

class PackageManagerThread(QThread):
    progress_update = pyqtSignal(str)
    progress_value = pyqtSignal(int)
    
    def __init__(self, apps_to_process, action="install"):
        super().__init__()
        self.apps_to_process = apps_to_process
        self.action = action
        self.total_apps = len(apps_to_process)
        self.current_app = 0

    def update_progress(self):
        self.current_app += 1
        progress = int((self.current_app / self.total_apps) * 100)
        self.progress_value.emit(progress)

    def run(self):
        self.current_app = 0
        self.progress_value.emit(0)

        spotify_app = next((app for app in self.apps_to_process if app["name"] == "Spotify"), None)
        other_apps = [app for app in self.apps_to_process if app["name"] != "Spotify"]

        if spotify_app and self.action == "install":
            self.progress_update.emit(f"Installing {spotify_app['name']}...")
            try:
                command = f'winget install -e -h --id {spotify_app["id"]} --accept-source-agreements --accept-package-agreements'
                run_without_admin(command)
                self.progress_update.emit(f"Started {spotify_app['name']} installation")
            except Exception as e:
                self.progress_update.emit(f"Failed to install {spotify_app['name']}: {str(e)}")
            self.update_progress()

        for app in other_apps:
            action_text = "Installing" if self.action == "install" else "Uninstalling"
            self.progress_update.emit(f"{action_text} {app['name']}...")
            
            try:
                if self.action == "install":
                    command = f'winget install -e -h --id {app["id"]} --silent --accept-source-agreements --accept-package-agreements'
                else:
                    command = f'winget uninstall -e -h --id {app["id"]} --silent'

                if not is_admin():
                    run_as_admin(command)
                else:
                    subprocess.run(command, shell=True, check=True)
                
                action_text = "installed" if self.action == "install" else "uninstalled"
                self.progress_update.emit(f"Successfully {action_text} {app['name']}")
            except subprocess.CalledProcessError:
                action_text = "install" if self.action == "install" else "uninstall"
                self.progress_update.emit(f"Failed to {action_text} {app['name']}")
            
            self.update_progress()

class AppCard(QFrame):
    def __init__(self, app_name, parent=None):
        super().__init__(parent)
        self.setObjectName("AppCard")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        self.checkbox = QCheckBox(app_name)
        self.checkbox.setFont(QFont("Segoe UI", 11))
        layout.addWidget(self.checkbox)
        
        self.checkbox.toggled.connect(self.update_selection)
    
    def update_selection(self, checked):
        self.setProperty("selected", checked)
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

class ModernInstaller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modular")
        self.setMinimumSize(900, 600)
        self.setup_ui()

    def setup_ui(self):
        self.apps = [
            {"name": "Spotify", "id": "Spotify.Spotify"},
            {"name": "Discord", "id": "Discord.Discord"},
            {"name": "Brave", "id": "Brave.Brave"},
            {"name": "Steam", "id": "Valve.Steam"},
            {"name": "7-Zip", "id": "7zip.7zip"},
            {"name": "Stremio", "id": "Stremio.Stremio"},
            {"name": "JPEGView", "id": "JPEGView.JPEGView"},
            {"name": "Visual C++ Redistributable", "id": "Microsoft.VCRedist.2015+.x64"},
            {"name": "Git", "id": "Git.Git"},
            {"name": "Python 3.10", "id": "Python.Python.3.10"},
            {"name": "Bitwarden", "id": "Bitwarden.Bitwarden"},
            {"name": "Mullvad VPN", "id": "MullvadVPN.MullvadVPN"},
            {"name": "Process Explorer", "id": "Microsoft.Sysinternals.ProcessExplorer"},
            {"name": "Visual Studio Code", "id": "Microsoft.VisualStudioCode"},
            {"name": "Trading View", "id": "TradingView.TradingViewDesktop"}
        ]

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        title = QLabel("Select applications to install")
        title.setFont(QFont("Segoe UI", 32, QFont.Weight.Light))
        main_layout.addWidget(title)

        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(10)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        self.app_cards = {}
        row = 0
        col = 0
        max_cols = 3

        for app in self.apps:
            card = AppCard(app["name"])
            self.app_cards[app["name"]] = card
            grid_layout.addWidget(card, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        main_layout.addWidget(grid_widget)

        progress_container = QWidget()
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setSpacing(8)
        progress_layout.setContentsMargins(0, 0, 0, 0)

        self.progress_label = QLabel("Ready to install")
        self.progress_label.setFont(QFont("Segoe UI", 11))
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        progress_layout.addWidget(self.progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        progress_layout.addWidget(self.progress_bar)

        main_layout.addWidget(progress_container)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.select_all)
        button_layout.addWidget(select_all_btn)
        
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_all)
        button_layout.addWidget(clear_btn)
        
        button_layout.addStretch()
        
        uninstall_btn = QPushButton("Uninstall Selected")
        uninstall_btn.clicked.connect(lambda: self.process_selected("uninstall"))
        button_layout.addWidget(uninstall_btn)
        
        install_btn = QPushButton("Install Selected")
        install_btn.clicked.connect(lambda: self.process_selected("install"))
        install_btn.setProperty("primary", True)
        button_layout.addWidget(install_btn)
        
        main_layout.addLayout(button_layout)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1f1f1f;
            }
            QWidget {
                background-color: transparent;
                color: #ffffff;
            }
            #AppCard {
                background-color: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 6px;
            }
            #AppCard:hover {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
            #AppCard[selected="true"] {
                background-color: rgba(0, 120, 212, 0.2);
                border: 1px solid #0078d4;
            }
            QCheckBox {
                spacing: 12px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border-radius: 4px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                background-color: transparent;
            }
            QCheckBox::indicator:hover {
                border: 1px solid rgba(255, 255, 255, 0.5);
                background-color: rgba(255, 255, 255, 0.1);
            }
            QCheckBox::indicator:checked {
                background-color: #0078d4;
                border: 1px solid #0078d4;
            }
            QCheckBox::indicator:checked:hover {
                background-color: #1884d7;
                border: 1px solid #1884d7;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.06);
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-family: 'Segoe UI';
                font-size: 13px;
                min-width: 100px;
                min-height: 32px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.08);
            }
            QPushButton[primary="true"] {
                background-color: #0078d4;
            }
            QPushButton[primary="true"]:hover {
                background-color: #1884d7;
            }
            QLabel {
                color: white;
            }
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 2px;
            }
        """)

    def select_all(self):
        for card in self.app_cards.values():
            card.checkbox.setChecked(True)

    def clear_all(self):
        for card in self.app_cards.values():
            card.checkbox.setChecked(False)

    def process_selected(self, action):
        selected_apps = [
            app for app in self.apps 
            if self.app_cards[app["name"]].checkbox.isChecked()
        ]

        if not selected_apps:
            self.progress_label.setText("Please select at least one application")
            return

        for card in self.app_cards.values():
            card.checkbox.setEnabled(False)

        self.progress_bar.setValue(0)

        self.manager_thread = PackageManagerThread(selected_apps, action)
        self.manager_thread.progress_update.connect(self.update_progress)
        self.manager_thread.progress_value.connect(self.progress_bar.setValue)
        self.manager_thread.finished.connect(lambda: self.process_finished(selected_apps))
        self.manager_thread.start()

    def update_progress(self, message):
        self.progress_label.setText(message)

    def process_finished(self, processed_apps):
        for card in self.app_cards.values():
            card.checkbox.setEnabled(True)
            if any(app["name"] == card.checkbox.text() for app in processed_apps):
                card.checkbox.setChecked(False)
        self.progress_label.setText("Operation completed!")

def main():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    app = QApplication(sys.argv)
    window = ModernInstaller()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()