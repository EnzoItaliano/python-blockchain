from datetime import datetime

from src.common.block import Block, BlockHeader
from src.common.io_blockchain import BlockchainMemory


def initialize_default_blockchain(blockchain_memory: BlockchainMemory):
    timestamp_0 = datetime.timestamp(datetime.fromisoformat("2022-12-11 19:25:00.000"))
    signature_0 = "088e6327b518466c4bb8290f5fdc2ec05c06506b3ecfe5ae903c7b3e46a3a2a4e014a04ef365b146fcbedbd472c9fac612d030851792a1b55a9e7935993b6e0dfcfc4659bae18ae5166fe50f3e98b9719d7cfe6eedfe30cf6e6347fc72c3bea427713b293c4cf6deb96c74ade09245d98e1539951a5c5acdb461d1e64083fd6044b627e14b0f9c09cab9f1e24f2e34c84796d96598e77f94f672210982d1e9b78755088833cbd4027ac351d01af204e271b13a6f42c0743068daa338e5b15e8982b6b1ae2f14a932f87cae5f2d2b152f088dd92cc723d44051ef5c4f2539222d6bafad1bf04d0d036a7d51f57138a470fcf7fce7cf00a3fa6794fc7f69ee7502"
    transaction_data_0 = "gAAAAABjlk1UmYFGr3lB2MaQTphKwVi-WpCit75J31Yyevt6usOR8oynwrHtZ_bN3SWJqb9sw0_Q7oKWSx70H9_9gId-3mPwmRxWLwOGy-pstGM5M7OhxXLkCF1aqcPHriCi3VA7-nb1xzERpGQs9VCvMJoRHtUlK10wcji2s33EQeunUCfsZEQUXt7-PrjDjDTT6yVCgL0S"
    block_header_0 = BlockHeader(
        previous_block_hash="1111",
        timestamp=timestamp_0,
        noonce=2,
    )
    transaction_0 = {"signature": signature_0, "transaction_hash": transaction_data_0}
    block_0 = Block(block_header=block_header_0, transaction=transaction_0)

    # ---------------------------------------------------------------------------------------
    timestamp_1 = datetime.timestamp(datetime.fromisoformat("2022-12-11 20:25:00.000"))
    signature_1 = "2459bf13c46c3187753a9ca8cc371c459401cfa5e5ae7cbaf70e96635028b73d25b765fe05b21a6a562db6780974df5894cde2638f37a32c677aa286f80915085081eedf0bc4b5da4a849ab416bc50c7337fb2a521abd6382670c2e41dacee92a00b3f3f26179823c19dc7c4c8c9c2963160f12fb9976b4a164e14f7bf1ea19a633f6cc2ad6641b0b01dce8491f4623bc1bc86d1b282c4f9b332ab93d355333d9900ca9539ec4149720fe6abe05d87d29252b93cd65ef6fd425a66d7b2aecef1c1321169c57ec6e68c66229ce800a4ea4b4364c2c4e9ff950e279de8f32b3c2f4a44a788b9206541559a0cad39db082157eb41341b1b98065ea68a5c172ab7e1"
    transaction_data_1 = "gAAAAABjlk2yIbHyrTqn-EjgxInN_FxXINFudXqeFXnEl0on3UnRHxkc3vfdf2rCD2B-qjqbLehBI5rFbiPWWqaHtQnT8WR-KHgyXrcRdlMMHC_DA0Jq9bnS9N_BXPTNLGxkB2FxaiV3fbfcaasN4mNEivwBQHR4vx-f-OF8suw7lTfueNB0RKKLVMx_GkQ6FlQDykJRsCKqdjqoRz74wK9MBAEc7ImEyyq-obYx0UxeNOO2HWBQ1Sb_toMWyB-W42njWNy3lvn3"
    block_header_1 = BlockHeader(
        previous_block_hash=block_0.block_header.hash,
        timestamp=timestamp_1,
        noonce=3,
    )
    transaction_1 = {"signature": signature_1, "transaction_hash": transaction_data_1}
    block_1 = Block(
        block_header=block_header_1, transaction=transaction_1, previous_block=block_0
    )

    # ---------------------------------------------------------------------------------------
    timestamp_2 = datetime.timestamp(datetime.fromisoformat("2022-12-11 20:25:00.000"))
    signature_2 = "572f7ea86dada64252631cbf56de791fc9169f1cbad7e4adcc51b28330f8f2157d10422c45a29463022647fa35b441967073c3b9d49ba961922e3550dc09184795dcfb7132824bf9c51e99cc93abad21ce599f3bada8b8134d1b830602cdebadd4ef7c6db7a1b57019a3781d1369ad81bdce2ae93474f697c9168c5bcd4b7612afac243a78ba824b4414688b1fe1596eb8f7f8a4dbd080edd24633c1a8554684fd2a7176003ce003f197ab81f61d757cc755bddad650f8985bdd14c4b3aac27a09b260e89b710b68043e0e20808685fd6966f90e082a78a3470d060e03d30c56d26ac3a0b94040ffd0da16cff37319195700a9e0349402c9473361ca9f3f35d3"
    transaction_data_2 = "gAAAAABjlk3dS5uWSMs44Oj5NG7OP_r18ipdSLkepdvFMhC51gGV1C9t_Wu_AAarm6ADMRoi41tS-0W_SZa8jHGaTydwLI59h91gWA-9LazZ64sPglt2nCTqgKco4WrMq3cCn8alTlQj52MFZKe9ZVu9UXcSlqXFAgRBBpKGuwn7JFP1xmZ7mWRmnxvwy_47NTjFUo6e9Bv03dh5D4VipmDoAAz0ag2wIbU6SAjoQlO4rwgMhFQMMgMoYxkg8F96ZTRoW_Erv0c4"
    block_header_2 = BlockHeader(
        previous_block_hash=block_1.block_header.hash,
        timestamp=timestamp_2,
        noonce=4,
    )
    transaction_2 = {"signature": signature_2, "transaction_hash": transaction_data_2}
    block_2 = Block(
        block_header=block_header_2, transaction=transaction_2, previous_block=block_1
    )

    blockchain_memory.store_blockchain_in_memory(block_2)
