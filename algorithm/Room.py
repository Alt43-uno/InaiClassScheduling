
class Room:
    _next_room_id = 0

    def __init__(self, name, lab, number_of_seats):
        self.Id = Room._next_room_id
        Room._next_room_id += 1
        self.Name = name
        self.Lab = lab
        self.NumberOfSeats = number_of_seats

    @staticmethod
    def restartIDs() -> None:
        Room._next_room_id = 0
