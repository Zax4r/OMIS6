from typing import Optional, Any
from abc import ABC, abstractmethod


from model import Incident, IncidentStatus, Phase, GetPoint, IncidentType, ObjectStatus
from view import DashboardView, IncidentView, ReportView, GeoPoint, TrafficData
from datetime import datetime


class IncidentData:
    """Data class for creating incidents"""
    def __init__(self, incident_id: str, type: IncidentType, location: GetPoint, 
                 description: str = ""):
        self.incident_id = incident_id
        self.type = type
        self.location = location
        self.description = description

class Request:
    """HTTP request wrapper"""
    def __init__(self, method: str = "GET", path: str = "", data: dict = None):
        self.method = method
        self.path = path
        self.data = data or {}

class Report:
    """Report class"""
    def __init__(self, report_id: str, content: str):
        self.report_id = report_id
        self.content = content


class IncidentRepository:
    """Repository for managing incidents"""
    def __init__(self):
        self.incidents = {}
    
    def create(self, incident: Incident) -> None:
        """Create a new incident"""
        self.incidents[incident.incidentId] = incident
        print(f"Incident {incident.incidentId} saved to repository")
    
    def find_by_id(self, incident_id: str) -> Optional[Incident]:
        """Find incident by ID"""
        return self.incidents.get(incident_id)
    
    def update(self, incident: Incident) -> None:
        """Update an existing incident"""
        if incident.incidentId in self.incidents:
            self.incidents[incident.incidentId] = incident
            print(f"Incident {incident.incidentId} updated in repository")
    
    def get_all(self) -> list[Incident]:
        """Get all incidents"""
        return list(self.incidents.values())

class TrafficLightRepository:
    """Repository for managing traffic lights"""
    def __init__(self):
        self.traffic_lights = {}
    
    def find_by_id(self, light_id: str) -> Any:  # Возвращает TrafficLight из model
        """Find traffic light by ID"""
        return self.traffic_lights.get(light_id)
    
    def update_phase(self, light_id: str, phase: Phase) -> None:
        """Update traffic light phase"""
        if light_id in self.traffic_lights:
            light = self.traffic_lights[light_id]
            light.setPhase(phase, 30)  # Default duration
            print(f"Traffic light {light_id} phase updated to {phase.value}")

class AnalyticsService:
    """Service for analytics operations"""
    def generate_monthly_analytics(self, month: int, year: int) -> dict:
        """Generate monthly analytics data"""
        print(f"Generating analytics for {month}/{year}")
        return {
            "month": month,
            "year": year,
            "total_incidents": 0,
            "avg_congestion": 0.0,
            "peak_hours": []
        }
    
    def export_report(self, report_id: str, format: str = "pdf") -> str:
        """Export report in specified format"""
        return f"/exports/{report_id}.{format}"


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


