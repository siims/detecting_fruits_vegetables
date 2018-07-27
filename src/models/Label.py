class Label:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __repr__(self) -> str:
        return "Label('%s';%f.2)" % (self.name, self.score)

    def __str__(self) -> str:
        return "('%s';%f.2)" % (self.name, self.score)
