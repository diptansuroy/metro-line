class Station:
    def __init__(self, station_id, name, lines):
        self.id = station_id
        self.name = name
        if isinstance(lines, str):
            self.lines = [line for line in lines.split(';')]
        else:
            self.lines = lines