class IncidentController(AbstractController):
    """Controller for managing incidents"""
    
    def __init__(self, incident_repo: IncidentRepository, incident_view: IncidentView):
        self.incidentRepo = incident_repo
        self.incidentView = incident_view
    
    def createIncident(self, data: IncidentData) -> None:
        """Create a new incident"""
        print(f"Creating incident with ID: {data.incident_id}")
        
        incident = Incident(
            incidentId=data.incident_id,
            type=data.type,
            location=data.location,
            activity=ObjectStatus.ACTIVE,
            timestamp=datetime.now()
        )
        
        self.incidentRepo.create(incident)
        
        self.incidentView.displayAlert(f"New incident created: {data.incident_id}")
        
        if incident.incidentId not in self.incidentView.incidentList:
            try:
                incident_num = int(incident.incidentId.replace("INC", ""))
                self.incidentView.incidentList.append(incident_num)
            except ValueError:
                pass
    
    def verifyIncident(self, id: str) -> None:
        """Verify an incident"""
        print(f"Verifying incident: {id}")
        
        incident = self.incidentRepo.find_by_id(id)
        if incident:
            incident.updateStatus(IncidentStatus.CONFIRMED)
            self.incidentRepo.update(incident)
            self.incidentView.displayAlert(f"Incident {id} verified and confirmed")
        else:
            self.incidentView.displayAlert(f"Incident {id} not found")
    
    def closeIncident(self, id: str) -> None:
        """Close an incident"""
        print(f"Closing incident: {id}")
        
        incident = self.incidentRepo.find_by_id(id)
        if incident:
            incident.updateStatus(IncidentStatus.RESOLVED)
            self.incidentRepo.update(incident)
            self.incidentView.displayAlert(f"Incident {id} closed and resolved")
            
            try:
                incident_num = int(id.replace("INC", ""))
                if incident_num in self.incidentView.incidentList:
                    self.incidentView.incidentList.remove(incident_num)
            except ValueError:
                pass
        else:
            self.incidentView.displayAlert(f"Incident {id} not found")
    
    def handleRequest(self, req: Request) -> None:
        """Handle HTTP request for incidents"""
        print(f"Handling incident request: {req.method} {req.path}")
        
        if req.method == "POST" and req.path == "/incidents":
            incident_data = IncidentData(
                incident_id=req.data.get("id", ""),
                type=IncidentType(req.data.get("type", "other")),
                location=GetPoint(
                    x=req.data.get("location_x", 0),
                    y=req.data.get("location_y", 0)
                ),
                description=req.data.get("description", "")
            )
            self.createIncident(incident_data)
        
        elif req.method == "PUT" and "/incidents/" in req.path:
            incident_id = req.path.split("/")[-1]
            
            if req.data.get("action") == "verify":
                self.verifyIncident(incident_id)
            elif req.data.get("action") == "close":
                self.closeIncident(incident_id)
    
    def updateView(self, data: object) -> None:
        """Update the incident view"""
        print("Updating incident view")
        if isinstance(data, dict) and "incident_id" in data:
            self.incidentView.showDetails(data["incident_id"])

class TrafficController(AbstractController):
    """Controller for managing traffic lights"""
    
    def __init__(self, light_repo: TrafficLightRepository, dashboard_view: DashboardView):
        self.lightRepo = light_repo
        self.dashBoardView = dashboard_view
    
    def setGreenWave(self, routed: str) -> None:
        """Set green wave for a route"""
        print(f"Setting green wave for route: {routed}")
        
        route_points = [
            GeoPoint(lat=40.7128, lng=-74.0060),
            GeoPoint(lat=40.7580, lng=-73.9855),
            GeoPoint(lat=40.7549, lng=-73.9840)
        ]
        
        self.dashBoardView.highlightRouteroute(route_points)
        print("Green wave strategy activated")
    
    def optimizePhases(self, junction_id: str) -> None:
        """Optimize traffic light phases for a junction"""
        print(f"Optimizing phases for junction: {junction_id}")
        
        
        traffic_data = {
            "junction": junction_id,
            "optimized": True,
            "new_phases": {"north_south": "GREEN", "east_west": "RED"}
        }
        
        print(f"Phases optimized for junction {junction_id}")
        return traffic_data
    
    def manualSwitch(self, light_id: str, phase: Phase) -> None:
        """Manually switch a traffic light phase"""
        print(f"Manually switching light {light_id} to phase {phase.value}")
        
        self.lightRepo.update_phase(light_id, phase)
        
        if phase == Phase.GREEN:
            location = GeoPoint(lat=40.7128, lng=-74.0060)
            self.dashBoardView.showTrafficJamlocation(location)
    
    def handleRequest(self, req: Request) -> None:
        """Handle HTTP request for traffic control"""
        print(f"Handling traffic request: {req.method} {req.path}")
        
        if req.method == "POST" and req.path == "/traffic/greenwave":
            route_id = req.data.get("route_id", "")
            self.setGreenWave(route_id)
        
        elif req.method == "POST" and req.path == "/traffic/optimize":
            junction_id = req.data.get("junction_id", "")
            self.optimizePhases(junction_id)
        
        elif req.method == "PUT" and "/traffic/lights/" in req.path:
            light_id = req.path.split("/")[-1]
            phase_str = req.data.get("phase", "red")
            phase = Phase(phase_str.upper())
            self.manualSwitch(light_id, phase)
    
    def updateView(self, data: object) -> None:
        """Update the dashboard view"""
        print("Updating traffic dashboard view")
        if isinstance(data, dict) and "location" in data:
            location = GeoPoint(
                lat=data["location"].get("lat", 0),
                lng=data["location"].get("lng", 0)
            )
            self.dashBoardView.showTrafficJamlocation(location)

