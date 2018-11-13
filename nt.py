import threading

from networktables import NetworkTables

import utils


# Network tables server IP
def get_nt_server(team_number=5987):
    return "roboRIO-{}-FRC.local".format(team_number)


# Thread condition for waiting on network tables to connect
cond = threading.Condition()
# Variable to check if condition was met
notified = False


def connectionListener(connected, info):
    """
    Callback for when network tables connect
    :param connected: Connected bool
    :param info: Connection info
    :return:
    """
    global notified
    if connected:
        print("Success: {}".format(info))
    else:
        print("Fail: {}".format(info))
    with cond:
        notified = True
        # Notify condition
        cond.notify()


def nt_table():  # create the table and load all persistent values
    """
    Initiates network table
    """
    global notified
    NetworkTables.initialize(server=get_nt_server())
    NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
    with cond:
        print("Waiting for connection...")
        if not notified:
            cond.wait()
    table = NetworkTables.getTable('Vision')
    return table


def set_item(table, key, value):
    """
    Summary: Add a value to SmartDashboard.

    Parameters:
        * table: The current network table.
        * key : The name the value will be stored under and displayed.
        * value : The information the key will hold.
    """
    table.setDefaultValue(key, value)  # TODO: test


def get_item(table, key, default_value):
    """
    Summary: Get a value from SmartDashboard.

    Parameters:
        * table: The current network table.
        * key : The name the value is stored under.
        * default_value : The value returned if key holds none.
    """
    return table.getValue(key, default_value)  # TODO: test


def load_values(table, name):  # load values from the associated file and add them to the table
    values = utils.load_file(name, 'values')
    for key, value in values.items():
        set_item(table, key, value)


def save_values(name):  # save values from the table to the associated file
    NetworkTables.saveEntries(filename=utils.get_filename(name, 'values'), prefix=name + '_')


def clear_table():  # save all persistent values and clean the table of other values
    NetworkTables.deleteAllEntries()
