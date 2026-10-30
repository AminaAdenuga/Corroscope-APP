
"""Validated scientific calculations used by CorroScope."""

import math


def _validate_number(name, value, allow_zero=False):
    """Validate that a value is a finite, non-negative or positive number."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a numeric value.")

    value = float(value)

    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite.")

    if value < 0 or (value == 0 and not allow_zero):
        qualifier = "non-negative" if allow_zero else "greater than zero"
        raise ValueError(f"{name} must be {qualifier}.")

    return value


def calculate_mass_loss(initial_mass, final_mass):
    """Calculate specimen mass loss in grams."""
    initial = _validate_number(
        "Initial mass", initial_mass, allow_zero=True
    )
    final = _validate_number(
        "Final mass", final_mass, allow_zero=True
    )

    if final > initial:
        raise ValueError(
            "Final mass cannot exceed initial mass for a mass-loss calculation."
        )

    return initial - final


def calculate_weight_loss_corrosion_rate(
    mass_loss_g,
    density_g_cm3,
    exposed_area_cm2,
    exposure_time_hours,
):
    """
    Calculate corrosion rate in mm/year.

    CR = 87.6 * W / (density * area * time)

    W: mass loss in mg
    Density: g/cm³
    Area: cm²
    Time: hours
    """
    loss_g = _validate_number(
        "Mass loss", mass_loss_g, allow_zero=True
    )
    density = _validate_number("Density", density_g_cm3)
    area = _validate_number("Exposed area", exposed_area_cm2)
    time = _validate_number("Exposure time", exposure_time_hours)

    loss_mg = loss_g * 1000

    return 87.6 * loss_mg / (density * area * time)


def calculate_electrochemical_corrosion_rate(
    corrosion_current_density_uA_cm2,
    equivalent_weight_g_equiv,
    density_g_cm3,
):
    """
    Calculate electrochemical corrosion rate in mm/year.

    CR = 0.00327 * Icorr * EW / density

    Icorr: µA/cm²
    Equivalent weight: g/equivalent
    Density: g/cm³
    """
    current = _validate_number(
        "Corrosion current density",
        corrosion_current_density_uA_cm2,
        allow_zero=True,
    )
    equivalent_weight = _validate_number(
        "Equivalent weight", equivalent_weight_g_equiv
    )
    density = _validate_number("Density", density_g_cm3)

    return 0.00327 * current * equivalent_weight / density


def calculate_inhibition_efficiency(
    blank_corrosion_rate,
    inhibited_corrosion_rate,
):
    """
    Calculate inhibition efficiency as a percentage.

    IE (%) = [(CR_blank - CR_inhibited) / CR_blank] * 100

    Negative efficiency is allowed and indicates a higher corrosion
    rate in the inhibited condition than in the blank condition.
    """
    blank = _validate_number(
        "Blank corrosion rate", blank_corrosion_rate
    )
    inhibited = _validate_number(
        "Inhibited corrosion rate",
        inhibited_corrosion_rate,
        allow_zero=True,
    )

    return ((blank - inhibited) / blank) * 100
