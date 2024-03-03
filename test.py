class Dad:
    def __init__(self):
        self.var = "public"
        self._provar = "protected"
        self.__privar = "private"
    @property
    def privar(self):
        return self.__privar

class Son(Dad):
    def __init__(self):
        super().__init__()
        print(self.var)
        print(self._provar)
        print(self.privar)
        
s = Son()