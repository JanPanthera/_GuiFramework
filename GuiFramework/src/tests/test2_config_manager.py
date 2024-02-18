# test2_config_manager.py

import json
import customtkinter as ctk
from GuiFramework.src.utilities.config_manager import ConfigManager


def create_default_config():
    return {
        "Settings": {
            "use_high_dpi_scaling": "True",
            "ui_theme": "System",
            "ui_language": "English",
            "selected_languages": "English",
            "supported_languages": "Chinese,English,French,German,Italian,Japanese,Korean,Portuguese,Russian,Spanish",
            "input_path": "_input",
            "output_path": "_output",
            "dictionaries_path": "_dictionaries"
        },
        "TranslationSettings": {
            "whole_word_replacement": "False"
        },
        "SaveOnWindowClose": {
            "save_window_size": "True",
            "save_window_pos": "True",
            "save_selected_languages": "False"
        },
        "WindowGeometry": {
            "width": "1366",
            "height": "768",
            "pos_x": "0",
            "pos_y": "0"
        }
    }


def stringvar_saver(value):
    return value.get()


def stringvar_creator(root, value):
    return ctk.StringVar(root, value=value)

# -------------------------------------------------


class Matrix:
    def __init__(self, data):
        self.data = data


def matrix_saver(matrix):
    return json.dumps(matrix.data)


def matrix_creator(matrix_data_string):
    matrix_data = json.loads(matrix_data_string)
    return Matrix(matrix_data)
# -------------------------------------------------


def list_saver(list_value):
    return json.dumps(list_value)


def list_creator(list_string):
    return json.loads(list_string)


def test_config_manager():
    root = ctk.CTk()

    config_manager = ConfigManager(default_config_creator_func=create_default_config, config_path="GuiFramework/configs")

    config_manager.register_variable_type(ctk.StringVar, lambda value: stringvar_creator(root, value), stringvar_saver)
    config_manager.register_variable_type(Matrix, matrix_creator, matrix_saver)
    config_manager.register_variable_type(list, list_creator, list_saver)

    # Add a list variable
    my_list = [1, 2, 3, 4, 5]
    config_manager.add_variable("my_list", value=my_list, section="Settings")
    print("Added variable: my_list")
    print(config_manager.get_variable("my_list"))

    # Set the list variable
    new_list = [6, 7, 8, 9, 10]
    config_manager.set_variable("my_list", new_list)
    print("Set variable: my_list")
    print(config_manager.get_variable("my_list"))

    # Add a Matrix variable
    matrix = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    config_manager.add_variable("test_matrix", value=matrix, section="Settings")
    print("Added variable: test_matrix")
    print(config_manager.get_variable("test_matrix").data)

    # Set the Matrix variable
    new_matrix = Matrix([[10, 11, 12], [13, 14, 15], [16, 17, 18]])
    config_manager.set_variable("test_matrix", new_matrix)
    print("Set variable: test_matrix")
    print(config_manager.get_variable("test_matrix").data)

    # Add a StringVar variable
    config_manager.add_variable("test_stringvar", value=ctk.StringVar(root, value="test_value"), section="Settings")
    print("Added variable: test_stringvar")
    print(config_manager.get_variable("test_stringvar").get())

    # Set the StringVar variable
    config_manager.set_variable("test_stringvar", ctk.StringVar(root, value="new_test_value"))
    print("Set variable: test_stringvar")
    print(config_manager.get_variable("test_stringvar").get())

    # Test without section
    config_manager.add_variable("test_stringvar_no_section", value=ctk.StringVar(root, value="test_value"))
    print("Added variable: test_stringvar_no_section")
    print(config_manager.get_variable("test_stringvar_no_section").get())

    config_manager.set_variable("test_stringvar_no_section", ctk.StringVar(root, value="new_test_value"))
    print("Set variable: test_stringvar_no_section")
    print(config_manager.get_variable("test_stringvar_no_section").get())

    # plain old saving and loading
    config_manager.save_setting("Settings", "input_path", "new_input_path")
    print("Saved setting: input_path")

    print("Loading setting: input_path")
    print(config_manager.load_setting("Settings", "input_path"))

    # Test reset
    config_manager.reset_setting("Settings", "input_path")
    print("Reset setting: input_path")
    print(config_manager.load_setting("Settings", "input_path"))

    # Test reset all
    config_manager.reset_all_settings()
    print("Reset all settings")
    print(config_manager.load_setting("Settings", "input_path"))

    input("Press Enter to continue...")


if __name__ == "__main__":
    test_config_manager()