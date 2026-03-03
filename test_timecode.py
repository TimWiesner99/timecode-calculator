"""Tests for timecode calculation logic."""

from timecode import FrameTimecode, DecimalTimecode, SimpleTimecode, Timecode, add_timecodes, apply_to_all


# --- FrameTimecode tests ---

def test_basic_addition():
    """Test basic timecode addition."""
    tc1 = FrameTimecode.from_string("00:00:10:00", fps=25)
    tc2 = FrameTimecode.from_string("00:00:15:12", fps=25)
    result = tc1 + tc2
    print(f"Test 1: {tc1} + {tc2} = {result}")
    assert str(result) == "00:00:25:12", f"Expected 00:00:25:12, got {result}"
    print("PASS Test 1 passed")


def test_frame_overflow():
    """Test that frames overflow correctly to seconds."""
    tc1 = FrameTimecode.from_string("00:00:00:20", fps=25)
    tc2 = FrameTimecode.from_string("00:00:00:10", fps=25)
    result = tc1 + tc2
    print(f"\nTest 2: {tc1} + {tc2} = {result}")
    assert str(result) == "00:00:01:05", f"Expected 00:00:01:05, got {result}"
    print("PASS Test 2 passed")


def test_complex_addition():
    """Test complex timecode addition with hours."""
    tc1 = FrameTimecode.from_string("01:15:45:23", fps=25)
    tc2 = FrameTimecode.from_string("00:30:20:15", fps=25)
    result = tc1 + tc2
    print(f"\nTest 3: {tc1} + {tc2} = {result}")
    assert str(result) == "01:46:06:13", f"Expected 01:46:06:13, got {result}"
    print("PASS Test 3 passed")


def test_multiple_timecodes():
    """Test adding multiple timecodes using add_timecodes function."""
    timecodes = """00:00:10:00
00:00:15:12
00:01:05:08"""
    result = add_timecodes(timecodes, mode='frames', framerate=25)
    print(f"\nTest 4: Multiple timecodes sum = {result}")
    assert result == "00:01:30:20", f"Expected 00:01:30:20, got {result}"
    print("PASS Test 4 passed")


def test_different_framerate():
    """Test with 24fps framerate."""
    tc1 = FrameTimecode.from_string("00:00:00:20", fps=24)
    tc2 = FrameTimecode.from_string("00:00:00:10", fps=24)
    result = tc1 + tc2
    print(f"\nTest 5 (24fps): {tc1} + {tc2} = {result}")
    assert str(result) == "00:00:01:06", f"Expected 00:00:01:06, got {result}"
    print("PASS Test 5 passed")


def test_timecode_alias():
    """Test that Timecode alias works as a backward-compatible name for FrameTimecode."""
    tc = Timecode.from_string("00:00:05:00", fps=25)
    assert isinstance(tc, FrameTimecode)
    print("\nPASS Test 6 (Timecode alias) passed")


# --- DecimalTimecode tests ---

def test_decimal_basic():
    """Test basic decimal timecode addition."""
    tc1 = DecimalTimecode.from_string("00:00:10,000")
    tc2 = DecimalTimecode.from_string("00:00:15,500")
    result = tc1 + tc2
    print(f"\nTest 7 (decimal): {tc1} + {tc2} = {result}")
    assert str(result) == "00:00:25,500", f"Expected 00:00:25,500, got {result}"
    print("PASS Test 7 passed")


def test_decimal_ms_overflow():
    """Test millisecond overflow into seconds."""
    tc1 = DecimalTimecode.from_string("00:00:00,800")
    tc2 = DecimalTimecode.from_string("00:00:00,400")
    result = tc1 + tc2
    print(f"\nTest 8 (decimal overflow): {tc1} + {tc2} = {result}")
    assert str(result) == "00:00:01,200", f"Expected 00:00:01,200, got {result}"
    print("PASS Test 8 passed")


