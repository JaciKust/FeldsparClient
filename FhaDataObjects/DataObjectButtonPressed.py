from FhaDataObjects.DataObjectBase import DataObjectBase


class DataObjectButtonPressed(DataObjectBase):
    def __init__(self, buttonName, group, category, triggerPin, buttonPressTime):
        super().__init__("DataObjectButtonPressed")
        self.ButtonName = buttonName
        self.Group = group
        self.Category = category
        self.TriggerPin = triggerPin
        self.ButtonPressTime = buttonPressTime
