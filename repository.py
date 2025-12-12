from typing import Dict, List, Optional, Any, TypeVar, Generic
from abc import ABC, abstractmethod
from model import GetPoint, Incident, TrafficLight, User, TrafficData, Phase, Status
from datetime import datetime
import json

T = TypeVar('T')


class Repository(Generic[T], ABC):
    """Абстрактный базовый класс репозитория"""
    
    def __init__(self):
        self._storage: Dict[str, T] = {}
    
    def getById(self, id: str) -> Optional[T]:
        """Получить объект по ID"""
        return self._storage.get(id)
    
    def getByType(self, type_str: str) -> List[T]:
        """Получить объекты по типу"""
        return [obj for obj in self._storage.values() 
                if hasattr(obj, 'type') and getattr(obj, 'type', None) == type_str]
    
    def add(self, id: str, obj: T) -> None:
        """Добавить объект"""
        if id in self._storage:
            print(f"Объект с ID {id} уже существует, обновление...")
        self._storage[id] = obj
        print(f"Объект {id} добавлен в репозиторий")
    
    def update(self, id: str, obj: T) -> None:
        """Обновить объект"""
        if id in self._storage:
            self._storage[id] = obj
            print(f"Объект {id} обновлен")
        else:
            print(f"Объект с ID {id} не найден")
    
    def delete(self, id: str) -> None:
        """Удалить объект по ID"""
        if id in self._storage:
            del self._storage[id]
            print(f"Объект {id} удален")
        else:
            print(f"Объект с ID {id} не найден")
    
    def getAll(self) -> List[T]:
        """Получить все объекты"""
        return list(self._storage.values())
    
    def count(self) -> int:
        """Получить количество объектов"""
        return len(self._storage)
    
    def exists(self, id: str) -> bool:
        """Проверить существование объекта"""
        return id in self._storage


class UserRepository(Repository[User]):
    """Репозиторий для управления пользователями"""
    
    def __init__(self):
        super().__init__()
        self._initialize_sample_users()
    
    def _initialize_sample_users(self) -> None:
        """Инициализация тестовыми пользователями"""
        users = [
            User(userId="admin", userID="admin", role="administrator"),
            User(userId="operator1", userID="operator1", role="operator"),
            User(userId="operator2", userID="operator2", role="operator"),
            User(userId="viewer1", userID="viewer1", role="viewer"),
        ]
        
        for user in users:
            self.add(user.userId, user)
    
    def findByUserId(self, user_id: str) -> Optional[User]:
        """Найти пользователя по ID"""
        return self.getById(user_id)
    
    def findByRole(self, role: str) -> List[User]:
        """Найти пользователей по роли"""
        return [user for user in self._storage.values() if user.role == role]
    
    def getUserConnections(self) -> List[Dict[str, Any]]:
        """Получить информацию о подключениях пользователей"""
        connections = []
        for user_id, user in self._storage.items():
            connections.append({
                "userId": user_id,
                "role": user.role,
                "isActive": True
            })
        return connections


class IncidentRepository(Repository[Incident]):
    """Репозиторий для управления инцидентами"""
    
    def __init__(self):
        super().__init__()
        self._initialize_sample_incidents()
    
    def _initialize_sample_incidents(self) -> None:
        """Инициализация тестовыми инцидентами"""
        from model import IncidentType, ObjectStatus
        
        incidents = [
            Incident(
                incidentId="INC001",
                type=IncidentType.ACCIDENT,
                location=GetPoint(40.7128, -74.0060),
                activity=ObjectStatus.ACTIVE,
                timestamp=datetime.now()
            ),
            Incident(
                incidentId="INC002",
                type=IncidentType.CONGESTION,
                location=GetPoint(40.7580, -73.9855),
                activity=ObjectStatus.ACTIVE,
                timestamp=datetime.now()
            ),
            Incident(
                incidentId="INC003",
                type=IncidentType.CONSTRUCTION,
                location=GetPoint(40.7549, -73.9840),
                activity=ObjectStatus.ACTIVE,
                timestamp=datetime.now()
            ),
        ]
        
        for incident in incidents:
            self.add(incident.incidentId, incident)
    
    def findActive(self) -> List[Incident]:
        """Найти активные инциденты"""
        return [incident for incident in self._storage.values() 
                if incident.activity.value == "active"]
    
    def findByLocation(self, location: GetPoint, radius: float = 0.01) -> List[Incident]:
        """Найти инциденты вблизи указанной локации"""
        nearby_incidents = []
        for incident in self._storage.values():
            distance = abs(incident.location.x - location.x) + abs(incident.location.y - location.y)
            if distance <= radius:
                nearby_incidents.append(incident)
        return nearby_incidents
    
    def archiveIncident(self, incident_id: str) -> None:
        """Архивировать инцидент"""
        incident = self.getById(incident_id)
        if incident:
            from model import ObjectStatus
            incident.activity = ObjectStatus.INACTIVE
            self.update(incident_id, incident)
            print(f"Инцидент {incident_id} заархивирован")
    
    def getIncidentsByType(self, incident_type: str) -> List[Incident]:
        """Получить инциденты по типу"""
        return [incident for incident in self._storage.values() 
                if incident.type.value == incident_type]
    
    def getIncidentStatistics(self) -> Dict[str, Any]:
        """Получить статистику по инцидентам"""
        total = self.count()
        active = len(self.findActive())
        
        type_counts = {}
        for incident in self._storage.values():
            type_str = incident.type.value
            type_counts[type_str] = type_counts.get(type_str, 0) + 1
        
        return {
            "total_incidents": total,
            "active_incidents": active,
            "by_type": type_counts,
            "last_updated": datetime.now().isoformat()
        }


