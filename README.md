<div align="center">
  <br />
  <a href="https://github.com/vsedge/ModularQT">
    <img src="https://i.imgur.com/tynE3yq.png" alt="ModularQT" width="100">
  </a>
  <br />
  <h1>ModularQT</h1>
  <p>
    Effortlessly install your applications with a focus on silent and streamlined installation.
  </p>
</div>

## About 

ModularQT is designed to simplify the installation of desktop applications. Leveraging a modular specification approach, it allows for organized and efficient application deployment. The core application logic resides within the `main.py` script, and the build process is managed by `build.py`. 

A key feature is its ability to silently install multiple applications using administrative privileges and tools like `winget`, ensuring a seamless and hands-free setup. 

This version is a refresh of batch based [Modular](https://github.com/vsedge/Modular) Project designed to work with 24H2, features like choco package manager and scripts `MAS, Office 365, SpotX, Takeover` have been removed due to security reasons. 

[![ModularQT](https://i.imgur.com/Q8F9Tab.png)](https://i.imgur.com/Q8F9Tab.png)

### Prerequisites

* **Python:** Ensure you have Python installed on your desktop if you plan to build. You can download it from [python.org](https://www.python.org/).

* **Winget:** Ensure that the Windows Package Manager (`winget`) is installed and available on your system. It typically comes pre-installed on modern versions of Windows 10 and 11.

* **Administrative Privileges:** Running `ModularInstaller.exe` requires administrative privileges on your desktop to perform silent installations.


### Building from Source

1.**Clone the Repository**
   ```bash
   git clone https://github.com/vsedge/ModularQT
   cd ModularQT
```
2.**Config Spec File**

Ensure you are running the build script files from Desktop. ModularInstaller.spec contains the build config; note that by default, it requires Modular.ico
```
User/Desktop/
│
├── main.py                     # Core application script
├── build.py                    # Build script
├── ModularInstaller.spec       # PyInstaller specification file
├── Modular.ico                 # Icon file
│
└── dist/                       # Distribution directory
    └── ModularQT.exe           # Compiled executable
```
3.**Build ModularQT**
```py
python build.py
```
This script will read your modular specification file and compile it to an exe in the user/dist directory.

### Downloading a Pre-compiled Release
You can also download a pre-compiled release of ModularQT if one is available.

Go to the "Releases" of this [repository](https://github.com/vsedge/ModularQT/releases).

Look for the latest release and download the appropriate executable file (e.g., `ModularQT.exe`).

Run it. Ensure you grant it administrative privileges when prompted.
