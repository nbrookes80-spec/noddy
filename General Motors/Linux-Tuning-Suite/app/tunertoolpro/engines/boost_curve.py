"""BoostCurve: parameterised boost-vs-RPM curve for forced-induction engines.

Transcribed by hand from the CPython 3.12 disassembly of the original
BoostCurve class (recovered/6l80e-python-disasm/01214..01280). Status:
transcribed, NOT yet differentially verified.

Effective torque: engine_tq * torque_mult(rpm), where
torque_mult = 1 + psi_at(rpm) * torque_per_psi_pct / 100.
"""


class BoostCurve:
    """Ramp from 0 PSI at low RPM, to peak_psi at peak_rpm, then flat or tapering
    to redline_psi. Defaults represent a moderate ~10 PSI turbo on a 5.3 L LS truck.
    """

    def __init__(self, spool_rpm=2500, peak_psi=0.0, peak_rpm=4000,
                 redline_psi=None, torque_per_psi_pct=7.5):
        # __init__.dis 1225
        self.spool_rpm = float(spool_rpm)
        self.peak_psi = float(peak_psi)
        self.peak_rpm = float(peak_rpm)
        self.redline_psi = float(redline_psi) if redline_psi is not None else self.peak_psi
        self.torque_per_psi_pct = float(torque_per_psi_pct)

    @property
    def is_empty(self):
        # is_empty.dis 1234
        return self.peak_psi <= 0.0

    def psi_at(self, rpm):
        # psi_at.dis 1238
        if self.is_empty:
            return 0.0
        rpm = float(rpm)
        if rpm < self.spool_rpm:
            t = max(0.0, rpm) / max(1.0, self.spool_rpm)
            return 0.5 * t
        if rpm < self.peak_rpm:
            t = (rpm - self.spool_rpm) / max(1.0, self.peak_rpm - self.spool_rpm)
            t_smooth = 3 * t ** 2 - 2 * t ** 3
            return 0.5 + (self.peak_psi - 0.5) * t_smooth
        ref_high = max(self.peak_rpm + 1000, 6500)
        if rpm >= ref_high:
            return self.redline_psi
        t = (rpm - self.peak_rpm) / (ref_high - self.peak_rpm)
        return self.peak_psi + (self.redline_psi - self.peak_psi) * t

    def torque_mult(self, rpm):
        # torque_mult.dis 1264
        if self.is_empty:
            return 1.0
        return 1.0 + self.psi_at(rpm) * self.torque_per_psi_pct / 100.0

    def to_dict(self):
        # to_dict.dis 1271
        return {
            'spool_rpm': self.spool_rpm,
            'peak_psi': self.peak_psi,
            'peak_rpm': self.peak_rpm,
            'redline_psi': self.redline_psi,
            'torque_per_psi_pct': self.torque_per_psi_pct,
        }

    @classmethod
    def from_dict(cls, d):
        # from_dict.dis 1280
        if not d:
            return cls()
        return cls(
            spool_rpm=d.get('spool_rpm', 2500),
            peak_psi=d.get('peak_psi', 0.0),
            peak_rpm=d.get('peak_rpm', 4000),
            redline_psi=d.get('redline_psi'),
            torque_per_psi_pct=d.get('torque_per_psi_pct', 7.5),
        )
