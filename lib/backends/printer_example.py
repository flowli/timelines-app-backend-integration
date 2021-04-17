from .backend_interface import BackendInterface


class PrinterExample(BackendInterface):
    def deliver_timelines_event(self, event):
        print("ℹ️ PLEASE NOTE: THIS PLUGIN IS ONLY PRINTING TO CONSOLE")
        print(event)
