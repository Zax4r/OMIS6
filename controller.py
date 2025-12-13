from typing import Optional, Any, Dict, List
from abc import ABC, abstractmethod
from model import (
    Incident, IncidentType, IncidentStatus, Phase, Status,
    GeoPoint, TrafficData, TrafficLight, DateRange
)
from view import DashboardView, IncidentView, ReportView, ControlPanelView, IView
from repository import (
    IncidentRepository, TrafficLightRepository, 
    UserRepository, RepositoryFactory
)
from datetime import datetime, timedelta

# ==================== Вспомогательные классы ====================

class IncidentData:
    """Data class for creating incidents"""
    def __init__(self, incident_id: str, type: IncidentType, location: GeoPoint, 
                 severity: int, description: str = ""):
        self.incident_id = incident_id
        self.type = type
        self.location = location
        self.severity = severity
        self.description = description

class Request:
    """HTTP request wrapper"""
    def __init__(self, method: str = "GET", path: str = "", data: dict = None):
        self.method = method
        self.path = path
        self.data = data or {}

class Report:
    """Report class"""
    def __init__(self, report_id: str, content: str, format: str = "txt"):
        self.report_id = report_id
        self.content = content
        self.format = format

# ==================== Абстрактный контроллер ====================

class AbstractController(ABC):
    """Abstract base controller"""
    
    @abstractmethod
    def handleRequest(self, req: Request) -> None:
        """Handle incoming request"""
        pass
    
    @abstractmethod
    def updateView(self, data: object) -> None:
        """Update the view with new data"""
        pass

# ==================== Конкретные контроллеры ====================

class IncidentController(AbstractController):
    """Controller for managing incidents"""
    
    def __init__(self, incident_repo: IncidentRepository, incident_view: IncidentView):
        self.incidentRepo = incident_repo
        self.incidentView = incident_view
    
    def createIncident(self, data: IncidentData) -> Incident:
        """Create a new incident"""
        print(f"Creating incident with ID: {data.incident_id}")
        
        incident = Incident(
            incidentId=data.incident_id,
            type=data.type,
            location=data.location,
            severity=data.severity,
            timestamp=datetime.now()
        )
        
        self.incidentRepo.add(incident.incidentId, incident)
        
        # Update view
        self.incidentView.displayAlert(f"New incident created: {data.incident_id}")
        self.incidentView.incidentList.append(incident.incidentId)
        self.incidentView.update()
        
        return incident
    
    def verifyIncident(self, incident_id: str) -> bool:
        """Verify an incident"""
        print(f"Verifying incident: {incident_id}")
        
        incident = self.incidentRepo.getById(incident_id)
        if incident:
            incident.updateStatus(IncidentStatus.CONFIRMED)
            self.incidentRepo.update(incident_id, incident)
            
            # Update view
            self.incidentView.displayAlert(f"Incident {incident_id} verified")
            self.incidentView.update()
            return True
        
        self.incidentView.displayAlert(f"Incident {incident_id} not found")
        return False
    
    def closeIncident(self, incident_id: str) -> bool:
        """Close an incident"""
        print(f"Closing incident: {incident_id}")
        
        incident = self.incidentRepo.getById(incident_id)
        if incident:
            incident.updateStatus(IncidentStatus.RESOLVED)
            self.incidentRepo.update(incident_id, incident)
            
            # Update view
            if incident_id in self.incidentView.incidentList:
                self.incidentView.incidentList.remove(incident_id)
            self.incidentView.displayAlert(f"Incident {incident_id} closed")
            self.incidentView.update()
            return True
        
        self.incidentView.displayAlert(f"Incident {incident_id} not found")
        return False
    
    def handleRequest(self, req: Request) -> Optional[Any]:
        """Handle HTTP request for incidents"""
        print(f"Handling incident request: {req.method} {req.path}")
        
        if req.method == "POST" and req.path == "/incidents":
            incident_data = IncidentData(
                incident_id=req.data.get("id", f"INC_{datetime.now().timestamp():.0f}"),
                type=IncidentType(req.data.get("type", "other")),
                location=GeoPoint(
                    x=float(req.data.get("location_x", 0.0)),
                    y=float(req.data.get("location_y", 0.0))
                ),
                severity=int(req.data.get("severity", 1)),
                description=req.data.get("description", "")
            )
            return self.createIncident(incident_data)
        
        elif req.method == "PUT" and "/incidents/" in req.path:
            incident_id = req.path.split("/")[-1]
            
            if req.data.get("action") == "verify":
                return self.verifyIncident(incident_id)
            elif req.data.get("action") == "close":
                return self.closeIncident(incident_id)
        
        return None
    
    def updateView(self, data: object) -> None:
        """Update the incident view"""
        if isinstance(data, dict):
            self.incidentView.render(data)
            self.incidentView.update()