class ReportController(AbstractController):
    """Controller for generating reports"""
    
    def __init__(self, analytics_service: AnalyticsService, report_view: ReportView):
        self.analyticsService = analytics_service
        self.reportView = report_view
    
    def generateMonthlyReport(self, month: int, year: int) -> Report:
        """Generate monthly traffic report"""
        print(f"Generating monthly report for {month}/{year}")
        
        analytics_data = self.analyticsService.generate_monthly_analytics(month, year)
        
        report_id = f"REPORT_{year}_{month:02d}"
        report_content = f"""
        Monthly Traffic Report
        Period: {month}/{year}
        
        Statistics:
        - Total Incidents: {analytics_data.get('total_incidents', 0)}
        - Average Congestion: {analytics_data.get('avg_congestion', 0.0)}%
        - Peak Hours: {', '.join(map(str, analytics_data.get('peak_hours', [])))}
        """
        
        report = Report(report_id, report_content)
        
        traffic_data = TrafficData()
        traffic_data.incident_count = analytics_data.get('total_incidents', 0)
        traffic_data.congestion_level = analytics_data.get('avg_congestion', 0.0)
        self.reportView.displayStats(traffic_data)
        
        print(f"Monthly report {report_id} generated")
        return report
    
    def exportToPDF(self, report_id: str) -> None:
        """Export report to PDF format"""
        print(f"Exporting report {report_id} to PDF")
        
        export_path = self.analyticsService.export_report(report_id, "pdf")
        
        self.reportView.exportButton.click()
        
        print(f"Report exported to: {export_path}")
    
    def handleRequest(self, req: Request) -> None:
        """Handle HTTP request for reports"""
        print(f"Handling report request: {req.method} {req.path}")
        
        if req.method == "GET" and req.path == "/reports/monthly":
            month = req.data.get("month", datetime.now().month)
            year = req.data.get("year", datetime.now().year)
            report = self.generateMonthlyReport(month, year)
            
            return report
        
        elif req.method == "POST" and req.path.startswith("/reports/export/"):
            report_id = req.path.split("/")[-1]
            self.exportToPDF(report_id)
    
    def updateView(self, data: object) -> None:
        """Update the report view"""
        print("Updating report view")
        if isinstance(data, dict):
            traffic_data = TrafficData()
            traffic_data.flow_rate = data.get("flow_rate", 0)
            traffic_data.congestion_level = data.get("congestion_level", 0)
            traffic_data.incident_count = data.get("incident_count", 0)
            traffic_data.average_speed = data.get("average_speed", 0)
            self.reportView.displayStats(traffic_data)


class Application:
    """Main application controller"""
    
    def __init__(self):
        self.incident_repo = IncidentRepository()
        self.light_repo = TrafficLightRepository()
        self.analytics_service = AnalyticsService()
        
        self.incident_view = IncidentView()
        self.dashboard_view = DashboardView()
        self.report_view = ReportView()
        
        self.incident_controller = IncidentController(self.incident_repo, self.incident_view)
        self.traffic_controller = TrafficController(self.light_repo, self.dashboard_view)
        self.report_controller = ReportController(self.analytics_service, self.report_view)
        
        print("Application initialized with all controllers")
    
    def dispatch_request(self, controller_type: str, req: Request) -> None:
        """Dispatch request to appropriate controller"""
        if controller_type == "incident":
            self.incident_controller.handleRequest(req)
        elif controller_type == "traffic":
            self.traffic_controller.handleRequest(req)
        elif controller_type == "report":
            self.report_controller.handleRequest(req)
        else:
            print(f"Unknown controller type: {controller_type}")