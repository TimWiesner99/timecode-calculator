"""Timecode classes for handling video and subtitle timecodes.

Provides an ABC base class with shared arithmetic/comparison operators,
and three concrete subclasses:
- FrameTimecode:   HH:MM:SS:FF (frame-based, e.g. broadcast)
- DecimalTimecode: HH:MM:SS,mmm (millisecond-based, e.g. SRT subtitles)
- SimpleTimecode:  HH:MM:SS (second-based, no frame-level precision)
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import re


class TimecodeBase(ABC):
    """Abstract base class for timecodes.

    Provides shared arithmetic and comparison operators.
    Subclasses must implement unit conversion and string parsing/formatting.
    """

    @abstractmethod
    def to_units(self) -> int:
        """Convert timecode to its smallest unit (frames, milliseconds, or seconds)."""

    @classmethod
    @abstractmethod
    def from_units(cls, total: int) -> TimecodeBase:
        """Create a timecode from a total unit count."""

    @classmethod
    @abstractmethod
    def from_string(cls, tc_string: str, **kwargs: object) -> TimecodeBase:
        """Parse a timecode from a string."""

    @abstractmethod
    def to_string(self) -> str:
        """Format the timecode as a string."""

    def __str__(self) -> str:
        return self.to_string()

    def __add__(self, other: TimecodeBase) -> TimecodeBase:
        if not isinstance(other, self.__class__):
            return NotImplemented
        total = self.to_units() + other.to_units()
        return self.__class__.from_units(total)

    def __sub__(self, other: TimecodeBase) -> TimecodeBase:
        if not isinstance(other, self.__class__):
            return NotImplemented
        total = self.to_units() - other.to_units()
        if total < 0:
            raise ValueError("Cannot have negative timecode result")
        return self.__class__.from_units(total)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.to_units() == other.to_units()

    def __lt__(self, other: TimecodeBase) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.to_units() < other.to_units()

    def __le__(self, other: TimecodeBase) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.to_units() <= other.to_units()

    def __gt__(self, other: TimecodeBase) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.to_units() > other.to_units()

    def __ge__(self, other: TimecodeBase) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.to_units() >= other.to_units()

    def __hash__(self) -> int:
        return hash(self.to_units())


@dataclass
class FrameTimecode(TimecodeBase):
    """Represents a video timecode with hours, minutes, seconds, and frames.

    The timecode format is HH:MM:SS:FF where FF is the frame number (0-based).
    Frame rate is configurable, with 25 fps as the default (PAL standard).
    """

    hours: int
    minutes: int
    seconds: int
    frames: int
    fps: int = 25

    TIMECODE_PATTERN = re.compile(r'^(\d{2}):(\d{2}):(\d{2}):(\d{2})$')

    def __post_init__(self) -> None:
        if self.hours < 0:
            raise ValueError(f"Hours cannot be negative: {self.hours}")
        if not 0 <= self.minutes < 60:
            raise ValueError(f"Minutes must be 0-59: {self.minutes}")
        if not 0 <= self.seconds < 60:
            raise ValueError(f"Seconds must be 0-59: {self.seconds}")
        if not 0 <= self.frames < self.fps:
            raise ValueError(f"Frames must be 0-{self.fps - 1}: {self.frames}")

    def to_units(self) -> int:
        return self.to_frames()

    @classmethod
    def from_units(cls, total: int, fps: int = 25) -> FrameTimecode:
        return cls.from_frames(total, fps)

    def to_frames(self) -> int:
        """Convert timecode to total frame count."""
        return (
            self.frames
            + self.seconds * self.fps
            + self.minutes * 60 * self.fps
            + self.hours * 3600 * self.fps
        )

    @classmethod
    def from_frames(cls, total_frames: int, fps: int = 25) -> FrameTimecode:
        """Create a FrameTimecode from total frame count."""
        if total_frames < 0:
            raise ValueError(f"Total frames cannot be negative: {total_frames}")

        frames = total_frames % fps
        total_seconds = total_frames // fps
        seconds = total_seconds % 60
        total_minutes = total_seconds // 60
        minutes = total_minutes % 60
        hours = total_minutes // 60

        return cls(hours=hours, minutes=minutes, seconds=seconds, frames=frames, fps=fps)

    @classmethod
    def from_string(cls, tc_string: str, fps: int = 25) -> FrameTimecode:
        """Parse a timecode string in HH:MM:SS:FF format."""
        if not tc_string or not isinstance(tc_string, str):
            raise ValueError(f"Invalid timecode string: {tc_string}")

        tc_string = tc_string.strip()
        match = cls.TIMECODE_PATTERN.match(tc_string)

        if not match:
            raise ValueError(f"Invalid timecode format: '{tc_string}'. Expected HH:MM:SS:FF")

        hours, minutes, seconds, frames = map(int, match.groups())

        if frames >= fps:
            frames = 0

        return cls(hours=hours, minutes=minutes, seconds=seconds, frames=frames, fps=fps)

    def to_string(self) -> str:
        """Convert timecode to string format HH:MM:SS:FF."""
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}:{self.frames:02d}"

    def __add__(self, other: TimecodeBase) -> FrameTimecode:
        if not isinstance(other, FrameTimecode):
            return NotImplemented
        if self.fps != other.fps:
            raise ValueError(f"Cannot add timecodes with different frame rates: {self.fps} vs {other.fps}")
        total_frames = self.to_frames() + other.to_frames()
        return FrameTimecode.from_frames(total_frames, self.fps)

    def __sub__(self, other: TimecodeBase) -> FrameTimecode:
        if not isinstance(other, FrameTimecode):
            return NotImplemented
        if self.fps != other.fps:
            raise ValueError(f"Cannot subtract timecodes with different frame rates: {self.fps} vs {other.fps}")
        total_frames = self.to_frames() - other.to_frames()
        if total_frames < 0:
            raise ValueError("Cannot have negative timecode result")
        return FrameTimecode.from_frames(total_frames, self.fps)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FrameTimecode):
            return NotImplemented
        return self.to_frames() == other.to_frames() and self.fps == other.fps

    def __hash__(self) -> int:
        return hash((self.to_frames(), self.fps))

    def round_to_seconds(self) -> FrameTimecode:
        """Round timecode to the nearest second."""
        if self.frames >= self.fps / 2:
            total_frames = self.to_frames() + (self.fps - self.frames)
            return FrameTimecode.from_frames(total_frames, self.fps)
        else:
            return FrameTimecode(
                hours=self.hours,
                minutes=self.minutes,
                seconds=self.seconds,
                frames=0,
                fps=self.fps
            )

    def to_string_rounded(self) -> str:
        """Convert timecode to string format HH:MM:SS (without frames), rounded to nearest second."""
        rounded = self.round_to_seconds()
        return f"{rounded.hours:02d}:{rounded.minutes:02d}:{rounded.seconds:02d}"

    def __repr__(self) -> str:
        return f"FrameTimecode({self.to_string()}, fps={self.fps})"


@dataclass
class DecimalTimecode(TimecodeBase):
    """Represents an SRT subtitle timecode with hours, minutes, seconds, and milliseconds.

    The timecode format is HH:MM:SS,mmm as used in SRT subtitle files.
    """

    hours: int = 0
    minutes: int = 0
    seconds: int = 0
    milliseconds: int = 0

    TIMECODE_PATTERN = re.compile(r'^(\d{2}):(\d{2}):(\d{2}),(\d{3})$')

    def __post_init__(self) -> None:
        if self.hours < 0:
            raise ValueError(f"Hours cannot be negative: {self.hours}")
        if not 0 <= self.minutes < 60:
            raise ValueError(f"Minutes must be 0-59: {self.minutes}")
        if not 0 <= self.seconds < 60:
            raise ValueError(f"Seconds must be 0-59: {self.seconds}")
        if not 0 <= self.milliseconds < 1000:
            raise ValueError(f"Milliseconds must be 0-999: {self.milliseconds}")

    def to_units(self) -> int:
        """Convert timecode to total milliseconds."""
        return (
            self.milliseconds
            + self.seconds * 1000
            + self.minutes * 60_000
            + self.hours * 3_600_000
        )

    @classmethod
    def from_units(cls, total_ms: int) -> DecimalTimecode:
        """Create a DecimalTimecode from total milliseconds."""
        if total_ms < 0:
            raise ValueError(f"Total milliseconds cannot be negative: {total_ms}")

        milliseconds = total_ms % 1000
        total_seconds = total_ms // 1000
        seconds = total_seconds % 60
        total_minutes = total_seconds // 60
        minutes = total_minutes % 60
        hours = total_minutes // 60

        return cls(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

    @classmethod
    def from_string(cls, tc_string: str) -> DecimalTimecode:
        """Parse a timecode string in HH:MM:SS,mmm format."""
        if not tc_string or not isinstance(tc_string, str):
            raise ValueError(f"Invalid timecode string: {tc_string}")

        tc_string = tc_string.strip()
        match = cls.TIMECODE_PATTERN.match(tc_string)

        if not match:
            raise ValueError(f"Invalid timecode format: '{tc_string}'. Expected HH:MM:SS,mmm")

        hours, minutes, seconds, milliseconds = map(int, match.groups())
        return cls(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

    def to_string(self) -> str:
        """Convert timecode to string format HH:MM:SS,mmm."""
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d},{self.milliseconds:03d}"

    def round_to_seconds(self) -> DecimalTimecode:
        """Round timecode to the nearest second."""
        if self.milliseconds >= 500:
            total_ms = self.to_units() + (1000 - self.milliseconds)
            return DecimalTimecode.from_units(total_ms)
        else:
            return DecimalTimecode(
                hours=self.hours,
                minutes=self.minutes,
                seconds=self.seconds,
                milliseconds=0
            )

    def to_string_rounded(self) -> str:
        """Convert timecode to string format HH:MM:SS (without milliseconds), rounded to nearest second."""
        rounded = self.round_to_seconds()
        return f"{rounded.hours:02d}:{rounded.minutes:02d}:{rounded.seconds:02d}"

    def __repr__(self) -> str:
        return f"DecimalTimecode({self.to_string()})"


@dataclass
class SimpleTimecode(TimecodeBase):
    """Represents a timecode in HH:MM:SS format without frame-level precision.

    Useful for contexts where second-level accuracy is sufficient.
    """

    hours: int = 0
    minutes: int = 0
    seconds: int = 0

    TIMECODE_PATTERN = re.compile(r'^(\d{2}):(\d{2}):(\d{2})$')

    def __post_init__(self) -> None:
        if self.hours < 0:
            raise ValueError(f"Hours cannot be negative: {self.hours}")
        if not 0 <= self.minutes < 60:
            raise ValueError(f"Minutes must be 0-59: {self.minutes}")
        if not 0 <= self.seconds < 60:
            raise ValueError(f"Seconds must be 0-59: {self.seconds}")

    def to_units(self) -> int:
        """Convert timecode to total seconds."""
        return self.seconds + self.minutes * 60 + self.hours * 3600

    @classmethod
    def from_units(cls, total: int) -> SimpleTimecode:
        """Create a SimpleTimecode from total seconds."""
        if total < 0:
            raise ValueError(f"Total seconds cannot be negative: {total}")

        seconds = total % 60
        total_minutes = total // 60
        minutes = total_minutes % 60
        hours = total_minutes // 60

        return cls(hours=hours, minutes=minutes, seconds=seconds)

    @classmethod
    def from_string(cls, tc_string: str) -> SimpleTimecode:
        """Parse a timecode string in HH:MM:SS format."""
        if not tc_string or not isinstance(tc_string, str):
            raise ValueError(f"Invalid timecode string: {tc_string}")

        tc_string = tc_string.strip()
        match = cls.TIMECODE_PATTERN.match(tc_string)

        if not match:
            raise ValueError(f"Invalid timecode format: '{tc_string}'. Expected HH:MM:SS")

        hours, minutes, seconds = map(int, match.groups())
        return cls(hours=hours, minutes=minutes, seconds=seconds)

    def to_string(self) -> str:
        """Convert timecode to string format HH:MM:SS."""
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"

    def __repr__(self) -> str:
        return f"SimpleTimecode({self.to_string()})"


# Backward-compatible alias
Timecode = FrameTimecode


def add_timecodes(timecode_list, mode: str = 'frames', framerate: int = 25) -> str:
    """Add a list of timecodes.

    Args:
        timecode_list: List of timecode strings or a single newline-separated string
        mode: One of 'frames', 'decimal', or 'simple'
        framerate: Frames per second (only used in 'frames' mode)

    Returns:
        String representation of the sum

    Raises:
        ValueError: If any timecode is invalid or mode is unknown
    """
    if isinstance(timecode_list, str):
        timecode_list = [tc.strip() for tc in timecode_list.split('\n') if tc.strip()]

    if mode == 'frames':
        if not timecode_list:
            return "00:00:00:00"
        result = FrameTimecode(hours=0, minutes=0, seconds=0, frames=0, fps=framerate)
        for tc_str in timecode_list:
            tc = FrameTimecode.from_string(tc_str, fps=framerate)
            result = result + tc
        return str(result)

    elif mode == 'decimal':
        if not timecode_list:
            return "00:00:00,000"
        result = DecimalTimecode()
        for tc_str in timecode_list:
            tc = DecimalTimecode.from_string(tc_str)
            result = result + tc
        return str(result)

    elif mode == 'simple':
        if not timecode_list:
            return "00:00:00"
        result = SimpleTimecode()
        for tc_str in timecode_list:
            tc = SimpleTimecode.from_string(tc_str)
            result = result + tc
        return str(result)

    else:
        raise ValueError(f"Unknown mode: '{mode}'. Expected 'frames', 'decimal', or 'simple'")


def apply_to_all(timecode_list, offset_str: str, operation: str = 'add',
                  mode: str = 'frames', framerate: int = 25) -> list[str]:
    """Apply an offset timecode to every timecode in a list.

    Args:
        timecode_list: List of timecode strings or a single newline-separated string
        offset_str: The offset timecode to add or subtract
        operation: 'add' or 'subtract'
        mode: One of 'frames', 'decimal', or 'simple'
        framerate: Frames per second (only used in 'frames' mode)

    Returns:
        List of result timecode strings

    Raises:
        ValueError: If any timecode is invalid, mode is unknown, or subtraction
                    would produce a negative result
    """
    if isinstance(timecode_list, str):
        timecode_list = [tc.strip() for tc in timecode_list.split('\n') if tc.strip()]

    if not timecode_list:
        return []

    if operation not in ('add', 'subtract'):
        raise ValueError(f"Unknown operation: '{operation}'. Expected 'add' or 'subtract'")

    cls_map = {
        'frames': (FrameTimecode, {'fps': framerate}),
        'decimal': (DecimalTimecode, {}),
        'simple': (SimpleTimecode, {}),
    }

    if mode not in cls_map:
        raise ValueError(f"Unknown mode: '{mode}'. Expected 'frames', 'decimal', or 'simple'")

    tc_cls, parse_kwargs = cls_map[mode]
    offset = tc_cls.from_string(offset_str, **parse_kwargs)

    results = []
    for tc_str in timecode_list:
        tc = tc_cls.from_string(tc_str, **parse_kwargs)
        if operation == 'add':
            results.append(str(tc + offset))
        else:
            results.append(str(tc - offset))
    return results


__all__ = [
    "TimecodeBase",
    "FrameTimecode",
    "DecimalTimecode",
    "SimpleTimecode",
    "Timecode",
    "add_timecodes",
    "apply_to_all",
]
