from abc import ABC, abstractmethod
import turtle
import time
from datetime import datetime
from typing import Protocol


class Digit:
    """Class for drawing a single digit on an analog clock face."""
    
    def __init__(self, value: int, position: tuple[float, float], size: float = 1.0):
        self.value = value
        self.position = position
        self.size = size
        self._turtle = turtle.Turtle()
        self._turtle.hideturtle()
        self._turtle.speed(0)
    
    def draw(self) -> None:
        """Draw the digit at the specified position with the given size."""
        pass


class ClockFace:
    """Container for Digit objects, represents the clock face."""
    
    def __init__(self, radius: float, center: tuple[float, float] = (0, 0)):
        self.radius = radius
        self.center = center
        self.digits: list[Digit] = []
        self._turtle = turtle.Turtle()
        self._turtle.hideturtle()
        self._turtle.speed(0)
    
    def setup(self) -> None:
        """Set up the clock face with all 12 digits."""
        pass
    
    def draw(self) -> None:
        """Draw the complete clock face including all digits."""
        pass


class Hand:
    """Class for drawing and updating a clock hand."""
    
    def __init__(self, length: float, width: float, color: str, center: tuple[float, float] = (0, 0)):
        self.length = length
        self.width = width
        self.color = color
        self.center = center
        self.angle = 0
        self._turtle = turtle.Turtle()
        self._turtle.hideturtle()
        self._turtle.speed(0)
    
    def draw(self) -> None:
        """Draw the hand at the current angle."""
        pass
    
    def update(self, angle: float) -> None:
        """Update the hand's position to the new angle."""
        pass


class Theme(Protocol):
    """Protocol defining theme attributes."""
    
    background_color: str
    face_color: str
    digit_color: str
    hour_hand_color: str
    minute_hand_color: str
    second_hand_color: str


class LightTheme:
    """Light theme implementation."""
    
    background_color = "white"
    face_color = "#f0f0f0"
    digit_color = "black"
    hour_hand_color = "black"
    minute_hand_color = "blue"
    second_hand_color = "red"


class DarkTheme:
    """Dark theme implementation."""
    
    background_color = "#1a1a1a"
    face_color = "#333333"
    digit_color = "white"
    hour_hand_color = "white"
    minute_hand_color = "#66a3ff"
    second_hand_color = "#ff6666"


class Watch(ABC):
    """Base abstract class for all watch types."""
    
    def __init__(self, theme: Theme = LightTheme()):
        self.theme = theme
        self.screen = turtle.Screen()
        self.configure_screen()
    
    def configure_screen(self) -> None:
        """Configure the turtle screen with theme settings."""
        self.screen.bgcolor(self.theme.background_color)
        self.screen.title("Python Turtle Watch")
        self.screen.tracer(0)  # Turn off animation for smoother updates
    
    @abstractmethod
    def setup(self) -> None:
        """Set up the watch components."""
        pass
    
    @abstractmethod
    def update(self) -> None:
        """Update the watch based on the current time."""
        pass
    
    def run(self, update_interval: float = 1.0) -> None:
        """Run the watch with the specified update interval."""
        self.setup()
        
        while True:
            try:
                self.update()
                self.screen.update()
                time.sleep(update_interval)
            except (KeyboardInterrupt, turtle.Terminator):
                break


class AnalogWatch(Watch):
    """Implementation of an analog watch."""
    
    def __init__(self, theme: Theme = LightTheme(), radius: float = 200):
        super().__init__(theme)
        self.radius = radius
        self.clock_face = ClockFace(radius)
        self.hour_hand = Hand(radius * 0.5, 6, theme.hour_hand_color)
        self.minute_hand = Hand(radius * 0.7, 4, theme.minute_hand_color)
        self.second_hand = Hand(radius * 0.9, 2, theme.second_hand_color)
    
    def setup(self) -> None:
        """Set up the analog watch components."""
        self.clock_face.setup()
        self.clock_face.draw()
    
    def update(self) -> None:
        """Update the analog watch hands based on current time."""
        current_time = datetime.now()
        
        # Calculate angles for each hand
        second_angle = current_time.second * 6  # 6 degrees per second
        minute_angle = current_time.minute * 6 + current_time.second * 0.1  # 6 degrees per minute + small adjustment
        hour_angle = (current_time.hour % 12) * 30 + current_time.minute * 0.5  # 30 degrees per hour + adjustment
        
        # Update hands
        self.hour_hand.update(hour_angle)
        self.minute_hand.update(minute_angle)
        self.second_hand.update(second_angle)


