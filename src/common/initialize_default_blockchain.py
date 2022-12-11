from src.common.block import Block


def initialize_default_blockchain():
    # transaction_data_1 = {'timestamp': 1670710843.370897, 'method': 'POST', 'path': '/login', 'user_id': None}
    transaction_data_1_bytes = b"gAAAAABjlQY7ZhvC2JR7vsET398K0G1K_F8ywVTlUxJA5bYrUzhO634-D7sgJ2cRGOb4BR73V-AfdZdYpuMcfplJ4BTw0TSPNU2_FlLMHG_K4ILzrPpVg_sWt6k4SiRXtwQOgZADF09jwG5F-g8QD6UMqw0nI7YwVv71zrtvlz3ZlgSoA4LP-zbEYEGjOK8GbHKJBZEVHdmo"
    block_0 = Block(transaction=transaction_data_1_bytes)

    # transaction_data_2 = {'timestamp': 1670710945.718833, 'method': 'GET', 'path': '/food/get', 'user_id':
    # '09cdf815-9cda-4a87-8ae9-34c06f915278'}
    transaction_data_2_bytes = b"gAAAAABjlQahRB54VLno4l5AC-puJAGkKmFAsPYqWyhrmZN47R58ueD49lazhZHqrhRj0tSF41GbJt7wYUpZcUD_g6fi8W4R1oLxkUtcviBDH-4WazEec3zijoby7KyGgeAo5BQgCnzaPhlhpNjgyxlvW-aDERdudaUSpt8h3ZBpD6ZetKG0Z4Aj1GlvRVd4uf2EwPakL0IrOWS1dDTA_FDO0M0CVOZMoKGiLsCyAH3ShGAFq3WYAXicUDHHZOAv9YVAYMqcewNg"
    block_1 = Block(
        transaction=transaction_data_2_bytes,
        previous_block=block_0,
    )

    # transaction_data_3 = {'timestamp': 1670711012.514417, 'method': 'GET', 'path':
    # '/food/get/96099ba5-7aac-496d-81af-1a3fd93050c0', 'user_id': '09cdf815-9cda-4a87-8ae9-34c06f915278'}
    transaction_data_3_bytes = b"gAAAAABjlQbkFXsCJ78rIJ-EkbkEf-7Zm2SwWVU6VKw7Dp0OhRzxHwRU0wqIKWzzqxTJT4p_a1MlVYwnKjY3xiD3ZFr6-8YsxoBcqSD5gjydu8wK5LVZXX6sbAStdRE7Exigjk1bA0Ckc2iYHmQz8QVTj94xaZ_CDSA8dF8uQk_oE8KJgPY3JnYzcC-0dneFu6s1JUWLIHQsBgr4kUyG-QeYhtX0omhkDrfFfSiztopGyCBK4H_Kt0NyfWK3jbyLXL6yYz_o--H8rUq-qu1k-vY4WX9buGRhSLNExnO2Vp6MqycAAkyKIf0="
    block_2 = Block(
        transaction=transaction_data_3_bytes,
        previous_block=block_1,
    )
    return block_2
