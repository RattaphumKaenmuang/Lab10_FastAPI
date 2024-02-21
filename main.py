import uvicorn
import fastapi
import json

app = fastapi.FastAPI()

class AirportSystem():
    def __init__(self):
        self.__admin_list = []
        self.__reservation_list = []
        self.__flight_list = []
        self.__flight_instance_list = []
        self.__service_list = []
        self.__aircraft_list = []
    
    def add_reservation(self, reservation):
        if reservation.get_reservation_id() in [r.get_reservation_id() for r in self.__reservation_list]:
                return False
        self.__reservation_list.append(reservation)
        return True
    
    def add_flight(self, flight):
        if flight.get_flight_number() in [f.get_flight_number() for f in self.__flight_list]:
            return False
        self.__flight_list.append(flight)
        return True

class Flight():
    def __init__(self, from_location, to_location, flight_number):
        self.__from_location = str(from_location)
        self.__to_location = str(to_location)
        self.__flight_number = str(flight_number)

class FlightInstance(Flight):
    def __init__(self, aircraft, from_location, to_location, date, flight_number):
        super().__init__(self, from_location, to_location, flight_number)
        self.__flight_seats = []
        self.__time_departure = []
        self.__time_arrival = []
        self.__aircraft = aircraft
        self.__date = date

class Aircraft():
    def __init__(self, aircraft_number, seats = []):
        self.__seats = seats
        self.__aircraft_number = aircraft_number
        
    def add_seat(self, seat):
        if seat.get_seat_number() in [s.get_seat_number() for s in self.__seats]:
            return False
        self.__seats.append(seat)
        
class Seat():
    def __init__(self, seat_number, seat_category, seat_price):
        self.__seat_number = str(seat_number)
        self.__seat_category = str(seat_category)
        
    def get_cost(self):
        return self.__seat_category.get_cost()
    
class SeatCategory():
    def __init__(self, category, price):
        self.__category = str(category)
        self.__price = float(price)
        
    def get_cost(self):
        return self.__price

class FlightSeat(Seat):
    def __init__(self, flight_instance, seat):
        super().__init__(seat.get_seat_number(), seat.get_seat_category(), seat.get_cost())
        self.__flight_instance = flight_instance
        self.__occupied = False
    
    def get_cost(self):
        return self.__seat_category.get_cost()
    
    def get_occupied(self):
        return self.__occupied
    
    def set_occupied(self, occupied):
        if occupied not in [True, False]:
            return False
        self.__occupied = occupied
        return True

class Service():
    def __init__(self, service_name, service_price):
        self.__service_name = str(service_name)
        self.__service_price = float(service_price)

    def get_cost(self):
        return self.__service_price
class Passenger():
    def __init__(self, title, first_name, middle_name, last_name, date_of_birth, phone_number):
        self.__title = str(title)
        self.__first_name = str(first_name)
        self.__middle_name = str(middle_name) if middle_name else None
        self.__last_name = str(last_name)
        self.__date_of_birth = date_of_birth
        self.__phone_number = phone_number if phone_number else None
        
def init_db():
    global airport_system
    airport_system = AirportSystem()
    

@app.get("/")
def default():
    return "ok"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)