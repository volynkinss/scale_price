class queries:
    def jetton_name_query(self, address):
        query = (
            """
                query JettonName {
                        redoubt_jetton_master (where: {address: {_eq:"%s"}}) {
                            name
                        }
                    }
                """
            % address
        )
        return query

    def dex_swaps_query(self):
        query = """
                    query GetDexSwaps {
                            redoubt_dex_swaps {
                                msg_id
                                platform
                                swap_dst_token
                                swap_src_token
                                swap_dst_amount
                                swap_src_amount
                                swap_time
                                swap_user
                            }
                        }
                    """
        return query
