import os
from typing import List, Union


class SampleProvider:
    """Load a sequence of sample values from a CSV-like file.

    File format:
    - lines with one value: numeric -> returns number
    - lines with comma-separated values: returns tuple of numbers
    - blank lines and lines starting with # are ignored

    The provider cycles through values when exhausted.
    """

    def __init__(self, sensor_id: str, filename: str = None):
        base = os.path.join(os.path.dirname(__file__), 'samples')
        if filename:
            path = filename
        else:
            path = os.path.join(base, f"{sensor_id}.csv")
        self.path = path
        self._samples: List[Union[int, float, tuple]] = []
        self._idx = 0
        self._load()

    def _parse_value(self, token: str):
        token = token.strip()
        if token == '':
            return None
        if '.' in token:
            try:
                return float(token)
            except ValueError:
                return token
        try:
            return int(token)
        except ValueError:
            return token

    def _load(self):
        try:
            with open(self.path, 'r') as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln or ln.startswith('#'):
                        continue
                    parts = [p.strip() for p in ln.split(',')]
                    parsed = [self._parse_value(p) for p in parts if p != '']
                    if len(parsed) == 1:
                        self._samples.append(parsed[0])
                    else:
                        self._samples.append(tuple(parsed))
        except FileNotFoundError:
            # Leave samples empty; callers should handle fallback
            self._samples = []

    def next(self):
        if not self._samples:
            raise FileNotFoundError(f"Sample file not found or empty: {self.path}")
        val = self._samples[self._idx]
        self._idx = (self._idx + 1) % len(self._samples)
        return val
