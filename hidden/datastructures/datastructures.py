from pydantic import BaseModel
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

class AddPersonRequest(BaseModel):
    target: str
    name: str

class AddNodeRequest(BaseModel):
    id: str
    label: str
    type: str

class AddEdgeRequest(BaseModel):
    id: str
    source: str
    target: str
    distance: int

class AddEmergencyRequest(BaseModel):
    id: str
    source: str
    target: str
    distance: int

class FirstResponderRequest(BaseModel):
    source: str

class PersonAdded(BaseModel):
    time: int
    data: AddPersonRequest

class EdgeAdded(BaseModel):
    time: int
    data: AddEdgeRequest

class NodeAdded(BaseModel):
    time: int
    data: AddNodeRequest

class EmergencyAdded(BaseModel):
    time: int
    data: Dict[str, Any]

class FirstResponderRequested(BaseModel):
    time: int
    data: FirstResponderRequest