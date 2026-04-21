import numpy as np

def simulate_passenger_demand(day, hour, size=1):
    mean = get_expected_demand_arr(day, hour)
    rel_std = get_rel_std_arr(day)

    uncertainty = np.random.normal(
        loc=0,
        scale=mean * rel_std,
        size=size)

    demand = mean + uncertainty

    # rounding to nearest whole person for realistic demand estimation
    return np.round(np.maximum(demand, 0)).astype(int)

def get_expected_demand_arr(day, hour):
    if day in range(1, 5): # Mo-Do
        return get_hourly_bimodal_demand(hour, 100, 250, 7.5, 1.5, 275, 17, 1.8)
    elif day == 5: # Fr
        return get_hourly_bimodal_demand(hour, 100, 250, 7.5, 1.5, 315, 16, 2.25)
    elif day == 6: # Sa
        return get_hourly_plateau_demand(hour, 50, 175, 14, 5.5, 50, 13, 0.8)
    else: # So
        return get_hourly_bimodal_demand(hour, 50, 175, 11, 4, 215, 20, 3)

def get_rel_std_arr(day):
    if day in range(1, 5): # Mo-Fr
        return 0.3
    elif day == 6: # Sa
        return 0.25
    else: # So
        return 0.15

def get_hourly_bimodal_demand(t, p_basis, p_peak1, mu1, sigma1, p_peak2, mu2, sigma2):
    peak1 = p_peak1 * np.exp(-((t - mu1)**2) / (2 * sigma1**2))
    peak2 = p_peak2 * np.exp(-((t - mu2)**2) / (2 * sigma2**2))

    expected_value = p_basis + peak1 + peak2

    # rounding to nearest whole person for realistic demand estimation
    return np.round(expected_value).astype(int)

def get_hourly_plateau_demand(t, p_basis, p_plateau, mu_plat, sigma_plat, p_dip, mu_dip, sigma_dip):
    plateau = p_plateau * np.exp(-0.5 * ((t - mu_plat) / sigma_plat)**8)
    dip = p_dip * np.exp(-((t - mu_dip)**2) / (2 * sigma_dip**2))

    excepted_value = p_basis + plateau - dip

    # rounding to nearest whole person for realistic demand estimation
    return np.round(np.maximum(excepted_value, 0)).astype(int)