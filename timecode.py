"""
Timecode calculation module for handling hh:mm:ss:ff format timecodes.
"""

class Timecode:
    """Represents a timecode with hours, minutes, seconds, and frames."""

    def __init__(self, hours=0, minutes=0, seconds=0, frames=0, framerate=25):
        """
        Initialize a timecode.

        Args:
            hours: Number of hours
            minutes: Number of minutes
            seconds: Number of seconds
            frames: Number of frames
            framerate: Frames per second
        """
        self.framerate = framerate
        self.total_frames = self._to_frames(hours, minutes, seconds, frames)

    def _to_frames(self, hours, minutes, seconds, frames):
        """Convert time components to total frames."""
        total_seconds = hours * 3600 + minutes * 60 + seconds
        return int(total_seconds * self.framerate + frames)

    def _from_frames(self, total_frames):
        """Convert total frames to time components."""
        frames = total_frames % self.framerate
        total_seconds = total_frames // self.framerate

        seconds = total_seconds % 60
        total_minutes = total_seconds // 60

        minutes = total_minutes % 60
        hours = total_minutes // 60

        return hours, minutes, seconds, frames

    @classmethod
    def from_string(cls, timecode_str, framerate=25):
        """
        Parse a timecode string in hh:mm:ss:ff format.

        Args:
            timecode_str: String in format "hh:mm:ss:ff"
            framerate: Frames per second

        Returns:
            Timecode object

        Raises:
            ValueError: If the format is invalid
        """
        parts = timecode_str.strip().split(':')
        if len(parts) != 4:
            raise ValueError(f"Invalid timecode format: {timecode_str}. Expected hh:mm:ss:ff")

        try:
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds = int(parts[2])
            frames = int(parts[3])
        except ValueError:
            raise ValueError(f"Invalid timecode format: {timecode_str}. All parts must be integers")

        if minutes >= 60 or seconds >= 60 or frames >= framerate:
            raise ValueError(f"Invalid timecode values in: {timecode_str}")

        return cls(hours, minutes, seconds, frames, framerate)

    def __add__(self, other):
        """Add two timecodes together."""
        if self.framerate != other.framerate:
            raise ValueError("Cannot add timecodes with different framerates")

        result = Timecode(framerate=self.framerate)
        result.total_frames = self.total_frames + other.total_frames
        return result

    def __str__(self):
        """Return timecode as string in hh:mm:ss:ff format."""
        hours, minutes, seconds, frames = self._from_frames(self.total_frames)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frames:02d}"


def add_timecodes(timecode_list, framerate=25):
    """
    Add a list of timecode strings.

    Args:
        timecode_list: List of timecode strings or a single string with newline-separated timecodes
        framerate: Frames per second

    Returns:
        String representation of the sum

    Raises:
        ValueError: If any timecode is invalid
    """
    if isinstance(timecode_list, str):
        timecode_list = [tc.strip() for tc in timecode_list.split('\n') if tc.strip()]

    if not timecode_list:
        return "00:00:00:00"

    result = Timecode(framerate=framerate)

    for tc_str in timecode_list:
        tc = Timecode.from_string(tc_str, framerate)
        result = result + tc

    return str(result)
