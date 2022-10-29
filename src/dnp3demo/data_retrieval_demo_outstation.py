import cmd
import logging
import random
import sys

from datetime import datetime
from pydnp3 import opendnp3, openpal
# from master import MyMaster, MyLogger, AppChannelListener, SOEHandler, MasterApplication
# from ..dnp3_python.master import command_callback, restart_callback

# from dnp3_python import asiodnp3 as asiodnp3

# from master_cmd import MasterCmd
# from master_new import MasterCmdNew
# from ..dnp3_python.master_new import MyMasterNew, MyLogger, AppChannelListener
# from outstation_cmd import OutstationCmd
# from src.dnp3_python.outstation_new import MyOutStationNew
from dnp3_python.dnp3station.outstation_new import MyOutStationNew
# from dnp3_python import visitors
# from src.dnp3_python.dnp3station.outstation_new import MyOutStationNew


from time import sleep

import datetime

stdout_stream = logging.StreamHandler(sys.stdout)
stdout_stream.setFormatter(logging.Formatter('%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s'))

_log = logging.getLogger(__name__)
_log = logging.getLogger("data_retrieval_demo_outstation")
# _log.addHandler(stdout_stream)
_log.setLevel(logging.DEBUG)
# _log.setLevel(logging.WARNING)
# _log.setLevel(logging.ERROR)


def main():
    # cmd_interface_master = MasterCmdNew()
    # master_application = MyMasterNew(log_handler=MyLogger(),
    #                                  listener=AppChannelListener(),
    #                                  soe_handler=SOEHandler(),
    #                                  master_application=MasterApplication())
    # master_application = MyMasterNew()
    # _log.debug('Initialization complete. Master Station in command loop.')
    outstation_application = MyOutStationNew()
    outstation_application.start()
    _log.debug('Initialization complete. OutStation in command loop.')

    count = 0
    while count < 3:
        sleep(5)  # Note: hard-coded, master station query every 1 sec.

        count += 1
        print(datetime.datetime.now(), "============count ", count, )

        # plan: there are 3 AnalogInput Points,
        # outstation will randomly pick from
        # index 0: [4.0, 7.0, 2.0]
        # index 1: [14.0, 17.0, 12.0]
        # index 1: [24.0, 27.0, 22.0]

        # outstation update point value (slower than master station query)
        if count % 3 == 1:
            point_values_0 = [4.8, 7.8, 2.8]
            point_values_1 = [14.1, 17.1, 12.1]
            point_values_2 = [24.2, 27.2, 22.2]
            point_values_0 = [val + random.random() for val in point_values_0]
            point_values_1 = [val + random.random() for val in point_values_1]
            point_values_2 = [val + random.random() for val in point_values_2]
            for i, pts in enumerate([point_values_0, point_values_1, point_values_2]):
                p_val = random.choice(pts)
                print(f"====== Outstation update index {i} with {p_val} at {datetime.datetime.now()}")
                outstation_application.apply_update(opendnp3.Analog(value=float(p_val),
                                                                    flags=opendnp3.Flags(24),
                                                                    time=opendnp3.DNPTime(3094)), i)

        # update binaryInput value as well
        if count % 3 == 1:
            point_values_0 = [True, False]
            point_values_1 = [True, False]
            point_values_2 = [True, False]
            for i, pts in enumerate([point_values_0, point_values_1, point_values_2]):
                p_val = random.choice(pts)
                print(f"====== Outstation update index {i} with {p_val}")
                outstation_application.apply_update(opendnp3.Binary(True), i)

    _log.debug('Exiting.')
    # cmd_interface_outstation.do_quit("something")
    # cmd_interface_master.do_quit("something")
    # quit()
    # quit()
    # TODO: shutdown gracefully
    outstation_application.shutdown()
    # del outstation_application


if __name__ == '__main__':
    main()

