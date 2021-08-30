from dataclasses import dataclass

@dataclass
class CommunicationData:
    pingerFlag: bool
    stateSwitchFlag: bool
    valveSwitchFlag: bool
    pumpSwitchFlag: bool
    heaterSwitchFlag: bool

    isCommsOnline: bool

    pingOnce: bool

    pingInterval: int

    stateToSet: int

    valveId: int
    valveStateToSet: int

    pumpId: int
    pumpStateToSet: int

    heaterId: int
    heaterStateToSet: int

    stateSwitchStartedAt: float
    valveSwitchStartedAt: float
    pumpSwitchStartedAt: float
    heaterSwitchStartedAt: float
