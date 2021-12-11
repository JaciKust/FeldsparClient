from FhaDataObjects.NamedDataObject import NamedDataObject


class LightStateDataObject(NamedDataObject):
    def __init__(self, lightIpAddresses, lightMacAddresses, rgbColor, transitionTimeSeconds):
        super("LightStateDataObject")

        self.LightIpAddresses = lightIpAddresses
        self.LightMacAddresses = lightMacAddresses
        self.RgbColor = rgbColor
        self.TransitionTimeSeconds = transitionTimeSeconds
