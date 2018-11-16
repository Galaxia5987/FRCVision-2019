import threading

from networktables import NetworkTables

from file import File


class NT:
    def __init__(self):
        self.file = File(lambda name: f'[NetworkTables Storage 3.0]\nstring "/Vision/{name}_name"={name}', 'values')

    # Network tables server IP
    def get_nt_server(self, team_number=5987):
        return "roboRIO-{}-FRC.local".format(team_number)

    def connectionListener(self, connected, info):
        """
        Callback for when network tables connect
        :param connected: Connected bool
        :param info: Connection info
        :return:
        """
        if connected:
            print("Success: {}".format(info))
        else:
            print("Fail: {}".format(info))

    def nt_table(self, name):  # create the table and load all persistent values
        """
        Initiates network table
        """
        NetworkTables.initialize(server=self.get_nt_server())
        NetworkTables.addConnectionListener(self.connectionListener, immediateNotify=True)
        table = NetworkTables.getTable('Vision')
        self.load_values(name)
        return table

    def set_item(self, table, key, value):
        """
        Summary: Add a value to SmartDashboard.

        Parameters:
            * table: The current network table.
            * key : The name the value will be stored under and displayed.
            * value : The information the key will hold.
        """
        table.setDefaultValue(key, value)  # TODO: test

    def get_item(self, table, key, default_value):
        """
        Summary: Get a value from SmartDashboard.

        Parameters:
            * table: The current network table.
            * key : The name the value is stored under.
            * default_value : The value returned if key holds none.
        """
        return table.getValue(key, default_value)  # TODO: test

    def load_values(self, name):  # load values from the associated file and add them to the table
        NetworkTables.loadEntries(self.file.get_filename(name), prefix='/Vision/' + name + '_')

    def save_values(self, name):  # save values from the table to the associated file
        NetworkTables.saveEntries(filename=self.file.get_filename(name), prefix='/Vision/' + name + '_')

    def close_table(self, name):  # save all persistent values and clean the table of other values
        self.save_values(name)
        NetworkTables.deleteAllEntries()