class TimeFormat:
    """Enum-like class for time formats."""
    
    HOURS_24 = "24h"
    HOURS_12 = "12h"


class DigitalWatch(Watch):
    """Implementation of a digital watch."""
    
    def __init__(self, theme: Theme = LightTheme(), time_format: str = TimeFormat.HOURS_24):
        super().__init__(theme)
        self.time_format = time_format
        self._turtle = turtle.Turtle()
        self._turtle.hideturtle()
    
    def setup(self) -> None:
        """Set up the digital watch components."""
        self._turtle.penup()
        self._turtle.goto(0, 0)
        self._turtle.color(self.theme.digit_color)
    
    def update(self) -> None:
        """Update the digital watch display based on current time."""
        current_time = datetime.now()
        
        # Format time based on selected format
        if self.time_format == TimeFormat.HOURS_12:
            hour = current_time.hour % 12
            if hour == 0:
                hour = 12
            am_pm = "AM" if current_time.hour < 12 else "PM"
            time_str = f"{hour:02d}:{current_time.minute:02d}:{current_time.second:02d} {am_pm}"
        else:
            time_str = f"{current_time.hour:02d}:{current_time.minute:02d}:{current_time.second:02d}"
        
        # Clear previous time and draw new time
        self._turtle.clear()
        self._turtle.write(time_str, align="center", font=("Arial", 36, "bold"))


class Alarm:
    """Class for implementing alarm functionality."""
    
    def __init__(self):
        self.alarms: list[tuple[int, int, int]] = []  # List of (hour, minute, second) tuples
    
    def add_alarm(self, hour: int, minute: int, second: int = 0) -> None:
        """Add a new alarm time."""
        self.alarms.append((hour, minute, second))
    
    def remove_alarm(self, hour: int, minute: int, second: int = 0) -> bool:
        """Remove an existing alarm time. Returns True if successful."""
        alarm = (hour, minute, second)
        if alarm in self.alarms:
            self.alarms.remove(alarm)
            return True
        return False
    
    def check_alarms(self, current_time: datetime) -> bool:
        """Check if any alarm should trigger at the current time."""
        current_hms = (current_time.hour, current_time.minute, current_time.second)
        return current_hms in self.alarms


class WatchWithAlarm(ABC):
    """Mixin class for adding alarm functionality to watches."""
    
    def __init__(self):
        self.alarm = Alarm()
    
    def add_alarm(self, hour: int, minute: int, second: int = 0) -> None:
        """Add a new alarm time."""
        self.alarm.add_alarm(hour, minute, second)
    
    def check_and_trigger_alarm(self) -> bool:
        """Check if any alarm should trigger and handles it if needed."""
        current_time = datetime.now()
        if self.alarm.check_alarms(current_time):
            self._trigger_alarm()
            return True
        return False
    
    def _trigger_alarm(self) -> None:
        """Handle alarm triggering."""
        # Placeholder for alarm trigger logic
        # This could flash the screen, play a sound, etc.
        pass


# Example combined class
class AnalogWatchWithAlarm(AnalogWatch, WatchWithAlarm):
    """Analog watch with alarm functionality."""
    
    def __init__(self, theme: Theme = LightTheme(), radius: float = 200):
        AnalogWatch.__init__(self, theme, radius)
        WatchWithAlarm.__init__(self)
    
    def update(self) -> None:
        """Update the watch and check for alarms."""
        super().update()
        self.check_and_trigger_alarm()