"""A wrapper for the different table types

"""

from .basic_table import BasicTable
from .simple_table import SimpleTable
from .noisy_table import NoisyTable, make_noisy

__all__ = ["BasicTable", "SimpleTable", "NoisyTable", "make_noisy"]
