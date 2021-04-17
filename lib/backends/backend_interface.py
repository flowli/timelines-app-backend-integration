class BackendInterface:
    def deliver_timelines_event(self, event):
        """Delivers a Timelines event to the backend and raises an Error when it fails."""
        pass
