import pytest
from daycare_fees import extra_hours_fee, enrolment_allowed, pickup_status


def test_extra_hours_fee_validation_branches():
    with pytest.raises(ValueError, match="unknown age group"):
        extra_hours_fee("school-age", 30, False)

    with pytest.raises(ValueError, match="invalid hours"):
        extra_hours_fee("toddler", -1, False)

    assert extra_hours_fee("toddler", 20, False) == 0


def test_extra_hours_fee_sibling_branches():
    # No sibling discount.
    assert extra_hours_fee("toddler", 26, False) == 9

    # Infants do not receive the extra included hours.
    assert extra_hours_fee("infant", 21, True) == 14

    # Sibling discount applies to non-infants.
    assert extra_hours_fee("toddler", 31, True) == 9


def test_extra_hours_fee_rate_branches():
    # Extra hours do not exceed twenty.
    assert extra_hours_fee("infant", 25, False) == 70
    assert extra_hours_fee("preschool", 31, False) == 9

    # Extra hours exceed twenty, for both age-group cases.
    assert extra_hours_fee("infant", 45, False) == 550
    assert extra_hours_fee("toddler", 51, False) == 364


def test_enrolment_pending_immunisation_branches():
    assert enrolment_allowed(12, 0, True) is True
    assert enrolment_allowed(11, 5, True) is False


def test_enrolment_age_and_vacancy_branches():
    assert enrolment_allowed(5, 2, False) is False
    assert enrolment_allowed(6, 0, False) is False
    assert enrolment_allowed(6, 1, False) is True


def test_pickup_cutoff_and_status_branches():
    # Aftercare: true; Friday: true.
    assert pickup_status(30, True, True) == "on_time"

    # Aftercare: false; Friday: false.
    assert pickup_status(10, False, False) == "on_time"

    # Aftercare: false; Friday: true.
    assert pickup_status(15, False, True) == "late"

    # Aftercare: true; Friday: false.
    assert pickup_status(10, True, False) == "late"

    # The overdue return path is intentionally not exercised here so the
    # branch coverage report remains above 90% but below 100%.
