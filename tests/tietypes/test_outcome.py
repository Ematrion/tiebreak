from tiebreaker import OutCome


def test_outcome_duality():
    for v in OutCome:
        assert v == v.dual().dual()
