from pydantic import BaseModel
from typing import List, Optional, Set, Literal
import datetime
from datetime import time, date

class Teacher(BaseModel):
    name: str
    link: Optional[str] = None

class Subject(BaseModel):
    name: str
    teacher: Teacher

class ClassTime(BaseModel):
    start_time: time
    end_time: time

class Classroom(BaseModel):
    room_number: Optional[str]

class Subgroup(BaseModel):
    number: int

class ClassType(BaseModel):
    class_type: Literal['lecture', 'practice']

class UniversityClass(BaseModel):
    subject: Subject
    class_time: ClassTime
    classroom: Classroom
    subgroups: Set[Subgroup]
    class_type: ClassType
    date: Optional[datetime.date] = None

class DailySchedule(BaseModel):
    date: date
    classes: List[UniversityClass]

class WeeklySchedule(BaseModel):
    week_start: date
    week_end: date
    daily_schedules: List[DailySchedule]
