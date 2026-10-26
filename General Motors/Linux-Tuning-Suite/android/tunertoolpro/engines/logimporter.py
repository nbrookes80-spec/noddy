"""LogImporter: read a datalog CSV and summarise shifts, stall RPM, WOT slip and trans temp.

Transcribed by hand from the CPython 3.12 disassembly of the original class
(recovered/6l80e-python-disasm/01499..01831). Status: transcribed, NOT yet
differentially verified.

pandas is optional. from_csv tries pandas first and falls back to the csv
module on any exception.
"""

import csv
import math
from itertools import islice

MPH_K = 336.13  # same constant as calc_engine.MPH_K


class LogImporter:
    RPM_ALIASES = ['engine rpm', 'engine speed', 'rpm', 'spark engine']
    MPH_ALIASES = ['vehicle speed', 'vss', 'speed (mph)']
    KPH_ALIASES = ['vehicle speed (kph)', 'vss (kph)', 'speed (kph)']
    TPS_ALIASES = ['tps (%)', 'throttle position', 'tps', 'app', 'apps']
    GEAR_ALIASES = ['current gear', 'trans gear', 'gear', 'trans current']
    TRANS_TEMP_ALIASES = ['trans temp', 'atf temp', 'transmission oil', 'tft', 'trans fluid']
    INPUT_SPD_ALIASES = ['trans input speed', 'input shaft', 'tiss', 'turbine']
    OUTPUT_SPD_ALIASES = ['trans output speed', 'output shaft', 'toss']
    TCC_DC_ALIASES = ['tcc duty', 'torque converter clutch duty', 'tcc pwm', 'tcc dc']
    TIME_ALIASES = ['time', 'timestamp', 'seconds', 't (s)']

    def __init__(self):
        # __init__.dis 1499
        self.rows = []
        self.col_map = {}
        self.headers = []
        self.sample_rate = 0.0

    # ----- column mapping -------------------------------------------------

    def _build_column_map(self, headers):
        # _build_column_map.dis
        lc = [h.lower() for h in headers]
        targets = [
            ('rpm', self.RPM_ALIASES),
            ('mph', self.MPH_ALIASES),
            ('kph', self.KPH_ALIASES),
            ('tps', self.TPS_ALIASES),
            ('gear', self.GEAR_ALIASES),
            ('trans_temp', self.TRANS_TEMP_ALIASES),
            ('input_spd', self.INPUT_SPD_ALIASES),
            ('output_spd', self.OUTPUT_SPD_ALIASES),
            ('tcc_dc', self.TCC_DC_ALIASES),
        ]
        mapping = {}
        for key, aliases in targets:
            for alias in aliases:
                for i, h in enumerate(lc):
                    if alias in h:
                        mapping[key] = i
                        break
                if key in mapping:
                    break
        return mapping

    def _find_col(self, aliases):
        # _find_col.dis: first header (in file order) containing any alias
        for i, h in enumerate(self.headers):
            hl = h.lower()
            for alias in aliases:
                if alias in hl:
                    return i
        return None

    def get_col(self, row, key):
        # get_col.dis
        idx = self.col_map.get(key)
        if idx is None or idx >= len(row):
            return None
        return row[idx]

    @property
    def is_empty(self):
        return len(self.rows) == 0

    @property
    def n_samples(self):
        return len(self.rows)

    def detected_columns(self):
        return [(key, self.headers[idx]) for key, idx in self.col_map.items()
                if idx < len(self.headers)]

    # ----- header sniffing ------------------------------------------------

    @staticmethod
    def _is_number(s):
        # _is_number.dis
        try:
            float(s)
            return True
        except (ValueError, TypeError):
            return False

    @classmethod
    def _header_index(cls, rows):
        """Index of the first row with at least two non-numeric, non-blank cells; else 0."""
        for i, row in enumerate(rows):
            non_numeric = sum(1 for c in row if c.strip() and not cls._is_number(c))
            if non_numeric >= 2:
                return i
        return 0

    @classmethod
    def _sniff_header_row(cls, path, max_lines=5):
        # _sniff_header_row.dis
        try:
            with open(path, 'r', errors='ignore') as f:
                preview = list(islice(f, max_lines))
        except OSError:
            return 0
        return cls._header_index(list(csv.reader(preview)))

    # ----- loading --------------------------------------------------------

    @classmethod
    def from_csv(cls, path, progress_cb=None, target_hz=None):
        # from_csv.dis 1600-1700 (arg order inferred from local names)
        def progress(p):
            if progress_cb:
                progress_cb(p)

        try:
            import pandas as pd  # noqa: F401  (import checked here; from_dataframe uses it)
            header_idx = cls._sniff_header_row(path)
            progress(5)
            df = pd.read_csv(path, skiprows=header_idx, low_memory=False,
                             encoding_errors='ignore')
            progress(15)
            imp = cls.from_dataframe(df, target_hz=target_hz)
            progress(100)
            return imp
        except Exception:
            pass

        # csv-module fallback
        imp = cls()
        with open(path, 'r', errors='ignore') as f:
            rows = list(csv.reader(f))
        if not rows:
            return imp
        progress(20)

        header_idx = cls._header_index(rows[:5])
        imp.headers = [c.strip() for c in rows[header_idx]]
        imp.col_map = imp._build_column_map(imp.headers)

        data_rows = rows[header_idx + 1:]
        n_total = len(data_rows)
        parsed_rows = []
        for i, row in enumerate(data_rows):
            if not row or all(not c.strip() for c in row):
                continue
            parsed = []
            for c in row:
                try:
                    parsed.append(float(c))
                except ValueError:
                    parsed.append(None)
            parsed_rows.append(parsed)
            if progress_cb and n_total > 0 and i % 5000 == 0:
                progress(20 + int(70 * i / n_total))

        imp.rows = parsed_rows
        imp._apply_sample_rate(target_hz)
        progress(100)
        return imp

    @classmethod
    def from_dataframe(cls, df, target_hz=None):
        # from_dataframe.dis
        import pandas as pd

        imp = cls()
        df = df.copy()
        imp.headers = [str(c).strip() for c in df.columns]
        imp.col_map = imp._build_column_map(imp.headers)

        for col in df.columns:
            if df[col].dtype == object:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        time_idx = imp._find_col(cls.TIME_ALIASES)
        if time_idx is not None and len(df) >= 2:
            try:
                t0 = df.iloc[0, time_idx]
                t1 = df.iloc[1, time_idx]
                if pd.notna(t0) and pd.notna(t1) and t1 > t0:
                    imp.sample_rate = 1.0 / (t1 - t0)
            except (IndexError, KeyError):
                pass

        if target_hz and imp.sample_rate > 1.5 * target_hz:
            stride = max(1, int(imp.sample_rate / target_hz))
            df = df.iloc[::stride].reset_index(drop=True)
            imp.sample_rate /= stride

        imp.rows = [
            [None if (v is None or (isinstance(v, float) and math.isnan(v))) else v
             for v in row]
            for row in df.values.tolist()
        ]
        return imp

    def _apply_sample_rate(self, target_hz):
        """csv path: sample rate from the first two time values, then optional stride."""
        time_idx = self._find_col(self.TIME_ALIASES)
        if time_idx is not None and len(self.rows) >= 2:
            try:
                t0 = self.rows[0][time_idx]
                t1 = self.rows[1][time_idx]
                dt = t1 - t0
                if dt > 0:
                    self.sample_rate = 1.0 / dt
            except (TypeError, IndexError):
                pass
        if target_hz and self.sample_rate > 1.5 * target_hz:
            stride = max(1, int(self.sample_rate / target_hz))
            self.rows = self.rows[::stride]
            self.sample_rate /= stride

    # ----- analysis -------------------------------------------------------

    def analyze(self, cfg=None):
        # analyze.dis 1749 onwards. cfg keys used: ratios, axle, chain, tire.
        result = {
            'shift_events': [],
            'stall_peak_rpm': None,
            'wot_slip_pct': None,
            'temp_range': None,
            'n_samples': self.n_samples,
            'warnings': [],
        }
        if self.is_empty:
            result['warnings'].append('Log is empty')
            return result

        for needed in ('rpm', 'mph', 'tps'):
            if needed not in self.col_map:
                result['warnings'].append(
                    f'Missing column: {needed} — analysis will be partial')

        # Shift events: gear increments with TPS above 70%.
        if 'gear' in self.col_map:
            prev_gear = None
            for row in self.rows:
                g = self.get_col(row, 'gear')
                if not isinstance(g, (int, float)):
                    continue
                g = int(g)
                if prev_gear is not None and g == prev_gear + 1:
                    tps_val = self.get_col(row, 'tps') or 0
                    if tps_val > 70:
                        mph = self.get_col(row, 'mph')
                        rpm = self.get_col(row, 'rpm')
                        result['shift_events'].append({
                            'gear_from': prev_gear,
                            'gear_to': g,
                            'mph': mph or 0,
                            'rpm': rpm or 0,
                            'tps': tps_val,
                        })
                prev_gear = g
        else:
            result['warnings'].append(
                "No gear column — can't detect shift events. "
                "VCM Scanner: enable PID 'Current Gear' (TCM).")

        # Stall: peak RPM at standstill (under 5 mph) with throttle above 80%.
        # Checked against analyze.dis 1807-1818: keep rows with mph < 5 and tps > 80.
        if all(k in self.col_map for k in ('rpm', 'mph', 'tps')):
            stall_samples = []
            for row in self.rows:
                rpm = self.get_col(row, 'rpm')
                mph = self.get_col(row, 'mph')
                tps = self.get_col(row, 'tps')
                if rpm is None or mph is None or tps is None:
                    continue
                if mph < 5 and tps > 80:
                    stall_samples.append(rpm)
            if stall_samples:
                result['stall_peak_rpm'] = max(stall_samples)

        # WOT slip: engine RPM vs. RPM implied by vehicle speed and gear ratio.
        # The original reads the tire size from 'tire_dia' (default 28.0), analyze.dis 1825.
        ratios = (cfg or {}).get('ratios', [])
        if ratios:
            axle = cfg.get('axle', 1.0)
            chain = cfg.get('chain', 1.0)
            final_drive = axle * chain
            tire = cfg.get('tire_dia', 28.0)
            slips = []
            for row in self.rows:
                vals = [self.get_col(row, k) for k in ('rpm', 'mph', 'tps', 'gear')]
                if any(v is None for v in vals):
                    continue
                rpm, mph, tps, gear = vals
                gear_idx = int(gear) - 1
                if not 0 <= gear_idx < len(ratios):
                    continue
                if mph < 10 or tps < 90 or rpm <= 0:
                    continue
                coupled_rpm = mph * final_drive * ratios[gear_idx] * MPH_K / tire
                if coupled_rpm > 100:
                    slip = (rpm - coupled_rpm) / rpm * 100.0
                    if 0 <= slip < 30:
                        slips.append(slip)
            if slips:
                result['wot_slip_pct'] = sum(slips) / len(slips)

        # Transmission temperature range.
        if 'trans_temp' in self.col_map:
            temps = [v for v in (self.get_col(r, 'trans_temp') for r in self.rows)
                     if v is not None]
            if temps:
                result['temp_range'] = (min(temps), max(temps))

        return result