class TrafficLightRepository(Repository[TrafficLight]):
    """Репозиторий для управления светофорами"""
    
    def __init__(self):
        super().__init__()
        self._traffic_data_cache: Dict[str, List[TrafficData]] = {}
        self._initialize_sample_traffic_lights()
    
    def _initialize_sample_traffic_lights(self) -> None:
        """Инициализация тестовыми светофорами"""
        traffic_lights = [
            TrafficLight(loginId="TL001", location=GetPoint(40.7128, -74.0060)),
            TrafficLight(loginId="TL002", location=GetPoint(40.7580, -73.9855)),
            TrafficLight(loginId="TL003", location=GetPoint(40.7549, -73.9840)),
            TrafficLight(loginId="TL004", location=GetPoint(40.7489, -73.9680)),
        ]
        
        traffic_lights[0].setPhase(Phase.GREEN, 30)
        traffic_lights[1].setPhase(Phase.RED, 20)
        traffic_lights[2].setPhase(Phase.YELLOW, 5)
        
        for light in traffic_lights:
            self.add(light.loginId, light)
    
    def findByIntersection(self, intersection_id: str) -> List[TrafficLight]:
        """Найти светофоры на перекрестке"""
        return [light for light_id, light in self._storage.items() 
                if intersection_id in light_id]
    
    def getDiagnosticDataFor(self, days: int = 7) -> Dict[str, List[Dict[str, Any]]]:
        """Получить диагностические данные за указанное количество дней"""
        diagnostic_data = {}
        
        for light_id, light in self._storage.items():
            light_data = []
            for day in range(days):
                light_data.append({
                    "date": (datetime.now().date().isoformat()),
                    "status": light.getStatus().value,
                    "phase": light.currentPhase.value,
                })
            
            diagnostic_data[light_id] = light_data
        
        return diagnostic_data
    
    def getLatestTrafficData(self) -> Dict[str, TrafficData]:
        """Получить последние данные о трафике для каждого светофора"""
        traffic_data_map = {}
        
        for light_id, light in self._storage.items():
            traffic_data = TrafficData(
            )
            traffic_data_map[light_id] = traffic_data
            
            if light_id not in self._traffic_data_cache:
                self._traffic_data_cache[light_id] = []
            self._traffic_data_cache[light_id].append(traffic_data)
        
        return traffic_data_map
    
    def updatePhase(self, light_id: str, phase: Phase, duration: int) -> bool:
        """Обновить фазу светофора"""
        light = self.getById(light_id)
        if light:
            light.setPhase(phase, duration)
            self.update(light_id, light)
            return True
        return False
    
    def getStatusReport(self) -> Dict[str, Dict[str, Any]]:
        """Получить отчет о статусе всех светофоров"""
        report = {}
        
        for light_id, light in self._storage.items():
            report[light_id] = {
                "location": {"x": light.location.x, "y": light.location.y},
                "current_phase": light.currentPhase.value,
                "status": light.getStatus().value,
                "phase_direction": light.phaseDirection,
                "is_active": light.isLocationActive,
                "last_updated": datetime.now().isoformat()
            }
        
        return report
    
    def getTrafficLightsInArea(self, center: GetPoint, radius: float) -> List[TrafficLight]:
        """Получить светофоры в указанной области"""
        lights_in_area = []
        
        for light in self._storage.values():
            distance = ((light.location.x - center.x) ** 2 + 
                       (light.location.y - center.y) ** 2) ** 0.5
            if distance <= radius:
                lights_in_area.append(light)
        
        return lights_in_area


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
    
    @staticmethod
    def get_user_repository() -> UserRepository:
        """Получить репозиторий пользователей"""
        repo = RepositoryFactory.get_repository("user")
        return repo if isinstance(repo, UserRepository) else UserRepository()
    
    @staticmethod
    def get_incident_repository() -> IncidentRepository:
        """Получить репозиторий инцидентов"""
        repo = RepositoryFactory.get_repository("incident")
        return repo if isinstance(repo, IncidentRepository) else IncidentRepository()
    
    @staticmethod
    def get_traffic_light_repository() -> TrafficLightRepository:
        """Получить репозиторий светофоров"""
        repo = RepositoryFactory.get_repository("trafficlight")
        return repo if isinstance(repo, TrafficLightRepository) else TrafficLightRepository()
    
    @staticmethod
    def clear_all():
        """Очистить все репозитории (для тестирования)"""
        RepositoryFactory._instances.clear()


def save_repository_state(repo: Repository, filename: str) -> bool:
    """Сохранить состояние репозитория в файл"""
    try:
        data = {
            "type": repo.__class__.__name__,
            "count": repo.count(),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Состояние репозитория сохранено в {filename}")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении репозитория: {e}")
        return False

def load_repository_state(filename: str) -> Optional[Dict[str, Any]]:
    """Загрузить состояние репозитория из файла"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        print(f"Состояние репозитория загружено из {filename}")
        return data
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке репозитория: {e}")
        return None