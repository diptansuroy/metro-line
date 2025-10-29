class Ticket:
    def __init__(self, ticket_id, from_station, to_station, price, path, instructions):
        self.ticket_id = ticket_id
        self.from_station = from_station
        self.to_station = to_station
        self.price = price
        self.path = path
        self.instructions = instructions
