import atexit

from networktables import NetworkTables
from termcolor import colored

from file import File


class NT:
    def __init__(self, name):
        """
        This is a class for handling all networktables operations, mainly starting a server and sending to and receiving
        variables from it.
        :param name: The name of the target
        """
        self.name = name
        self.prefix = '/Vision/' + self.name + '_'  # Prefix for working with files
        self.team_number = 5987  # Our team number, used for the server IP
        self.file = File(self.name, f'[NetworkTables Storage 3.0]\nstring "/Vision/{self.name}_name"={self.name}',
                         'values', 'nt')
        # The values file for the target, with a default value for when no such file exists
        server = self.get_nt_server()
        print(colored(f'Initiating network tables connection with {server}', 'blue'))
        NetworkTables.initialize(server=server)
        NetworkTables.addConnectionListener(self.connection_listener, immediateNotify=True)
        self.table = NetworkTables.getTable('Vision')  # Create our own table instead of clogging SmartDashboard
        atexit.register(self.save_values)

    # Network tables server IP
    def get_nt_server(self):
        return f"roboRIO-{self.team_number}-FRC.local"

    def connection_listener(self, connected, info):
        """
        Callback for when network tables connect
        :param connected: Connected bool
        :param info: Connection info
        """
        if connected:
            print(f'Success: {info}')
            self.load_values()
        else:
            print(f'Fail: {info}')

    def set_item(self, key, value):
        """
        Summary: Add a value to SmartDashboard.

        :param key: The name the value will be stored under and displayed.
        :param value: The information the key will hold.
        """
        self.table.setDefaultValue(key, value)

    def get_item(self, key, default_value):
        """
        Summary: Get a value from SmartDashboard.

        :param key: The name the value is stored under.
        :param default_value: The value returned if key holds none.
        :return: The value that the key holds, default_value if it holds none.
        """
        return self.table.getValue(key, default_value)

    def load_values(self):
        """
        Loads the target's values onto networktables, using its values file.
        Values files are found in the 'values' folder and have the .nt extension.
        """
        NetworkTables.loadEntries(self.file.get_filename(), prefix='/Vision/' + self.name + '_')

    def save_values(self):
        """
        Save the target's values from networktables, to its values file.
        Values files are found in the 'values' folder and have the .nt extension.
        """
        NetworkTables.saveEntries(self.file.get_filename(), prefix='/Vision/' + self.name + '_')