def test_decimal_add_timecodes():
    """Test add_timecodes in decimal mode."""
    timecodes = "00:00:10,000\n00:00:15,500\n00:01:05,080"
    result = add_timecodes(timecodes, mode='decimal')
    print(f"\nTest 9 (decimal add_timecodes): {result}")
    assert result == "00:01:30,580", f"Expected 00:01:30,580, got {result}"
    print("PASS Test 9 passed")


# --- SimpleTimecode tests ---

def test_simple_basic():
    """Test basic simple timecode addition."""
    tc1 = SimpleTimecode.from_string("00:00:10")
    tc2 = SimpleTimecode.from_string("00:00:15")
    result = tc1 + tc2
    print(f"\nTest 10 (simple): {tc1} + {tc2} = {result}")
    assert str(result) == "00:00:25", f"Expected 00:00:25, got {result}"
    print("PASS Test 10 passed")


def test_simple_overflow():
    """Test second overflow into minutes."""
    tc1 = SimpleTimecode.from_string("00:00:50")
    tc2 = SimpleTimecode.from_string("00:00:20")
    result = tc1 + tc2
    print(f"\nTest 11 (simple overflow): {tc1} + {tc2} = {result}")
    assert str(result) == "00:01:10", f"Expected 00:01:10, got {result}"
    print("PASS Test 11 passed")


def test_simple_add_timecodes():
    """Test add_timecodes in simple mode."""
    timecodes = "00:00:10\n00:00:15\n00:01:05"
    result = add_timecodes(timecodes, mode='simple')
    print(f"\nTest 12 (simple add_timecodes): {result}")
    assert result == "00:01:30", f"Expected 00:01:30, got {result}"
    print("PASS Test 12 passed")


# --- apply_to_all tests ---

def test_apply_to_all_add_frames():
    """Test adding an offset to a list of frame timecodes."""
    timecodes = "00:00:10:00\n00:00:20:00\n00:01:00:00"
    results = apply_to_all(timecodes, "00:00:05:00", operation='add', mode='frames', framerate=25)
    print(f"\nTest 13 (apply_to_all add frames): {results}")
    assert results == ["00:00:15:00", "00:00:25:00", "00:01:05:00"], f"Got {results}"
    print("PASS Test 13 passed")


def test_apply_to_all_subtract_frames():
    """Test subtracting an offset from a list of frame timecodes."""
    timecodes = "00:00:30:00\n00:01:00:00"
    results = apply_to_all(timecodes, "00:00:10:00", operation='subtract', mode='frames', framerate=25)
    print(f"\nTest 14 (apply_to_all subtract frames): {results}")
    assert results == ["00:00:20:00", "00:00:50:00"], f"Got {results}"
    print("PASS Test 14 passed")


def test_apply_to_all_decimal():
    """Test adding an offset to decimal timecodes."""
    timecodes = "00:00:10,000\n00:00:20,500"
    results = apply_to_all(timecodes, "00:00:05,250", operation='add', mode='decimal')
    print(f"\nTest 15 (apply_to_all decimal): {results}")
    assert results == ["00:00:15,250", "00:00:25,750"], f"Got {results}"
    print("PASS Test 15 passed")


def test_apply_to_all_simple():
    """Test subtracting an offset from simple timecodes."""
    timecodes = "00:01:00\n00:02:30"
    results = apply_to_all(timecodes, "00:00:30", operation='subtract', mode='simple')
    print(f"\nTest 16 (apply_to_all simple subtract): {results}")
    assert results == ["00:00:30", "00:02:00"], f"Got {results}"
    print("PASS Test 16 passed")


if __name__ == "__main__":
    print("Running timecode tests...\n")
    test_basic_addition()
    test_frame_overflow()
    test_complex_addition()
    test_multiple_timecodes()
    test_different_framerate()
    test_timecode_alias()
    test_decimal_basic()
    test_decimal_ms_overflow()
    test_decimal_add_timecodes()
    test_simple_basic()
    test_simple_overflow()
    test_simple_add_timecodes()
    test_apply_to_all_add_frames()
    test_apply_to_all_subtract_frames()
    test_apply_to_all_decimal()
    test_apply_to_all_simple()
    print("\nPASS All tests passed!")
