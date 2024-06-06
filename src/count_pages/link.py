class Link:
    """Using this class, you can get a link based on the entered parameters"""
    def __init__(self, region, car=None, model=None):
        self.region = region
        self.car = car
        self.model = model

    def create_link(self) -> str:
        link = "https://auto.ru"
        link += "/" + self.region + "/"
        link += "cars/"
        if self.car is not None:
            link += self.car + "/"
        if self.model is not None:
            link += self.model + "/"
        link += "all/"

        return link
