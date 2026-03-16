import sys
import os

# Allow the test to find logic_utils.py from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from logic_utils import check_guess


def test_win():
    assert check_guess(50, 50)[0] == "Win"


def test_too_high():
    assert check_guess(60, 50)[0] == "Too High"


def test_too_low():
    assert check_guess(40, 50)[0] == "Too Low"