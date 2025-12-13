from typing import List, Optional, Callable, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from model import TrafficData, GeoPoint, Phase, Status

# ==================== Интерфейс IView ====================

class IView(ABC):
    """Интерфейс для всех представлений"""
    
    @abstractmethod
    def render(self, data: Any) -> None:
        """Отрисовать представление с данными"""
        pass
    
    @abstractmethod
    def update(self) -> None:
        """Обновить представление"""
        pass
    
    @abstractmethod
    def show(self) -> None:
        """Показать представление"""
        pass
    
    @abstractmethod
    def hide(self) -> None:
        """Скрыть представление"""
        pass

# ==================== Helper Classes for View ====================

@dataclass
class MapWidget:
    """Widget for displaying maps"""
    zoom_level: int = 10
    center: Optional[GeoPoint] = None
    
    def set_center(self, point: GeoPoint) -> None:
        """Set the center of the map"""
        self.center = point
        print(f"Map center set to: ({point.x}, {point.y})")

class Layer:
    """Layer for map overlay"""
    def __init__(self, name: str, visible: bool = True):
        self.name = name
        self.visible = visible

class VideoComponent:
    """Video component for displaying camera feeds"""
    def __init__(self, camera_id: str = "", source: str = ""):
        self.camera_id = camera_id
        self.source = source
        self.is_playing = False
    
    def play(self, camera_id: str = "") -> None:
        """Play the video"""
        if camera_id:
            self.camera_id = camera_id
        self.is_playing = True
        print(f"Playing video from camera: {self.camera_id}")
    
    def pause(self) -> None:
        """Pause the video"""
        self.is_playing = False
        print("Video paused")

class ChartWidget:
    """Widget for displaying charts"""
    def __init__(self, chart_type: str = "line"):
        self.chart_type = chart_type
        self.data: List[float] = []
    
    def update_data(self, data: List[float]) -> None:
        """Update chart data"""
        self.data = data
        print(f"Chart data updated with {len(data)} points")

class Button:
    """Button UI component"""
    def __init__(self, label: str, enabled: bool = True):
        self.label = label
        self.enabled = enabled
        self.on_click_callback: Optional[Callable] = None
    
    def set_on_click(self, callback: Callable) -> None:
        """Set click event handler"""
        self.on_click_callback = callback
    
    def click(self) -> None:
        """Simulate button click"""
        if self.enabled and self.on_click_callback:
            print(f"Button '{self.label}' clicked")
            self.on_click_callback()
        elif not self.enabled:
            print(f"Button '{self.label}' is disabled")

class Switch:
    """Toggle switch UI component"""
    def __init__(self, label: str = "", state: bool = False):
        self.label = label
        self.state = state
    
    def toggle(self) -> bool:
        """Toggle switch state"""
        self.state = not self.state
        status = "ON" if self.state else "OFF"
        print(f"Switch '{self.label}' toggled to: {status}")
        return self.state

# ==================== View Classes (реализуют IView) ====================

class DashboardView(IView):
    """Dashboard view with map and traffic visualization"""
    
    def __init__(self):
        self.mapComponent = MapWidget()
        self.trafficLayer = Layer(name="Traffic", visible=True)
        self.controlPanelView = ControlPanelView()
        self.is_visible = False
    
    def render(self, data: Any) -> None:
        """Отрисовать дашборд с данными"""
        if isinstance(data, dict) and 'location' in data:
            self.showTrafficJamLocation(data['location'])
        print("Dashboard rendered")
    
    def update(self) -> None:
        """Обновить дашборд"""
        print("Dashboard updated")
    
    def show(self) -> None:
        """Показать дашборд"""
        self.is_visible = True
        print("Dashboard shown")
    
    def hide(self) -> None:
        """Скрыть дашборд"""
        self.is_visible = False
        print("Dashboard hidden")
    
    def showTrafficJamLocation(self, location: GeoPoint) -> None:
        """Show traffic jam location on the map"""
        self.mapComponent.set_center(location)
    
    def highlightRoute(self, route: List[GeoPoint]) -> None:
        """Highlight a route on the map"""
        print(f"Highlighting route with {len(route)} points")

