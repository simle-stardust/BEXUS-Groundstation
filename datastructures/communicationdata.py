from dataclasses import dataclass

@dataclass
class CommunicationData:
    pingerFlag: bool
    stateSwitchFlag: bool
    valveSwitchFlag: bool
    pumpSwitchFlag: bool

    pingOnce: bool

    pingInterval: int

    stateToSet: int

    valveId: int
    valveStateToSet: int

    pumpId: int
    pumpStateToSet: int