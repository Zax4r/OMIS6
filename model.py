from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass

# ==================== Enums ====================

class IncidentType(Enum):
    ACCIDENT = "accident"
    CONGESTION = "congestion"
    ROAD_CLOSURE = "road_closure"
    CONSTRUCTION = "construction"
    OTHER = "other"

class IncidentStatus(Enum):
    REPORTED = "reported"
    CONFIRMED = "confirmed"
    RESOLVED = "resolved"
    FALSE_ALARM = "false_alarm"

class Phase(Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"
    OFF = "off"

class Status(Enum):
    OPERATIONAL = "operational"
    MALFUNCTION = "malfunction"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"

class SensorType(Enum):
    TRAFFIC_FLOW = "traffic_flow"
    SPEED = "speed"
    CAMERA = "camera"
    WEATHER = "weather"

# ==================== Helper Classes ====================

@dataclass
class GeoPoint:
    """Represents a geographic point"""
    x: float
    y: float
    
    def distance_to(self, other: 'GeoPoint') -> float:
        """Calculate distance to another point"""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

@dataclass
class DateRange:
    """Date range for reports"""
    start_date: datetime
    end_date: datetime

class SensorData:
    """Data collected by sensor"""
    def __init__(self, value: float, timestamp: datetime, sensor_id: str):
        self.value = value
        self.timestamp = timestamp
        self.sensor_id = sensor_id

# ==================== Main Model Classes ====================

class Sensor:
    def __init__(self, sensorId: str, location: GeoPoint, sensor_type: SensorType):
        self.sensorId = sensorId
        self.location = location
        self.type = sensor_type
    
    def readData(self) -> SensorData:
        """Read data from the sensor"""
        return SensorData(
            value=0.0, 
            timestamp=datetime.now(),
            sensor_id=self.sensorId
        )



class Camera:
    def __init__(self, resolution: str):
        self.resolution = resolution
    
    def recognizePlate(self) -> str:
        """Perform license plate recognition and return result"""
        return f"PLATE_{datetime.now().timestamp():.0f}"

class TrafficData:
    def __init__(self, flowRate: float, averageSpeed: float, congestionLevel: int):
        self.flowRate = flowRate
        self.averageSpeed = averageSpeed
        self.congestionLevel = congestionLevel

class Operator:
    def __init__(self, shiftId: str):
        self.shiftId = shiftId
    
    def verificationLevel(self, level: str) -> None:
        """Set verification level"""
        print(f"Setting verification level to: {level}")
    
    def manualOverrideIgnite(self, overrideId: str) -> None:
        """Manual override ignition"""
        print(f"Operator manual override lightIdd: {overrideId}")

class User:
    def __init__(self, userId: str, role: str, name: str = ''):
        self.userId = userId
        self.role = role
        self.name = name
    
    def login(self) -> None:
        """User login method"""
        print(f"User {self.userId} logged in")

class AnalysisReport:
    def __init__(self, reportId: str, totalIncidents: int, averageCongestion: float, period: DateRange):
        self.reportId = reportId
        self.totalIncidents = totalIncidents
        self.averageCongestion = averageCongestion
        self.period = period
    
    def generate(self) -> str:
        """Generate and return file path"""
        filename = f"report_{self.reportId}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        print(f"Report generated: {filename}")
        return filename

class Incident:
    def __init__(self, incidentId: str, type: IncidentType, location: GeoPoint, 
                 severity: int, timestamp: datetime):
        self.incidentId = incidentId
        self.type = type
        self.location = location
        self.severity = severity
        self.timestamp = timestamp
        self.status = IncidentStatus.REPORTED
    
    def updateStatus(self, status: IncidentStatus) -> None:
        """Update incident status"""
        self.status = status
        print(f"Incident {self.incidentId} status updated to: {status.value}")

class TrafficLight:
    def __init__(self, lightId: str, location: GeoPoint):
        """
        Args:
            lightId: Идентификатор включения/активации светофора
            question_component: Компонент вопросов/управления
            location: Местоположение светофора
        """
        self.lightId: str = lightId 
        self.location: GeoPoint = location
        self.currentPhase: Phase = Phase.RED
        self.phaseDuration: int = 0
        self.isOnline: bool = False
    
    def setPhaseUpdate(self, phase: Phase, duration: int) -> None:
        """
        Установить фазу светофора с длительностью
        
        Args:
            phase: Новая фаза светофора
            duration: Длительность фазы в секундах
        """
        if self.confine:
            print(f"⚠️ Traffic light {self.lightId} is confined. Cannot change phase.")
            return
        
        self.currentPhase = phase
        self.baseDataPosition = duration
        
        print(f"✅ Traffic light {self.lightId} phase updated to {phase.value} for {duration} seconds")
    
    def getStatusUp(self) -> Status:
        """
        Получить статус светофора
        
        Returns:
            Статус работы светофора
        """
        if self.confine:
            return Status.MAINTENANCE
        elif self.currentPhase == Phase.OFF:
            return Status.OFFLINE
        elif not self.question_component or "ERROR" in self.question_component:
            return Status.MALFUNCTION
        else:
            return Status.OPERATIONAL
    
    def setConfine(self, confine: bool) -> None:
        """
        Установить/снять ограничение светофора
        
        Args:
            confine: True - заблокировать, False - разблокировать
        """
        self.confine = confine
        status = "CONFINED" if confine else "RELEASED"
        print(f"🔒 Traffic light {self.lightId} {status}")

class GreenwaveStrategy:
    def __init__(self, strategyId: str, route: List[TrafficLight], targetSpeed: int):
        self.strategyId = strategyId
        self.route = route
        self.targetSpeed = targetSpeed
        self.isActive = False
    
    def activate(self) -> None:
        """Activate the greenwave strategy"""
        if self.isActive:
            print(f"⚠️ Greenwave strategy {self.strategyId} is already active")
            return
        
        self.isActive = True
        print(f"✅ Greenwave strategy {self.strategyId} activated")
        print(f"   Route: {len(self.route)} traffic lights")
        print(f"   Target speed: {self.targetSpeed} km/h")
    
    def deactivate(self) -> None:
        """Deactivate the greenwave strategy"""
        if not self.isActive:
            print(f"⚠️ Greenwave strategy {self.strategyId} is not active")
            return
        
        self.isActive = False
        print(f"✅ Greenwave strategy {self.strategyId} deactivated")