class IncidentView(IView):
    """View for displaying and managing incidents"""
    
    def __init__(self):
        self.incidentList: List[str] = []
        self.videoComponent = VideoComponent()
        self.is_visible = False
    
    def render(self, data: Any) -> None:
        """Отрисовать представление инцидентов"""
        if isinstance(data, dict):
            if 'incident_id' in data:
                self.showDetails(data['incident_id'])
            if 'alert' in data:
                self.displayAlert(data['alert'])
        print("IncidentView rendered")
    
    def update(self) -> None:
        """Обновить представление инцидентов"""
        print(f"IncidentView updated with {len(self.incidentList)} incidents")
    
    def show(self) -> None:
        """Показать представление инцидентов"""
        self.is_visible = True
        print("IncidentView shown")
    
    def hide(self) -> None:
        """Скрыть представление инцидентов"""
        self.is_visible = False
        print("IncidentView hidden")
    
    def showDetails(self, incident_id: str) -> None:
        """Show details of a specific incident"""
        print(f"Showing details for incident ID: {incident_id}")
    
    def displayAlert(self, message: str) -> None:
        """Display an alert message"""
        print(f"ALERT: {message}")

class ReportView(IView):
    """View for displaying traffic reports and statistics"""
    
    def __init__(self):
        self.charts = ChartWidget(chart_type="bar")
        self.exportButton = Button(label="Export Report", enabled=True)
        self.is_visible = False
    
    def render(self, data: Any) -> None:
        """Отрисовать представление отчетов"""
        if isinstance(data, TrafficData):
            self.displayStats(data)
        print("ReportView rendered")
    
    def update(self) -> None:
        """Обновить представление отчетов"""
        print("ReportView updated")
    
    def show(self) -> None:
        """Показать представление отчетов"""
        self.is_visible = True
        print("ReportView shown")
    
    def hide(self) -> None:
        """Скрыть представление отчетов"""
        self.is_visible = False
        print("ReportView hidden")
    
    def displayStats(self, metrics: TrafficData) -> None:
        """Display traffic statistics"""
        print(f"Displaying traffic statistics:")
        print(f"  Flow Rate: {metrics.flowRate} vehicles/hour")
        print(f"  Average Speed: {metrics.averageSpeed} km/h")
        print(f"  Congestion Level: {metrics.congestionLevel}%")

class ControlPanelView(IView):
    """View for controlling traffic lights and manual overrides"""
    
    def __init__(self):
        self.lightControls: List[Button] = []
        self.manualModeToggle = Switch(label="Manual Mode", state=False)
        self.is_visible = False
        
        # Initialize light control buttons
        self._initialize_light_controls()
    
    def _initialize_light_controls(self) -> None:
        """Initialize traffic light control buttons"""
        light_ids = ["TL001", "TL002", "TL003", "TL004"]
        
        for light_id in light_ids:
            button = Button(label=f"Control {light_id}", enabled=True)
            button.set_on_click(lambda lid=light_id: self._on_light_control_click(lid))
            self.lightControls.append(button)
    
    def _on_light_control_click(self, light_id: str) -> None:
        """Handle light control button click"""
        if self.manualModeToggle.state:
            print(f"Manual control activated for light: {light_id}")
        else:
            print(f"Cannot control {light_id}. Manual mode is OFF")
    
    def render(self, data: Any) -> None:
        """Отрисовать панель управления"""
        if isinstance(data, dict) and 'light_status' in data:
            self.showLightsStatus(data['light_id'], data['light_status'])
        print("ControlPanelView rendered")
    
    def update(self) -> None:
        """Обновить панель управления"""
        print("ControlPanelView updated")
    
    def show(self) -> None:
        """Показать панель управления"""
        self.is_visible = True
        print("ControlPanelView shown")
    
    def hide(self) -> None:
        """Скрыть панель управления"""
        self.is_visible = False
        print("ControlPanelView hidden")
    
    def showLightsStatus(self, light_id: str, status: str) -> None:
        """Show status of a specific traffic light"""
        print(f"Traffic Light {light_id} Status: {status}")