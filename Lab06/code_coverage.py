import pytest
from daycare_fees import (
    extra_hours_fee,
    enrolment_allowed,
    pickup_status,
)


def test_unknown_age_group_raises_value_error():
    with pytest.raises(ValueError, match="unknown age group"):
        extra_hours_fee("school-age", 30, False)


def test_negative_hours_raise_value_error():
    with pytest.raises(ValueError, match="invalid hours"):
        extra_hours_fee("toddler", -1, False)


def test_no_fee_within_included_hours():
    assert extra_hours_fee("toddler", 20, False) == 0


def test_sibling_extra_hours_fee_for_toddler():
    assert extra_hours_fee("toddler", 31, True) == 9


def test_infant_fee_when_extra_hours_exceed_twenty():
    assert extra_hours_fee("infant", 45, False) == 550


def test_enrolment_allowed_when_immunisation_pending():
    assert enrolment_allowed(24, 0, True) is True


def test_enrolment_rejected_when_pending_and_under_twelve():
    assert enrolment_allowed(11, 5, True) is False


def test_enrolment_rejected_when_under_six_months():
    assert enrolment_allowed(5, 2, False) is False


def test_enrolment_allowed_when_vacancy_exists():
    assert enrolment_allowed(6, 1, False) is True


def test_pickup_on_time():
    assert pickup_status(30, True, True) == "on_time"


def test_pickup_late():
    assert pickup_status(8, False, False) == "late"


def test_pickup_overdue():
    assert pickup_status(10, True, True) == "overdue"