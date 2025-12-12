from typing import List
from dataclasses import dataclass


@dataclass
class GeoPoint:
    """Represents a geographic point with latitude and longitude"""
    lat: float
    lng: float

class MapWidget:
    """Widget for displaying maps"""
    def __init__(self):
        self.zoom_level = 10
        self.center = GeoPoint(0, 0)
    
    def set_center(self, point: GeoPoint):
        """Set the center of the map"""
        self.center = point
        print(f"Map center set to: ({point.lat}, {point.lng})")
    
    def zoom_in(self):
        """Zoom in on the map"""
        self.zoom_level += 1
        print(f"Zoom level: {self.zoom_level}")
    
    def zoom_out(self):
        """Zoom out on the map"""
        self.zoom_level -= 1
        print(f"Zoom level: {self.zoom_level}")

class Layer:
    """Layer for map overlay"""
    def __init__(self, name: str, visible: bool = True):
        self.name = name
        self.visible = visible
    
    def toggle_visibility(self):
        """Toggle layer visibility"""
        self.visible = not self.visible
        status = "visible" if self.visible else "hidden"
        print(f"Layer '{self.name}' is now {status}")

class VideComponent:
    """Video component for displaying camera feeds"""
    def __init__(self, source: str = ""):
        self.source = source
        self.is_playing = False
    
    def play(self):
        """Play the video"""
        self.is_playing = True
        print(f"Playing video from: {self.source}")
    
    def pause(self):
        """Pause the video"""
        self.is_playing = False
        print("Video paused")
    
    def set_source(self, source: str):
        """Set video source"""
        self.source = source
        print(f"Video source set to: {source}")

class ChartWidget:
    """Widget for displaying charts"""
    def __init__(self, chart_type: str = "line"):
        self.chart_type = chart_type
        self.data = []
    
    def update_data(self, data: List[float]):
        """Update chart data"""
        self.data = data
        print(f"Chart data updated with {len(data)} points")
    
    def set_chart_type(self, chart_type: str):
        """Change chart type"""
        self.chart_type = chart_type
        print(f"Chart type changed to: {chart_type}")

class Button:
    """Button UI component"""
    def __init__(self, label: str, enabled: bool = True):
        self.label = label
        self.enabled = enabled
        self.on_click_callback = None
    
    def set_on_click(self, callback):
        """Set click event handler"""
        self.on_click_callback = callback
    
    def click(self):
        """Simulate button click"""
        if self.enabled and self.on_click_callback:
            print(f"Button '{self.label}' clicked")
            self.on_click_callback()
        elif not self.enabled:
            print(f"Button '{self.label}' is disabled")
        else:
            print(f"Button '{self.label}' has no action")

class Switch:
    """Toggle switch UI component"""
    def __init__(self, label: str = "", state: bool = False):
        self.label = label
        self.state = state
    
    def toggle(self):
        """Toggle switch state"""
        self.state = not self.state
        status = "ON" if self.state else "OFF"
        print(f"Switch '{self.label}' toggled to: {status}")
        return self.state
    
    def set_state(self, state: bool):
        """Set switch state"""
        self.state = state
        status = "ON" if self.state else "OFF"
        print(f"Switch '{self.label}' set to: {status}")

class TrafficData:
    """Traffic data for reporting"""
    def __init__(self):
        self.flow_rate = 0.0
        self.congestion_level = 0.0
        self.incident_count = 0
        self.average_speed = 0.0


class DashboardView:
    """Dashboard view with map and traffic visualization"""
    def __init__(self):
        self.mapComponent = MapWidget()
        self.trafficLayer = Layer(name="Traffic", visible=True)
    
    def showTrafficJamlocation(self, location: GeoPoint) -> None:
        """Show traffic jam location on the map"""
        print(f"Showing traffic jam at location: ({location.lat}, {location.lng})")
        self.mapComponent.set_center(location)
    
    def highlightRouteroute(self, route: List[GeoPoint]) -> None:
        """Highlight a route on the map"""
        print(f"Highlighting route with {len(route)} points")
        for i, point in enumerate(route):
            print(f"  Point {i+1}: ({point.lat}, {point.lng})")

class IncidentView:
    """View for displaying and managing incidents"""
    def __init__(self):
        self.incidentList: List[int] = []
        self.videOrder = VideComponent()
    
    def showDetails(self, id: str) -> None:
        """Show details of a specific incident"""
        print(f"Showing details for incident ID: {id}")
    
    def displayAlert(self, msg: str) -> None:
        """Display an alert message"""
        print(f"ALERT: {msg}")

class ReportView:
    """View for displaying traffic reports and statistics"""
    def __init__(self):
        self.charts = ChartWidget(chart_type="bar")
        self.exportButton = Button(label="Export Report", enabled=True)
        self.exportButton.set_on_click(self._on_export_click)
    
    def displayStats(self, metrics: TrafficData) -> None:
        """Display traffic statistics"""
        print(f"Displaying traffic statistics:")
        print(f"  Flow Rate: {metrics.flow_rate}")
        print(f"  Congestion Level: {metrics.congestion_level}%")
        print(f"  Incident Count: {metrics.incident_count}")
        print(f"  Average Speed: {metrics.average_speed} km/h")
        
        chart_data = [
            metrics.flow_rate,
            metrics.congestion_level,
            metrics.incident_count * 10,
            metrics.average_speed
        ]
        self.charts.update_data(chart_data)
    
    def _on_export_click(self) -> None:
        """Handle export button click"""
        print("Exporting report...")

class ControlPaneView:
    """View for controlling traffic lights and manual overrides"""
    def __init__(self):
        self.lightControls: List[Button] = []
        self.manualModeToggle = Switch(label="Manual Mode", state=False)
        self._initialize_light_controls()
    
    def _initialize_light_controls(self) -> None:
        """Initialize traffic light control buttons"""
        light_ids = ["TL001", "TL002", "TL003", "TL004"]
        
        for light_id in light_ids:
            button = Button(label=f"Control {light_id}", enabled=True)
            button.set_on_click(lambda lid=light_id: self._on_light_control_click(lid))
            self.lightControls.append(button)
    
    def showLightsStatus(self, id: str, status: str) -> None:
        """Show status of a specific traffic light"""
        print(f"Traffic Light {id} Status: {status}")
    
    def _on_light_control_click(self, light_id: str) -> None:
        """Handle light control button click"""
        if self.manualModeToggle.state:
            print(f"Manual control activated for light: {light_id}")
        else:
            print(f"Cannot control {light_id}. Manual mode is OFF")