
import pytest  # type: ignore

from calculations import (
    calculate_mass_loss,
    calculate_weight_loss_corrosion_rate,
    calculate_electrochemical_corrosion_rate,
    calculate_inhibition_efficiency,
)


def test_calculate_mass_loss():
    assert calculate_mass_loss(10.00, 9.80) == pytest.approx(0.20)


def test_zero_mass_loss():
    assert calculate_mass_loss(10.0, 10.0) == 0.0


def test_final_mass_greater_than_initial_is_rejected():
    with pytest.raises(ValueError):
        calculate_mass_loss(9.80, 10.00)


def test_negative_mass_is_rejected():
    with pytest.raises(ValueError):
        calculate_mass_loss(-1.0, 0.0)


def test_string_input_is_rejected():
    with pytest.raises(TypeError):
        calculate_mass_loss("10.00", 9.80)


def test_nan_input_is_rejected():
    with pytest.raises(ValueError):
        calculate_mass_loss(float("nan"), 9.80)


def test_weight_loss_corrosion_rate():
    expected = (87.6 * 10) / (7.85 * 10 * 24)

    result = calculate_weight_loss_corrosion_rate(
        mass_loss_g=0.01,
        density_g_cm3=7.85,
        exposed_area_cm2=10,
        exposure_time_hours=24,
    )

    assert result == pytest.approx(expected)


def test_zero_area_is_rejected():
    with pytest.raises(ValueError):
        calculate_weight_loss_corrosion_rate(0.01, 7.85, 0, 24)


def test_electrochemical_corrosion_rate():
    expected = 0.00327 * 10 * 27.92 / 7.85

    result = calculate_electrochemical_corrosion_rate(
        corrosion_current_density_uA_cm2=10,
        equivalent_weight_g_equiv=27.92,
        density_g_cm3=7.85,
    )

    assert result == pytest.approx(expected)


def test_inhibition_efficiency():
    assert calculate_inhibition_efficiency(2.0, 0.5) == pytest.approx(75.0)


def test_negative_inhibition_efficiency_is_allowed():
    assert calculate_inhibition_efficiency(1.0, 1.2) == pytest.approx(-20.0)