class TrafficController(AbstractController):
    """Controller for managing traffic lights"""
    
    def __init__(self, light_repo: TrafficLightRepository, dashboard_view: DashboardView):
        self.lightRepo = light_repo
        self.dashboardView = dashboard_view
    
    def setGreenWave(self, route_id: str, lights: List[str]) -> bool:
        """Set green wave for a route"""
        print(f"Setting green wave for route: {route_id}")
        
        route_lights = []
        for light_id in lights:
            light = self.lightRepo.getById(light_id)
            if light:
                route_lights.append(light)
        
        if not route_lights:
            print(f"⚠️ No valid lights found for route {route_id}")
            return False
        
        # Update dashboard
        route_points = [light.location for light in route_lights]
        self.dashboardView.highlightRoute(route_points)
        self.dashboardView.update()
        
        print(f"✅ Green wave set for {len(route_lights)} traffic lights")
        return True
    
    def optimizePhases(self, junction_id: str) -> Dict[str, Any]:
        """Optimize traffic light phases for a junction"""
        print(f"Optimizing phases for junction: {junction_id}")
        
        junction_lights = self.lightRepo.findByIntersection(junction_id)
        
        if not junction_lights:
            return {"error": f"No lights found for junction {junction_id}"}
        
        results = {}
        for light in junction_lights:
            current_status = light.getStatusUp()
            if current_status == Status.OPERATIONAL:
                hour = datetime.now().hour
                if 7 <= hour <= 9 or 16 <= hour <= 18:
                    light.setPhaseUpdate(Phase.GREEN, 45)
                else:
                    light.setPhaseUpdate(Phase.GREEN, 30)
                
                results[light.lightId] = {
                    "new_phase": light.currentPhase.value,
                    "duration": light.phaseDuration
                }
        
        print(f"✅ Phases optimized for {len(results)} lights at junction {junction_id}")
        return results
    
    def manualSwitch(self, light_id: str, phase: Phase, duration: int) -> bool:
        """Manually switch a traffic light phase"""
        print(f"Manually switching light {light_id} to phase {phase.value}")
        
        light = self.lightRepo.getById(light_id)
        if light:
            light.setPhaseUpdate(phase, duration)
            self.lightRepo.update(light_id, light)
            
            # Update dashboard
            self.dashboardView.showTrafficJamLocation(light.location)
            self.dashboardView.update()
            
            print(f"✅ Light {light_id} switched to {phase.value}")
            return True
        
        print(f"⚠️ Failed to switch light {light_id}")
        return False
    
    def handleRequest(self, req: Request) -> Optional[Any]:
        """Handle HTTP request for traffic control"""
        print(f"Handling traffic request: {req.method} {req.path}")
        
        if req.method == "POST" and req.path == "/traffic/greenwave":
            route_id = req.data.get("route_id", "")
            lights = req.data.get("lights", [])
            return self.setGreenWave(route_id, lights)
        
        elif req.method == "POST" and req.path == "/traffic/optimize":
            junction_id = req.data.get("junction_id", "")
            return self.optimizePhases(junction_id)
        
        elif req.method == "PUT" and "/traffic/lights/" in req.path:
            light_id = req.path.split("/")[-1]
            phase_str = req.data.get("phase", "red")
            phase = Phase(phase_str.upper())
            duration = int(req.data.get("duration", 30))
            return self.manualSwitch(light_id, phase, duration)
        
        return None
    
    def updateView(self, data: object) -> None:
        """Update the dashboard view"""
        if isinstance(data, dict):
            self.dashboardView.render(data)
            self.dashboardView.update()

