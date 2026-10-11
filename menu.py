from registry import system_commands
import os


class DiagnosticMenu:

    def __init__(self):
        self.available_test_options = {}

        current_dir = os.path.dirname(os.path.abspath(__file__))
        tests_path = os.path.join(current_dir, "tests")
        files_availabe = os.listdir(tests_path)
        clean_list = [os.path.splitext(f)[0] for f in files_availabe]

        for index, file_name in enumerate(clean_list, 1):
            self.available_test_options[str(index)] = file_name

    def show_test_options(self):
        test_lines = [f"{key}: {value}" for key, value in self.available_test_options.items()]
        return "\n".join(test_lines)
    
    def show_command_options(self):
        command_lines = [f"{key}: {data[0]}" for key, data in system_commands.items()]
        return "\n".join(command_lines)