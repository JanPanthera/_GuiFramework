# GuiFramework

GuiFramework is a powerful and user-friendly library for building UI applications in Python 3.12. Designed with simplicity and efficiency in mind, it leverages the `customtkinter` library to provide an enhanced experience for developers looking to create intuitive and dynamic interfaces.

## Features

- **Window Class**: A convenient wrapper around `customtkinter`'s CTk class, simplifying the creation and setup of windows for your applications.
- **Config Manager**: Utilizes Python's built-in config library for easy reading and writing of settings to a config file. It includes support for application-wide variables, enabling seamless access and modification across your project.
- **Custom Type Registration**: Allows for the registration of custom types (e.g., a Matrix class) with functions to convert these types to and from strings. This feature facilitates the straightforward persistence of custom data types in configuration files.
- **GUI Manager**: Empowers developers to define GUI layouts using JSON, significantly reducing the amount of code required in your GUI components. The GUI Manager handles the instantiation and organization of `customtkinter` and `tkinter` widgets based on your JSON definitions.

## Package Installation and Updates with update_package.bat

For convenience, the GuiFramework includes a Windows batch script update_package.bat which automates the packaging of the source files into a wheel and updates the installation in your local pip environment.
Requirements

Before running update_package.bat, make sure you have:

    Python 3.12 installed and properly added to your system's PATH.
    pip installed and up-to-date (you can update pip using python -m pip install --upgrade pip).

Using update_package.bat

The script is designed to be run from the Windows command prompt. It performs the following actions:

    Uninstalls the existing GuiFramework package if it's already installed.
    Builds a new .whl file from the source .py files located in the src directory.
    Finds the latest .whl file generated in the dist directory.
    Installs or updates the .whl file using pip.

To run the script, follow these steps:

    Open the command prompt.
    Navigate to the directory where update_package.bat is located.
    Execute the script by typing update_package.bat and pressing Enter.


Note: The update_package.bat script should be executed whenever changes are made to the source files and you wish to test the updated package. The script ensures that you always have the latest version of GuiFramework installed in your local Python environment for development and testing purposes.

## Getting Started ~ TODO
;-)