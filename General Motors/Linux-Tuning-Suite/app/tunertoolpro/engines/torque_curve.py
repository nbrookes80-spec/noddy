"""TorqueCurve: RPM-indexed HP/TQ pairs with interpolated lookups.

Transcribed by hand from the CPython 3.12 disassembly of the original
TorqueCurve class (recovered/6l80e-python-disasm/01293..01457). Each method
names the disassembly file it was read from. Status: transcribed, NOT yet
differentially verified (see README.md: the original must not be executed
without approval).

boost_curve is any object with an `is_empty` property and a
`torque_mult(rpm)` method (the BoostCurve class, still to be reconstructed).
"""


class TorqueCurve:
    """Stores RPM-indexed (rpm, hp, tq) tuples sorted by rpm.

    An empty curve (fewer than two points) falls back to flat scalar behaviour.
    """

    def __init__(self, points=None, boost_curve=None):
        # __init__.dis 1300
        # The original sorts by rpm and fills in any missing torque from hp:
        # tq = hp * 5252 / max(1, rpm) when hp > 0, else 0.
        self.points = sorted(points or [], key=lambda p: p[0])
        for i, p in enumerate(self.points):
            rpm, hp, tq = p
            if tq is None or tq == 0:
                tq = hp * 5252.0 / max(1.0, rpm) if hp > 0 else 0.0
                self.points[i] = (rpm, hp, tq)
        self.boost_curve = boost_curve

    @property
    def is_empty(self):
        # is_empty.dis 1313
        return len(self.points) < 2

    def _uses_boost(self):
        return self.boost_curve is not None and not self.boost_curve.is_empty

    def _scan_rpm_range(self, value_at):
        """Yields (rpm, value) at 101 evenly spaced points across the curve."""
        rmin = self.points[0][0]
        rmax = self.points[-1][0]
        for i in range(101):
            r = rmin + (rmax - rmin) * i / 100
            yield r, value_at(r)

    @property
    def peak_hp(self):
        # peak_hp.dis 1317
        if self.is_empty:
            return 0.0
        if not self._uses_boost():
            return max(p[1] for p in self.points)
        peak = 0.0
        for _, v in self._scan_rpm_range(self.hp_at):
            if v > peak:
                peak = v
        return peak

    @property
    def peak_tq(self):
        # peak_tq.dis 1333
        if self.is_empty:
            return 0.0
        if not self._uses_boost():
            return max(p[2] for p in self.points)
        peak = 0.0
        for _, v in self._scan_rpm_range(self.tq_at):
            if v > peak:
                peak = v
        return peak

    @property
    def peak_hp_rpm(self):
        # peak_hp_rpm.dis 1348
        if self.is_empty:
            return 0
        if not self._uses_boost():
            return max(self.points, key=lambda p: p[1])[0]
        peak_rpm, peak_v = 0, 0.0
        for r, v in self._scan_rpm_range(self.hp_at):
            if v > peak_v:
                peak_v = v
                peak_rpm = r
        return peak_rpm

    @property
    def peak_tq_rpm(self):
        # peak_tq_rpm.dis 1364
        if self.is_empty:
            return 0
        if not self._uses_boost():
            return max(self.points, key=lambda p: p[2])[0]
        peak_rpm, peak_v = 0, 0.0
        for r, v in self._scan_rpm_range(self.tq_at):
            if v > peak_v:
                peak_v = v
                peak_rpm = r
        return peak_rpm

    @property
    def rpm_range(self):
        # rpm_range.dis 1380
        if self.is_empty:
            return (0, 0)
        return (self.points[0][0], self.points[-1][0])

    def _interp(self, rpm, idx):
        """Linear interpolation of column idx (1 = hp, 2 = tq), then boost scaling.

        Shared body of hp_at.dis 1386 and tq_at.dis 1410.
        """
        if self.is_empty:
            return 0.0
        if rpm <= self.points[0][0]:
            base = self.points[0][idx]
        elif rpm >= self.points[-1][0]:
            base = self.points[-1][idx]
        else:
            base = self.points[-1][idx]
            for i in range(len(self.points) - 1):
                r1, v1 = self.points[i][0], self.points[i][idx]
                r2, v2 = self.points[i + 1][0], self.points[i + 1][idx]
                if r1 <= rpm <= r2:
                    t = (rpm - r1) / (r2 - r1)
                    base = v1 + (v2 - v1) * t
                    break
        if self.boost_curve is not None:
            return base * self.boost_curve.torque_mult(rpm)
        return base

    def hp_at(self, rpm):
        # hp_at.dis 1386
        return self._interp(rpm, 1)

    def tq_at(self, rpm):
        # tq_at.dis 1410
        return self._interp(rpm, 2)

    def avg_hp(self, rpm_lo, rpm_hi):
        # avg_hp.dis 1432: trapezoid average of hp over [rpm_lo, rpm_hi], 16 steps
        if self.is_empty or rpm_hi <= rpm_lo:
            return 0.0
        n = 16
        step = (rpm_hi - rpm_lo) / n
        total = 0.0
        for i in range(n):
            r1 = rpm_lo + i * step
            r2 = r1 + step
            total += (self.hp_at(r1) + self.hp_at(r2)) * 0.5 * step
        return total / (rpm_hi - rpm_lo)

    def to_dict(self):
        # to_dict.dis 1447
        return {'points': [list(p) for p in self.points]}

    @classmethod
    def from_dict(cls, d):
        # from_dict.dis 1451
        if not d or 'points' not in d:
            return cls()
        return cls([tuple(p) for p in d['points']])

    @classmethod
    def from_csv(cls, path):
        # from_csv.dis 1457
        # Reads rpm,hp,tq rows. The first row is skipped only when its first
        # cell is not numeric. Rows with rpm <= 0 or unparseable cells are dropped.
        import csv as _csv
        points = []
        with open(path, 'r') as f:
            reader = _csv.reader(f)
            header_skipped = False
            for row in reader:
                if not row:
                    continue
                if not header_skipped:
                    try:
                        float(row[0])
                    except ValueError:
                        header_skipped = True
                        continue
                    header_skipped = True
                try:
                    rpm = float(row[0])
                    hp = float(row[1]) if len(row) > 1 else 0.0
                    tq = float(row[2]) if len(row) > 2 else 0.0
                except (ValueError, IndexError):
                    continue
                if rpm > 0:
                    points.append((rpm, hp, tq))
        return cls(points)
