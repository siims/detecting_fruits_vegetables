class Result:
    def __init__(self, given_image_filename, labels) -> None:
        self.given_image_filename = given_image_filename
        self.labels = labels

    def __repr__(self) -> str:
        return "Result(%s;#labels:%d)" % (self.given_image_filename, len(self.labels))

    def __str__(self) -> str:
        return "%s; [%s]" % (self.given_image_filename, ",".join(map(str, self.labels)))
