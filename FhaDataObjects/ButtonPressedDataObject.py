from FhaDataObjects.NamedDataObject import NamedDataObject


class ButtonPressedDataObject(NamedDataObject):
    def __init__(self, buttonName, group, category, triggerPin, buttonPressTime):
        super().__init__("ButtonPressedDataObject")
        self.ButtonName = buttonName
        self.Group = group
        self.Category = category
        self.TriggerPin = triggerPin
        self.ButtonPressTime = buttonPressTime
