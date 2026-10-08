@pytest.mark.parametrize("hour", [2])
def test_T_MISSING_DISCOUNT_MAX_CAP(monkeypatch, hour):
    # Build a dynamic FakeNow with the hour value without using 'hour' in a class body
    FakeNow = type("FakeNow", (), {"hour": hour})
    class FakeDateTime:
        @classmethod
        def now(cls):
            return FakeNow

    monkeypatch.setattr("data.input_code.d06_complex_logic.datetime", FakeDateTime)
    res = DiscountEngine.calculate_discount(1001.0, "PLATINUM", "ABC-123")
    assert res == 0.40