from uuid import uuid4
from typing import List, Dict

class Observation():
    def __init__(self) -> None:
        self._id = ""

        self._arrayConfig = []

        self._freq = 0.0
        self._srcDeclination = 0.0

        self._imagePath = ''

    def init(self) -> None:
        self._id = str(uuid4())

    def setArrayConfig(self, arrayConfig: dict) -> None:
        self._arrayConfig.append(arrayConfig)
    
    def setObservationFreq(self, obsFreq: float) -> None:
        self._freq = obsFreq
    
    def setSrcDeclination(self, srcDeclination:float) -> None:
        self._srcDeclination = srcDeclination
    
    def setImagePath(self, imagePath: str) -> None:
        self._imagePath = imagePath

    def getID(self) -> str:
        return self._id
    
    def clear(self) -> None:
        self._id = ''
 
    def getArrayConfig(self) -> List[Dict]:
        return self._arrayConfig
    
    def getFrequency(self) -> float:
        return self._freq
    
    def getSourceDeclination(self) -> float:
        return self._srcDeclination
    
    def getImagePath(self) -> str:
        return self._imagePath
    
    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'array_config': self._arrayConfig,
            'freq': self._freq,
            'src_declination': self._srcDeclination,
            'image_path': self._imagePath
        }