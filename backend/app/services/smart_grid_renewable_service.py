"""
Smart Renewable Energy Micro-Grid Dispatch Simulator Service.
Simulates solar photovoltaic kinetics and LiFePO4 battery storage system (BESS)
dispatch for campus microgrids with diurnal peak shaving optimization.
"""

from typing import Dict, Any, List, Optional


class SmartGridRenewableDispatchService:
    """
    Simulates solar PV power generation, LiFePO4 battery kinetics,
    and 24-hour dispatch economics with peak shaving and grid import reduction.
    """

    # Realistic 24-hour campus baseline load curve in kW (Classrooms, Labs, Library, Hostels)
    DEFAULT_CAMPUS_LOAD_KW: List[float] = [
        18.0, 16.0, 15.0, 15.0, 16.0, 22.0,  # 00:00 - 05:00 (Night base load)
        35.0, 48.0, 65.0, 85.0, 95.0, 90.0,  # 06:00 - 11:00 (Morning ramp, labs & AC)
        85.0, 80.0, 75.0, 70.0, 65.0, 60.0,  # 12:00 - 17:00 (Afternoon)
        75.0, 80.0, 70.0, 50.0, 30.0, 20.0   # 18:00 - 23:00 (Evening library & hostel peak)
    ]

    # Realistic 24-hour solar irradiance profile in W/m^2 (Dhaka tropical solar window)
    DEFAULT_SOLAR_IRRADIANCE_W_M2: List[float] = [
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0,        # 00:00 - 05:00 (Night)
        45.0, 210.0, 480.0, 740.0, 890.0, 950.0, # 06:00 - 11:00 (Sunrise & peak sun)
        920.0, 820.0, 620.0, 380.0, 120.0, 15.0, # 12:00 - 17:00 (Afternoon decline)
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0         # 18:00 - 23:00 (Sunset & Night)
    ]

    @classmethod
    def calculate_solar_pv_output(
        cls,
        array_area_m2: float = 250.0,
        efficiency: float = 0.21,
        irradiance_w_per_m2: float = 850.0,
        ambient_temp_c: float = 32.0,
        temp_coefficient: float = 0.0038,
        system_performance_ratio: float = 0.82
    ) -> Dict[str, Any]:
        """
        Calculates DC and AC solar power generation with thermal derating.
        """
        area = max(0.1, float(array_area_m2))
        eff = max(0.01, min(0.50, float(efficiency)))
        irr = max(0.0, float(irradiance_w_per_m2))
        amb_t = float(ambient_temp_c)
        pr = max(0.1, min(1.0, float(system_performance_ratio)))
        gamma = max(0.0, float(temp_coefficient))

        # Cell temperature model: T_cell = T_amb + 0.025 * Irradiance
        cell_temp = amb_t + (0.025 * irr)

        # Thermal derating factor: [1 - gamma * (T_cell - 25.0)]
        temp_delta = max(0.0, cell_temp - 25.0)
        thermal_derating_factor = max(0.5, 1.0 - (gamma * temp_delta))
        thermal_loss_pct = round((1.0 - thermal_derating_factor) * 100.0, 2)

        # DC Power in kW = Area * Efficiency * Irradiance * Derating / 1000
        dc_power_kw = (area * eff * irr * thermal_derating_factor) / 1000.0
        ac_power_kw = dc_power_kw * pr
        hourly_energy_kwh = ac_power_kw * 1.0

        return {
            "cell_temperature_c": round(cell_temp, 2),
            "dc_power_kw": round(dc_power_kw, 3),
            "ac_power_kw": round(ac_power_kw, 3),
            "thermal_derating_pct": thermal_loss_pct,
            "hourly_energy_kwh": round(hourly_energy_kwh, 3)
        }

    @classmethod
    def simulate_microgrid_dispatch(
        cls,
        solar_area_m2: float = 650.0,
        solar_efficiency: float = 0.20,
        battery_capacity_kwh: float = 120.0,
        battery_initial_soc: float = 0.50,
        battery_max_charge_kw: float = 40.0,
        battery_max_discharge_kw: float = 50.0,
        battery_efficiency_roundtrip: float = 0.90,
        grid_tariff_peak_bdt_per_kwh: float = 13.5,
        grid_tariff_offpeak_bdt_per_kwh: float = 8.2,
        custom_hourly_load_kw: Optional[List[float]] = None,
        custom_hourly_irradiance: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Executes 24-hour chronological microgrid dispatch optimization.
        Implements battery peak shaving and renewable self-consumption priority.
        """
        load_curve = custom_hourly_load_kw if (custom_hourly_load_kw and len(custom_hourly_load_kw) == 24) else cls.DEFAULT_CAMPUS_LOAD_KW
        irradiance_curve = custom_hourly_irradiance if (custom_hourly_irradiance and len(custom_hourly_irradiance) == 24) else cls.DEFAULT_SOLAR_IRRADIANCE_W_M2

        b_cap = max(1.0, float(battery_capacity_kwh))
        soc = max(0.15, min(0.95, float(battery_initial_soc)))
        max_ch = max(0.0, float(battery_max_charge_kw))
        max_dis = max(0.0, float(battery_max_discharge_kw))
        eta_rt = max(0.5, min(0.99, float(battery_efficiency_roundtrip)))
        eta_one_way = eta_rt ** 0.5

        soc_min = 0.15
        soc_max = 0.95

        hourly_results: List[Dict[str, Any]] = []

        total_load_kwh = 0.0
        total_solar_generated_kwh = 0.0
        total_battery_charged_kwh = 0.0
        total_battery_discharged_kwh = 0.0
        total_grid_imported_kwh = 0.0
        total_grid_exported_kwh = 0.0
        daily_cost_with_microgrid = 0.0
        daily_baseline_cost = 0.0

        peak_demand_unshaved = max(load_curve) if load_curve else 0.0
        peak_demand_shaved = 0.0

        for h in range(24):
            load_h = max(0.0, float(load_curve[h]))
            irr_h = max(0.0, float(irradiance_curve[h]))
            total_load_kwh += load_h

            # Determine tariff for this hour (Dhaka peak: 17:00 to 23:00)
            is_peak = (17 <= h <= 23)
            tariff = grid_tariff_peak_bdt_per_kwh if is_peak else grid_tariff_offpeak_bdt_per_kwh
            daily_baseline_cost += load_h * tariff

            # Solar PV generation for hour h
            pv_calc = cls.calculate_solar_pv_output(
                array_area_m2=solar_area_m2,
                efficiency=solar_efficiency,
                irradiance_w_per_m2=irr_h,
                ambient_temp_c=28.0 + (6.0 if 11 <= h <= 15 else 0.0)
            )
            pv_kw = pv_calc["ac_power_kw"]
            total_solar_generated_kwh += pv_kw

            battery_flow_kw = 0.0  # Positive = charge, Negative = discharge
            grid_import_kw = 0.0
            grid_export_kw = 0.0

            net_power = pv_kw - load_h

            if net_power >= 0:
                # Excess Solar: charge battery first, export remainder
                excess_solar = net_power
                # Capacity available to charge (kWh)
                space_kwh = max(0.0, (soc_max - soc) * b_cap)
                # Max charging power possible in 1 hour
                charge_power = min(excess_solar, max_ch, space_kwh / eta_one_way if eta_one_way > 0 else 0.0)
                energy_stored = charge_power * eta_one_way
                soc += energy_stored / b_cap
                soc = min(soc_max, max(soc_min, soc))

                battery_flow_kw = charge_power
                total_battery_charged_kwh += charge_power

                # Leftover beyond battery charging exported to grid
                grid_export_kw = max(0.0, excess_solar - charge_power)
                total_grid_exported_kwh += grid_export_kw
            else:
                # Solar Deficit: discharge battery first to shave peak, import rest from grid
                deficit = abs(net_power)
                # Energy available to discharge (kWh)
                available_kwh = max(0.0, (soc - soc_min) * b_cap)
                # Max discharging power possible
                discharge_power = min(deficit, max_dis, available_kwh * eta_one_way)
                energy_drained = discharge_power / eta_one_way if eta_one_way > 0 else 0.0
                soc -= energy_drained / b_cap
                soc = min(soc_max, max(soc_min, soc))

                battery_flow_kw = -discharge_power
                total_battery_discharged_kwh += discharge_power

                # Remaining deficit imported from national grid
                grid_import_kw = max(0.0, deficit - discharge_power)
                total_grid_imported_kwh += grid_import_kw

            # Track peak shaved grid demand
            if grid_import_kw > peak_demand_shaved:
                peak_demand_shaved = grid_import_kw

            hourly_cost = grid_import_kw * tariff
            daily_cost_with_microgrid += hourly_cost

            hourly_results.append({
                "hour": h,
                "time_label": f"{h:02d}:00",
                "load_kw": round(load_h, 2),
                "solar_generation_kw": round(pv_kw, 2),
                "battery_power_kw": round(battery_flow_kw, 2),
                "battery_soc_pct": round(soc * 100.0, 1),
                "grid_import_kw": round(grid_import_kw, 2),
                "grid_export_kw": round(grid_export_kw, 2),
                "tariff_rate_bdt": tariff,
                "hourly_cost_bdt": round(hourly_cost, 2)
            })

        # Calculate peak shaving reduction percentage
        peak_reduction_pct = 0.0
        if peak_demand_unshaved > 0:
            peak_reduction_pct = round(max(0.0, (peak_demand_unshaved - peak_demand_shaved) / peak_demand_unshaved * 100.0), 2)

        # Renewable fraction
        renewable_fraction_pct = 0.0
        if total_load_kwh > 0:
            renewable_energy_used = max(0.0, total_load_kwh - total_grid_imported_kwh)
            renewable_fraction_pct = round(min(100.0, (renewable_energy_used / total_load_kwh) * 100.0), 2)

        daily_savings_bdt = max(0.0, daily_baseline_cost - daily_cost_with_microgrid)

        return {
            "total_load_kwh": round(total_load_kwh, 2),
            "total_solar_generated_kwh": round(total_solar_generated_kwh, 2),
            "total_battery_discharged_kwh": round(total_battery_discharged_kwh, 2),
            "total_battery_charged_kwh": round(total_battery_charged_kwh, 2),
            "total_grid_imported_kwh": round(total_grid_imported_kwh, 2),
            "total_grid_exported_kwh": round(total_grid_exported_kwh, 2),
            "final_battery_soc_pct": round(soc * 100.0, 1),
            "peak_demand_unshaved_kw": round(peak_demand_unshaved, 2),
            "peak_demand_shaved_kw": round(peak_demand_shaved, 2),
            "peak_shaving_reduction_pct": peak_reduction_pct,
            "renewable_fraction_pct": renewable_fraction_pct,
            "daily_cost_with_microgrid_bdt": round(daily_cost_with_microgrid, 2),
            "daily_baseline_cost_no_microgrid_bdt": round(daily_baseline_cost, 2),
            "daily_savings_bdt": round(daily_savings_bdt, 2),
            "hourly_dispatch": hourly_results
        }
