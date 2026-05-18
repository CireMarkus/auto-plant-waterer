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
	# Environment variable override (useful for CI):
	# - AUTO_PLANT_USE_HARDWARE=1|true|yes enables hardware
	# - AUTO_PLANT_USE_HARDWARE=0|false|no disables hardware
	env = os.environ.get('AUTO_PLANT_USE_HARDWARE')
	if env is not None:
		if env.lower() in ('1', 'true', 'yes'):
			return True
		if env.lower() in ('0', 'false', 'no'):
			return False

	cfg = _load_config()
	# Use only the global flag. Per-sensor flags were removed to keep
	# configuration simple and consistent across environments.
	return bool(cfg.get('use_hardware', False))
