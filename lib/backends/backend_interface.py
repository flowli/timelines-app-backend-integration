class BackendInterface:
    def deliver_timelines_event(self, timespan):
        """Delivers a timespan to the backend and raises an Error when it fails."""
        pass
