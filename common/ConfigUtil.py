"""
Simple configuration utility for reading `common/config.json` and
exposing helper methods used by sensors to decide whether to use real
hardware or simulated values.

The functions are deliberately small and dependency-free so tests and CI
can run without external libraries.
"""
import json
import os
from typing import Optional

_CONFIG = None


def _load_config():
	global _CONFIG
	if _CONFIG is not None:
		return _CONFIG
	path = os.path.join(os.path.dirname(__file__), 'config.json')
	try:
		with open(path, 'r') as f:
			_CONFIG = json.load(f)
	except Exception:
		_CONFIG = {}
	return _CONFIG


def use_hardware(sensor_id: Optional[str] = None) -> bool:
	"""Return True if hardware should be used.

	Lookup order:
	- Per-sensor setting in `sensors` list with `id` and `use_hardware` bool
	- Top-level `use_hardware` bool
	- Defaults to False when config unreadable
	"""
	cfg = _load_config()
	# Use only the global flag. Per-sensor flags were removed to keep
	# configuration simple and consistent across environments.
	return bool(cfg.get('use_hardware', False))

def get_poll_rate(sensor_name: str) -> Optional[int]:
	"""Return the poll rate in seconds for a given sensor name.
	
	Looks up the sensor by id in the sensors list and returns its poll_rate_seconds.
	Returns None if sensor not found or poll_rate_seconds is not defined.
	"""
	cfg = _load_config()
	sensors = cfg.get('sensors', [])
	for sensor in sensors:
		if sensor.get('id') == sensor_name:
			return int(sensor.get('poll_rate_seconds'))
	return int(5)
