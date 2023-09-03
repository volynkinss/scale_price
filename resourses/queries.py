class queries:
    JETTON_NAME_QUERY = """
                query JettonName {
                        redoubt_jetton_master (where: {address: {_eq:"%s"}}) {
                            name
                        }
                    }
                """

    DEX_SWAPS_QUERY = """
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
    JETTON_MASTER_QUERY = """
            query jetton {
                redoubt_jetton_master(where: {address: {_eq:"%s"}}) {
                    address
                    symbol
                    decimals
                    admin_address
                }
            }
        """
