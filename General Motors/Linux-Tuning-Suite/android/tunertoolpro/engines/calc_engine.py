"""CalcEngine — shift-point and TCC math, reconstructed by hand from CPython 3.12 bytecode.

Source of truth: recovered/6l80e-python-disasm/ (02106..02209 .dis.txt files, plus the
module-level constants in 00001__module_.dis.txt).

Every function here was transcribed by reading the disassembly instruction by
instruction. Comments give the disassembly line that each rule came from.
Gear indices are 0-based; TPS columns are 0..TPS_COLS-1 at TPS_STEP % per column.
"""

import math

# ---- module constants (00001__module_.dis.txt) -------------------------------
MPH_K = 336.13                 # line 45
TPS_COLS = 17                  # line 48
TPS_STEP = 6.25                # line 49
SLOPE_BLEND = (0.0, 0.1, 0.1, 0.1, 0.1, 0.125, 0.15, 0.225, 0.35, 0.5,
               0.675, 0.825, 0.925, 0.95, 1.0, 1.0, 1.0)   # line 51
MAX_SPREAD_ITERATIONS = 32     # line 55
TCC_DISABLED_MPH = 255.0       # line 59 — sentinel: "TCC not allowed at this cell"


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


class CalcEngine:
    # ---- primitive helpers --------------------------------------------------

    @staticmethod
    def mph(rpm, tire_dia, ratio, final_drive):
        """Vehicle speed (MPH) at rpm: rpm * tire / (final_drive * ratio * MPH_K)."""
        if ratio <= 0 or final_drive <= 0:
            return 0.0
        return rpm * tire_dia / (final_drive * ratio * MPH_K)

    @staticmethod
    def stall_slip(stall_rpm):
        """Torque-converter slip fraction at stall: (stall/1000)^1.7 / 100."""
        return (stall_rpm / 1000.0) ** 1.7 / 100.0

    @staticmethod
    def base_slope(tps_pct, offset, factor):
        """Clamp(min(1, x**factor)) where x = clamp(tps - offset, 0, 100) / 100."""
        x = _clamp(tps_pct - offset, 0.0, 100.0) / 100.0
        return _clamp(min(1.0, x ** factor), 0.0, 1.0)

    @staticmethod
    def upshift_slope(col, tps_pct, offset, factor, upf):
        """Base slope blended toward an 'aggressive' curve by SLOPE_BLEND[col].

        aggressive = 1 - (1 - x) ** (factor + upf/10)
        result     = base + (aggressive - base) * SLOPE_BLEND[col]   (col clamped 0..16)
        """
        base = CalcEngine.base_slope(tps_pct, offset, factor)
        x = _clamp(tps_pct - offset, 0.0, 100.0) / 100.0
        aggressive = 1.0 - (1.0 - x) ** (factor + upf / 10.0)
        blend = SLOPE_BLEND[int(_clamp(col, 0, 16))]
        return _clamp(base + (aggressive - base) * blend, 0.0, 1.0)

    @staticmethod
    def downshift_slope(tps_pct, offset, factor, downf):
        """clamp(x ** (factor + 0.1 + (10 - downf)/5), 0, 1)."""
        x = _clamp(tps_pct - offset, 0.0, 100.0) / 100.0
        exp = factor + 0.1 + (10.0 - downf) / 5.0
        return _clamp(x ** exp, 0.0, 1.0)

    @staticmethod
    def vss_calibration(mode_idx, tire_dia, axle_ratio, vss_count, metric):
        """Speedometer (VSS) calibration summary for the export dialog.

        tire_rev_mi = 63360 / (tire_dia * pi);  trans_rev_mi = tire_rev_mi * axle_ratio.
        mode_idx 0..3 choose which quantities are divided by the axle ratio.
        Any other mode_idx returns the short summary with a metric/imperial label.
        """
        tire_rev_mi = 63360.0 / (tire_dia * math.pi)
        trans_rev_mi = tire_rev_mi * axle_ratio
        keys_tire = ('VSS Pulses/Mile', 'VSS Count', 'Tire / Gear', 'Trans Rev/Mile')
        keys_gear = ('VSS Pulses/Mile', 'VSS Count', 'Gear Ratio', 'Trans Rev/Mile')
        if mode_idx == 0:
            return dict(zip(keys_tire, (trans_rev_mi * vss_count, vss_count,
                                   tire_dia / axle_ratio, trans_rev_mi)))
        if mode_idx == 1:
            return dict(zip(keys_tire, (trans_rev_mi * vss_count / axle_ratio,
                                   vss_count / axle_ratio,
                                   tire_dia / axle_ratio, trans_rev_mi)))
        if mode_idx == 2:
            return dict(zip(keys_gear, (trans_rev_mi * vss_count, vss_count,
                                   axle_ratio, trans_rev_mi)))
        if mode_idx == 3:
            return dict(zip(keys_gear, (trans_rev_mi * vss_count / axle_ratio,
                                   vss_count / axle_ratio,
                                   axle_ratio, trans_rev_mi)))
        label_rev = 'Tire Rev/Km' if metric else 'Tire Rev/M'
        value_rev = tire_rev_mi / 1.609 if metric else tire_rev_mi
        return {'VSS Count': vss_count, label_rev: value_rev, 'Gear Ratio': axle_ratio}

    # ---- main entry point ---------------------------------------------------

    @staticmethod
    def calculate(cfg):
        """Build the shift-speed, upshift, downshift, TCC unlock and TCC lock tables.

        Required cfg keys: ratios, tire_dia, axle, chain, idle_rpm, stall_rpm,
        shift_rpm, downshift_rpm, weight, rwhp, tps_offset, tps_factor,
        up_firmness, down_firmness, spread_up, spread_lock, spread_lock_up,
        spread_unlock_dn, lead_mode, lead_value, down_time, delays, min_tcc_rpm.
        Optional: per_gear_rpm, torque_curve, min_tcc_gear (2), accel_lock_gear (3),
        wot_lock_gear (n), stall_lock_logic (False), init_lock_logic (False; read
        but unused in calculate()).
        """
        ratios = cfg['ratios']                                    # 2216
        n = len(ratios)                                           # 2217
        tire = cfg['tire_dia']                                    # 2218
        final_drive = cfg['axle'] * cfg['chain']                  # 2219
        idle = cfg['idle_rpm']                                    # 2220
        stall = cfg['stall_rpm']                                  # 2221
        shift_rpm = cfg['shift_rpm']                              # 2222
        drpm = cfg['downshift_rpm']                               # 2223
        wt = cfg['weight']                                        # 2224
        rwhp = cfg['rwhp']                                        # 2225
        offset = cfg['tps_offset']                                # 2226
        factor = cfg['tps_factor']                                # 2227
        upf = cfg['up_firmness']                                  # 2228
        downf = cfg['down_firmness']                              # 2229
        s_up = cfg['spread_up']                                   # 2230
        s_lock = cfg['spread_lock']                               # 2231
        s_lockup = cfg['spread_lock_up']                          # 2232
        s_unlock = cfg['spread_unlock_dn']                        # 2233
        lead_mode = cfg['lead_mode']                              # 2234
        lead_val = cfg['lead_value']                              # 2235
        down_time = cfg['down_time']                              # 2236
        delays = cfg['delays']                                    # 2237
        per_gear_rpm = cfg.get('per_gear_rpm', None)              # 2238
        torque_curve = cfg.get('torque_curve', None)              # 2288

        slip = CalcEngine.stall_slip(stall)                       # 2240

        # RPM target per gear (2245-2256)
        if per_gear_rpm is None or len(per_gear_rpm) < n - 1:
            rpm_targets = [shift_rpm] * n
        elif len(per_gear_rpm) == n - 1:
            rpm_targets = [max(1500.0, r) for r in per_gear_rpm] + [shift_rpm]
        else:
            rpm_targets = [max(1500.0, r) for r in per_gear_rpm[:n]]

        # Speed at each gear's idle-plus-400 RPM and per-gear shift speed
        min_speed = [CalcEngine.mph(idle + 400, tire, ratios[g], final_drive)
                     for g in range(n)]                           # 2255-2265
        speed = [[0.0] * 4 for _ in range(n)]                     # 2265

        # Per-gear WOT speeds: columns 0..3 (2266-2310)
        for g in range(n):
            ratio_g = ratios[g]                                   # 2267
            speed[g][0] = CalcEngine.mph(rpm_targets[g], tire, ratio_g, final_drive)  # 2268
            speed[g][1] = speed[g][0] * (1.0 - slip)              # 2269
            base_wot = speed[g][1]                                # 2270

            if lead_mode == 'rpm':                                # 2272
                lead_norm = lead_val / 8.0                        # 2274
                speed[g][2] = (base_wot * (1.0 - 0.01 * ratio_g * final_drive * lead_norm)
                               - (ratio_g + 1.0) * final_drive * lead_norm)   # 2275-2276
                if speed[g][2] < base_wot * 0.2:                  # 2277
                    speed[g][2] = base_wot * 0.2                  # 2278
                speed[g][3] = (speed[g][2] * 0.98 - 2.0           # 2279-2280
                               - ratio_g * final_drive * (1.0 + lead_val / 10.0) * 0.5)
            else:                                                 # 2287 onward
                v_ref = max(base_wot, 5.0)                        # 2287
                # is_empty is a property (LOAD_ATTR without CALL), not a method
                if torque_curve is not None and not torque_curve.is_empty:   # 2289
                    rpm_lo = max(1500.0, rpm_targets[g] - 1000.0) # 2293
                    rpm_hi = rpm_targets[g]                       # 2294
                    avg_hp = torque_curve.avg_hp(rpm_lo, rpm_hi)  # 2295
                    eff_hp = avg_hp * 0.92                        # 2296
                else:
                    eff_hp = rwhp * 0.75                          # 2298
                accel_mph_s = eff_hp * 375.0 / v_ref / wt * 21.93685   # 2299
                d = delays[g] if g < len(delays) else delays[-1]  # 2300
                up_d, dn_d = d                                    # 2300
                speed[g][2] = base_wot - accel_mph_s * (up_d + dn_d)          # 2301
                speed[g][3] = base_wot - accel_mph_s * (down_time + up_d + dn_d)  # 2302

            # Common clamps (2305-2313)
            d_cap = CalcEngine.mph(drpm, tire, ratio_g, final_drive)          # 2305
            if speed[g][3] > d_cap:                               # 2306
                speed[g][3] = d_cap                               # 2307
            min_down = speed[g][2] - s_up                         # 2309
            if speed[g][3] > min_down:                            # 2310
                speed[g][3] = min_down                            # 2311
            if speed[g][3] < speed[g][2] * 0.2:                   # 2312
                speed[g][3] = speed[g][2] * 0.2                   # 2313

        # Upshift and downshift tables, one row per shift, TPS_COLS columns (2318-2331)
        n_shifts = n - 1                                          # 2318
        up = [[0.0] * TPS_COLS for _ in range(n_shifts)]          # 2319
        dn = [[0.0] * TPS_COLS for _ in range(n_shifts)]          # 2320

        for g in range(n_shifts):                                 # 2322
            min_s = min_speed[g]                                  # 2323
            wot_up = speed[g][2]                                  # 2328
            wot_dn = speed[g][3]                                  # 2329
            for col in range(TPS_COLS):                           # 2331
                tps = col * TPS_STEP                              # 2332
                up_s = CalcEngine.upshift_slope(col, tps, offset, factor, upf)   # 2333
                dn_s = CalcEngine.downshift_slope(tps, offset, factor, downf)    # 2334
                up[g][col] = min_s + s_up + (wot_up - min_s - s_up) * up_s       # 2336
                dn[g][col] = min_s + (wot_dn - min_s) * dn_s                     # 2337
                if dn[g][col] > up[g][col] - s_up:                # 2340
                    dn[g][col] = up[g][col] - s_up                # 2341
                if dn[g][col] < 0:                                # 2342
                    dn[g][col] = 0.0                              # 2343

        # Gear-lock configuration (2349-2356)
        min_tcc_gear = max(1, cfg.get('min_tcc_gear', 2))     # 2349
        accel_lock_gear = max(1, cfg.get('accel_lock_gear', 3))  # 2350
        wot_lock_gear = max(1, cfg.get('wot_lock_gear', n))   # 2351
        stall_lock = cfg.get('stall_lock_logic', False)           # 2352
        init_lock = cfg.get('init_lock_logic', False)             # 2353 (unused here)

        # TCC unlock/lock tables initialised to the disabled sentinel (2357-2358)
        unlock = [[TCC_DISABLED_MPH] * TPS_COLS for _ in range(n)]
        lock = [[TCC_DISABLED_MPH] * TPS_COLS for _ in range(n)]

        for g in range(1, n):                                     # 2360
            if g + 1 < min_tcc_gear:                              # 2362
                continue
            # Base unlock: previous downshift + spread (2364-2376)
            for col in range(TPS_COLS):                           # 2364
                if g - 1 < n_shifts:                              # 2367
                    base = dn[g - 1][col] + s_unlock              # 2368
                else:
                    base = min_speed[g] + s_unlock                # 2370
                tcc_floor = CalcEngine.mph(cfg['min_tcc_rpm'], tire, ratios[g], final_drive)  # 2372
                if base < tcc_floor:                              # 2373
                    base = tcc_floor                              # 2374
                unlock[g][col] = base                             # 2375
                lock[g][col] = base + s_lock                      # 2376

            # Accelerator-lock adjustment (2383-2394)
            if g + 1 >= accel_lock_gear:                          # 2383
                for col in range(TPS_COLS):                       # 2384
                    if g < n_shifts:                              # 2385
                        accel_target = up[g][col] - s_lockup * 1.5    # 2386
                    elif 0 <= g - 1 < n_shifts:                   # 2387
                        accel_target = up[g - 1][col] + s_lockup  # 2388
                    else:
                        continue                                  # 2390
                    if lock[g][col] < accel_target:               # 2391
                        lock[g][col] = accel_target               # 2392
                    if unlock[g][col] > lock[g][col] - s_lock:    # 2393
                        unlock[g][col] = lock[g][col] - s_lock    # 2394

            # WOT-lock adjustment on the last TPS column (2400-2411)
            if g + 1 >= wot_lock_gear:                            # 2400
                col = TPS_COLS - 1                                # 2401
                if g < n_shifts:                                  # 2402
                    wot_lock = up[g][col] - s_lockup              # 2403
                elif 0 <= g - 1 < n_shifts:                       # 2404
                    wot_lock = up[g - 1][col] + s_lockup          # 2405
                else:
                    wot_lock = lock[g][col]                       # 2407
                if lock[g][col] < wot_lock:                       # 2408
                    lock[g][col] = wot_lock                       # 2409
                if unlock[g][col] > lock[g][col] - s_lock:        # 2410
                    unlock[g][col] = lock[g][col] - s_lock        # 2411

        # Stall-based lock floor (2416-2433)
        if stall_lock:
            stall_floor_rpm = stall * 0.66                        # 2417
            for g in range(1, n):                                 # 2418
                if g + 1 < min_tcc_gear:                          # 2419
                    continue
                floor_mph = CalcEngine.mph(stall_floor_rpm, tire, ratios[g], final_drive)  # 2421
                wot_mph = speed[g][0]                             # 2423
                floor_mph = min(floor_mph, wot_mph * 0.66)        # 2424
                for col in range(TPS_COLS):                       # 2425
                    if lock[g][col] < floor_mph:                  # 2426
                        lock[g][col] = floor_mph                  # 2427
                    if unlock[g][col] > lock[g][col] - s_lock:    # 2428
                        unlock[g][col] = lock[g][col] - s_lock    # 2429

        # Consistency passes (2438-2466), up to MAX_SPREAD_ITERATIONS
        for _ in range(MAX_SPREAD_ITERATIONS):                    # 2438
            changed = False                                       # 2439
            for g in range(1, n):                                 # 2440
                if g + 1 < min_tcc_gear:                          # 2442
                    # Below the minimum TCC gear: force both tables to the sentinel
                    for col in range(TPS_COLS):                   # 2443
                        if (unlock[g][col] != TCC_DISABLED_MPH
                                or lock[g][col] != TCC_DISABLED_MPH):   # 2444
                            unlock[g][col] = TCC_DISABLED_MPH     # 2445
                            lock[g][col] = TCC_DISABLED_MPH       # 2446
                            changed = True                        # 2447
                    continue                                      # 2448
                for col in range(TPS_COLS):                       # 2450
                    min_lock = unlock[g][col] + s_lock            # 2452
                    if lock[g][col] < min_lock:                   # 2453
                        lock[g][col] = min_lock                   # 2454
                        changed = True                            # 2455
                    if g < n_shifts:                              # 2460
                        max_lock = up[g][col] - s_lockup          # 2461
                        if lock[g][col] > max_lock:               # 2462
                            lock[g][col] = max(max_lock, unlock[g][col] + 0.1)   # 2463
                            changed = True                        # 2464
            if not changed:                                       # 2465
                break

        return {                                                  # 2468
            'min_speed': min_speed,
            'speed_summary': speed,
            'upshift': up,
            'downshift': dn,
            'tcc_unlock': unlock,
            'tcc_lock': lock,
            'n_gears': n,
            'rpm_targets': rpm_targets,
            'slip_pct': slip * 100.0,                             # 2477
        }

