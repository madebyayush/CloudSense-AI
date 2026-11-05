import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scaling import ScalingEngine

def test_scale_up():
    result = ScalingEngine().decide(85, 2)
    assert result["action"] == "SCALE UP"
    assert result["recommended_instances"] == 3

def test_scale_down():
    result = ScalingEngine().decide(20, 3)
    assert result["action"] == "SCALE DOWN"
    assert result["recommended_instances"] == 2

def test_maintain():
    result = ScalingEngine().decide(50, 2)
    assert result["action"] == "MAINTAIN"
    assert result["recommended_instances"] == 2
