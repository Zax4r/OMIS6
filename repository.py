from typing import Dict, List, Optional, TypeVar, Generic, Any
from abc import ABC, abstractmethod
from model import (
    TrafficLight, User, Incident, GeoPoint, 
    IncidentType, IncidentStatus, Phase, Status
)
from datetime import datetime

T = TypeVar('T')

# ==================== Базовый репозиторий ====================

class Repository(Generic[T], ABC):
    """Абстрактный базовый класс репозитория"""
    
    def __init__(self):
        self._storage: Dict[str, T] = {}
    
    def getById(self, id: str) -> Optional[T]:
        """Получить объект по ID"""
        return self._storage.get(id)
    
    def getAll(self) -> List[T]:
        """Получить все объекты"""
        return list(self._storage.values())
    
    def add(self, id: str, obj: T) -> None:
        """Добавить объект"""
        self._storage[id] = obj
    
    def update(self, id: str, obj: T) -> None:
        """Обновить объект"""
        if id in self._storage:
            self._storage[id] = obj
    
    def delete(self, id: str) -> None:
        """Удалить объект по ID"""
        if id in self._storage:
            del self._storage[id]
    
    def count(self) -> int:
        """Получить количество объектов"""
        return len(self._storage)
    
    def exists(self, id: str) -> bool:
        """Проверить существование объекта"""
        return id in self._storage

# ==================== UserRepository ====================

class UserRepository(Repository[User]):
    """Репозиторий для управления пользователями"""
    
    def __init__(self):
        super().__init__()
        self._initialize_sample_users()
    
    def _initialize_sample_users(self) -> None:
        """Инициализация тестовыми пользователями"""
        users = [
            User(userId="admin01", role="administrator", name="Admin User"),
            User(userId="operator01", role="operator", name="John Operator"),
            User(userId="viewer01", role="viewer", name="Viewer User"),
        ]
        
        for user in users:
            self.add(user.userId, user)
    
    def findByUserId(self, user_id: str) -> Optional[User]:
        """Найти пользователя по ID"""
        return self.getById(user_id)
    
    def findByRole(self, role: str) -> List[User]:
        """Найти пользователей по роли"""
        return [user for user in self._storage.values() if user.role == role]

# ==================== IncidentRepository ====================

class IncidentRepository(Repository[Incident]):
    """Репозиторий для управления инцидентами"""
    
    def __init__(self):
        super().__init__()
        self._initialize_sample_incidents()
    
    def _initialize_sample_incidents(self) -> None:
        """Инициализация тестовыми инцидентами"""
        incidents = [
            Incident(
                incidentId="INC001",
                type=IncidentType.ACCIDENT,
                location=GeoPoint(40.7128, -74.0060),
                severity=3,
                timestamp=datetime.now()
            ),
            Incident(
                incidentId="INC002",
                type=IncidentType.CONGESTION,
                location=GeoPoint(40.7580, -73.9855),
                severity=2,
                timestamp=datetime.now()
            ),
        ]
        
        for incident in incidents:
            self.add(incident.incidentId, incident)
    
    def findActive(self) -> List[Incident]:
        """Найти активные инциденты"""
        return [incident for incident in self._storage.values() 
                if incident.status in [IncidentStatus.REPORTED, IncidentStatus.CONFIRMED]]
    
    def findByLocation(self, location: GeoPoint, radius: float = 0.01) -> List[Incident]:
        """Найти инциденты вблизи указанной локации"""
        nearby_incidents = []
        for incident in self._storage.values():
            distance = incident.location.distance_to(location)
            if distance <= radius:
                nearby_incidents.append(incident)
        return nearby_incidents
    
    def findByType(self, incident_type: IncidentType) -> List[Incident]:
        """Найти инциденты по типу"""
        return [incident for incident in self._storage.values() 
                if incident.type == incident_type]

# ==================== TrafficLightRepository ====================

class TrafficLightRepository(Repository[TrafficLight]):
    """Репозиторий для управления светофорами"""
    
    def __init__(self):
        super().__init__()
        self._initialize_sample_lights()
    
    def _initialize_sample_lights(self) -> None:
        """Инициализация тестовыми светофорами"""
        lights = [
            TrafficLight(
                lightId="TL001",
                location=GeoPoint(40.7128, -74.0060)
            ),
            TrafficLight(
                lightId="TL002", 
                location=GeoPoint(40.7580, -73.9855)
            ),
            TrafficLight(
                lightId="TL003",
                location=GeoPoint(40.7549, -73.9840)
            ),
        ]
        
        for light in lights:
            self.add(light.lightId, light)
    
    def findByIntersection(self, intersection_id: str) -> List[TrafficLight]:
        """Найти светофоры на перекрестке"""
        return [light for light_id, light in self._storage.items() 
                if intersection_id in light_id]
    
    def getByStatus(self, status: Status) -> List[TrafficLight]:
        """Найти светофоры по статусу"""
        return [light for light in self._storage.values() 
                if light.getStatusUp() == status]

# ==================== Repository Factory ====================

class RepositoryFactory:
    """Фабрика для создания репозиториев"""
    
    _instances: Dict[str, Repository] = {}
    
    @staticmethod
    def get_repository(repo_type: str) -> Optional[Repository]:
        """Получить экземпляр репозитория по типу"""
        if repo_type not in RepositoryFactory._instances:
            if repo_type == "user":
                RepositoryFactory._instances[repo_type] = UserRepository()
            elif repo_type == "incident":
                RepositoryFactory._instances[repo_type] = IncidentRepository()
            elif repo_type == "trafficlight":
                RepositoryFactory._instances[repo_type] = TrafficLightRepository()
            else:
                return None
        
        return RepositoryFactory._instances[repo_type]