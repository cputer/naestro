from src.telemetry.metrics import LabeledCounter, LabeledGauge, SimpleCounter


def test_counter_and_gauge_reset():
    lc = LabeledCounter("c", "d")
    lc.inc("x")
    assert lc.get("x") == 1
    lc.reset()
    assert lc.get("x") == 0

    sc = SimpleCounter("s", "d")
    sc.inc()
    assert sc.get() == 1
    sc.reset()
    assert sc.get() == 0

    lg = LabeledGauge("g", "d")
    lg.set("x", 1.5)
    assert lg.get("x") == 1.5
    lg.reset()
    assert lg.get("x") == 0.0
