import datetime


class OperationDetails:
    def __init__(self, operation):
        self.msg_id = operation["msg_id"]
        self.time = operation["swap_time"]
        self.platform = operation["platform"]
        self.user = operation["swap_user"]
        self.src_token = operation["swap_src_token"]
        self.src_amount = operation["swap_src_amount"]
        self.dst_token = operation["swap_dst_token"]
        self.dst_amount = operation["swap_dst_amount"]

    def formatted_time(self):
        time_obj = datetime.datetime.strptime(self.time, "%Y-%m-%dT%H:%M:%S%z")
        formatted_time = time_obj.strftime("%d.%m.%Y %H:%M:%S")
        return formatted_time
