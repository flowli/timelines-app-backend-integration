from .backend_interface import BackendInterface


class PrinterExample(BackendInterface):
    def deliver_timespan(self, timespan):
        print("ℹ️ PLEASE NOTE: THIS PLUGIN IS ONLY PRINTING TO CONSOLE")
        print(timespan)
