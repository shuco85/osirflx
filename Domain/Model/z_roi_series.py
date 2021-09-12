class ZRoiSeries:
    def __init__(self, pk, name, color):
        self.pk = pk
        self.name = name
        self.color = color

    def __str__(self):
        return f"Pk: {self.pk}\n Name: {self.name}\n Color: {self.color}"
