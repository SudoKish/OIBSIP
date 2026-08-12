import json
import webbrowser


COMMAND_FILE = "commands.json"


def load_commands():

    try:

        with open(
            COMMAND_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        return {}

    except json.JSONDecodeError:

        print("Error: commands.json contains invalid JSON.")

        return {}


def execute_custom_command(command):

    commands = load_commands()

    command = command.lower().strip()

    for trigger, action in commands.items():

        if command == trigger.lower():

            print(
                f"Executing custom command: {trigger}"
            )

            webbrowser.open(action)

            return True

    return False


if __name__ == "__main__":

    while True:

        command = input(
            "\nEnter command (type exit to stop): "
        )

        if command.lower() == "exit":

            break

        if execute_custom_command(command):

            print("Command executed successfully.")

        else:

            print("Custom command not found.")