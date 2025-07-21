from enum import Enum


class OperationType(str, Enum):
    CUTTING = "Обработка резанием"
    PRESSING = "Обработка давлением"


class MetalType(str, Enum):
    NONFERROUS = "Металлы цветные"
    FERROUS = "Металлы черные"
    NONMETALLIC = "Неметаллические материалы"
