from integrations.policy.rllm_ppo_adapter import (
    PPOParams,
    RewardWeights,
    RouterEnv,
    RouterPPOAdapter,
    SimpleCategoricalPolicy,
    compute_reward,
    ppo_train,
)


def test_adapter_symbols_available() -> None:
    assert PPOParams is not None
    assert RewardWeights is not None
    assert RouterEnv is not None
    assert SimpleCategoricalPolicy is not None
    assert RouterPPOAdapter is not None
    assert callable(compute_reward)
    assert callable(ppo_train)
