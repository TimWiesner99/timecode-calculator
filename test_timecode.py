"""Simple tests for timecode calculation logic."""

from timecode import Timecode, add_timecodes

def test_basic_addition():
    """Test basic timecode addition."""
    tc1 = Timecode.from_string("00:00:10:00", framerate=25)
    tc2 = Timecode.from_string("00:00:15:12", framerate=25)
    result = tc1 + tc2
    print(f"Test 1: {tc1} + {tc2} = {result}")
    assert str(result) == "00:00:25:12", f"Expected 00:00:25:12, got {result}"
    print("✓ Test 1 passed")

def test_frame_overflow():
    """Test that frames overflow correctly to seconds."""
    tc1 = Timecode.from_string("00:00:00:20", framerate=25)
    tc2 = Timecode.from_string("00:00:00:10", framerate=25)
    result = tc1 + tc2
    print(f"\nTest 2: {tc1} + {tc2} = {result}")
    assert str(result) == "00:00:01:05", f"Expected 00:00:01:05, got {result}"
    print("✓ Test 2 passed")

def test_complex_addition():
    """Test complex timecode addition with hours."""
    tc1 = Timecode.from_string("01:15:45:23", framerate=25)
    tc2 = Timecode.from_string("00:30:20:15", framerate=25)
    result = tc1 + tc2
    print(f"\nTest 3: {tc1} + {tc2} = {result}")
    assert str(result) == "01:46:06:13", f"Expected 01:46:06:13, got {result}"
    print("✓ Test 3 passed")

def test_multiple_timecodes():
    """Test adding multiple timecodes using add_timecodes function."""
    timecodes = """00:00:10:00
00:00:15:12
00:01:05:08"""
    result = add_timecodes(timecodes, framerate=25)
    print(f"\nTest 4: Multiple timecodes sum = {result}")
    assert result == "00:01:30:20", f"Expected 00:01:30:20, got {result}"
    print("✓ Test 4 passed")

def test_different_framerate():
    """Test with 24fps framerate."""
    tc1 = Timecode.from_string("00:00:00:20", framerate=24)
    tc2 = Timecode.from_string("00:00:00:10", framerate=24)
    result = tc1 + tc2
    print(f"\nTest 5 (24fps): {tc1} + {tc2} = {result}")
    assert str(result) == "00:00:01:06", f"Expected 00:00:01:06, got {result}"
    print("✓ Test 5 passed")

if __name__ == "__main__":
    print("Running timecode tests...\n")
    test_basic_addition()
    test_frame_overflow()
    test_complex_addition()
    test_multiple_timecodes()
    test_different_framerate()
    print("\n✓ All tests passed!")
