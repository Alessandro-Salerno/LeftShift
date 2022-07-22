class LeftShiftRequest:
    def __init__(self, content_type='leftshift-ping', content=''):
        self.content_type = content_type
        self.content      = content


class LeftShiftResponse:
    def __init__(self, content_type='leftshift-ok', content=''):
        self.content_type = content_type
        self.content      = content
