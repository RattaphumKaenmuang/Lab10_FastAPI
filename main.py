import uvicorn
import fastapi
import json
import uuid

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
    
    def add_aircraft(self, aircraft):
        if aircraft.get_aircraft_number() in [a.get_aircraft_number() for a in self.__aircraft_list]:
            return False
        self.__aircraft_list.append(aircraft)
        return True
    
    def get_reservation(self):
        return self.__reservation_list[0]

class Flight():
    def __init__(self, from_location, to_location, flight_number):
        self.__from_location = str(from_location)
        self.__to_location = str(to_location)
        self.__flight_number = str(flight_number)
        
    def get_from_location(self):
        return self.__from_location
    def get_to_location(self):
        return self.__to_location
    def get_flight_number(self):
        return self.__flight_number

class FlightInstance(Flight):
    def __init__(self, flight, aircraft, date):
        super().__init__(flight.get_from_location(), flight.get_to_location(), flight.get_flight_number())
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
    
    def get_aircraft_number(self):
        return self.__aircraft_number
    
    def get_seats(self):
        return self.__seats
class Seat():
    def __init__(self, seat_number, seat_category):
        self.__seat_number = str(seat_number)
        self.__seat_category = str(seat_category)
        
    def get_cost(self):
        return self.__seat_category.get_cost()
    
    def get_seat_number(self):
        return self.__seat_number
    
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
        
class Reservation():
    def __init__(self, passengers: list, flight_instance, reservation_date, flight_seats = [], services = []):
        self.__passengers = passengers
        self.__flight_instance = flight_instance
        self.__reservation_date = reservation_date
        self.__flight_seats = flight_seats
        self.__services = services
        self.__reservation_id = self.__generate_reservation_id()
        
    def __generate_reservation_id(self):
        return str(uuid.uuid4())
    
    def get_reservation_id(self):
        return self.__reservation_id

airport_system = AirportSystem()
def init_db():
    global airport_system
    aircraft1 = Aircraft("B737-800")
    aircraft2 = Aircraft("D999-222")
    first_class = SeatCategory("First-Class", 1000)
    business = SeatCategory("Business", 500)
    economy = SeatCategory("Economy", 200)
    
    flight1 = Flight("DMK", "CNX", "D69")
    flight2 = Flight("CNX", "DMK", "D70")
    
    flight_instance1 = FlightInstance(flight1, aircraft1, "2021-01-01")
    flight_instance2 = FlightInstance(flight2, aircraft2, "2021-01-01")
    
    airport_system.add_aircraft(aircraft1)
    airport_system.add_aircraft(aircraft2)
    
    airport_system.add_flight(flight1)
    airport_system.add_flight(flight2)
    
    for i in range(0, 6):
        for j in range(1, 11):
            alphabet = "ABCDEF"
            seat_class = economy
            if i < 2:
                seat_class = first_class
            elif i < 4:
                seat_class = business
                
            aircraft1.add_seat(Seat(alphabet[i] + str(j), seat_class))
            aircraft2.add_seat(Seat(alphabet[i] + str(j), seat_class))
            
    passenger1 = Passenger("Mr.", "John", "Doe", "Smith", "1990-01-01", "081-234-5678")
    passenger2 = Passenger("Mrs.", "Jane", "", "Smith", "1990-01-01", "069-420-6969")
    
    reservation1 = Reservation(passenger1, flight1, "2021-01-01")
    reservation2 = Reservation(passenger2, flight1, "2021-01-01")
    
    airport_system.add_reservation(reservation1)
    airport_system.add_reservation(reservation2)
    
    
init_db()
    
@app.get("/")
def default():
    return airport_system.get_reservation()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)