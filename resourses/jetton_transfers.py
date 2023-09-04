class JettonTranfer:
    def __init__(self, transfers_info):
        self.master = transfers_info["data"]["master"]
        self.source_owner = transfers_info["data"]["source_owner"]
        self.destination_owner = transfers_info["data"]["destination_owner"]
        self.amount = int(transfers_info["data"]["amount"])