class ReportController(AbstractController):
    """Controller for generating reports"""
    
    def __init__(self, incident_repo: IncidentRepository, report_view: ReportView):
        self.incidentRepo = incident_repo
        self.reportView = report_view
    
    def generateMonthlyReport(self, month: int, year: int) -> Report:
        """Generate monthly traffic report"""
        print(f"Generating monthly report for {month}/{year}")
        
        # Calculate date range
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        date_range = DateRange(start_date, end_date)
        
        # Get incidents for the period
        all_incidents = self.incidentRepo.getAll()
        period_incidents = [
            incident for incident in all_incidents
            if start_date <= incident.timestamp <= end_date
        ]
        
        # Calculate statistics
        total_incidents = len(period_incidents)
        if period_incidents:
            avg_congestion = sum(incident.severity for incident in period_incidents) / total_incidents
        else:
            avg_congestion = 0
        
        # Create report
        report_id = f"REPORT_{year}_{month:02d}"
        report_content = f"Monthly Traffic Report\nPeriod: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\nTotal Incidents: {total_incidents}\nAverage Severity: {avg_congestion:.1f}/5"
        
        report = Report(report_id, report_content)
        
        # Update view
        traffic_data = TrafficData(
            flowRate=total_incidents * 10,
            averageSpeed=50 - (avg_congestion * 5),
            congestionLevel=int(avg_congestion * 20)
        )
        self.reportView.displayStats(traffic_data)
        self.reportView.update()
        
        print(f"✅ Monthly report {report_id} generated")
        return report
    
    def exportToPDF(self, report_id: str) -> str:
        """Export report to PDF format"""
        print(f"Exporting report {report_id} to PDF")
        
        export_path = f"/exports/{report_id}.pdf"
        
        if self.reportView.exportButton:
            self.reportView.exportButton.click()
        
        print(f"✅ Report exported to: {export_path}")
        return export_path
    
    def handleRequest(self, req: Request) -> Optional[Any]:
        """Handle HTTP request for reports"""
        print(f"Handling report request: {req.method} {req.path}")
        
        if req.method == "GET" and req.path == "/reports/monthly":
            month = int(req.data.get("month", datetime.now().month))
            year = int(req.data.get("year", datetime.now().year))
            return self.generateMonthlyReport(month, year)
        
        elif req.method == "POST" and req.path.startswith("/reports/export/"):
            report_id = req.path.split("/")[-1]
            return self.exportToPDF(report_id)
        
        return None
    
    def updateView(self, data: object) -> None:
        """Update the report view"""
        if isinstance(data, TrafficData):
            self.reportView.render(data)
            self.reportView.update()

# ==================== Application Controller ====================

class Application:
    """Main application controller"""
    
    def __init__(self):
        # Get repositories
        self.incident_repo = RepositoryFactory.get_repository("incident")
        self.light_repo = RepositoryFactory.get_repository("trafficlight")
        self.user_repo = RepositoryFactory.get_repository("user")
        
        # Initialize views
        self.incident_view = IncidentView()
        self.dashboard_view = DashboardView()
        self.report_view = ReportView()
        self.control_view = ControlPanelView()
        
        # Initialize controllers
        self.incident_controller = IncidentController(self.incident_repo, self.incident_view)
        self.traffic_controller = TrafficController(self.light_repo, self.dashboard_view)
        self.report_controller = ReportController(self.incident_repo, self.report_view)
        
        print("✅ Application initialized with all controllers")
    
    def dispatch_request(self, controller_type: str, req: Request) -> Optional[Any]:
        """Dispatch request to appropriate controller"""
        controllers = {
            "incident": self.incident_controller,
            "traffic": self.traffic_controller,
            "report": self.report_controller
        }
        
        controller = controllers.get(controller_type)
        if controller:
            return controller.handleRequest(req)
        
        print(f"⚠️ Unknown controller type: {controller_type}")
        return None
    
    def show_view(self, view_type: str) -> None:
        """Show specific view"""
        views = {
            "dashboard": self.dashboard_view,
            "incident": self.incident_view,
            "report": self.report_view,
            "control": self.control_view
        }
        
        view = views.get(view_type)
        if view:
            view.show()
        else:
            print(f"⚠️ Unknown view type: {view_type}")
    
    def hide_view(self, view_type: str) -> None:
        """Hide specific view"""
        views = {
            "dashboard": self.dashboard_view,
            "incident": self.incident_view,
            "report": self.report_view,
            "control": self.control_view
        }
        
        view = views.get(view_type)
        if view:
            view.hide()
        else:
            print(f"⚠️ Unknown view type: {view_type}")