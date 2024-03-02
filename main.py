import uvicorn
import fastapi
import json
import uuid
from fastapi.middleware.cors import CORSMiddleware


app = fastapi.FastAPI()

origins = [
    "http://localhost:5500",  # Replace with the origin of your frontend
    "http://127.0.0.1:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class AirportSystem():
    def __init__(self):
        self.__admin_list = []
        self.__reservation_list = []
        self.__flight_list = []
        self.__flight_instance_list = []
        self.__service_list = []
        self.__aircraft_list = []
    
    def add_reservation(self, reservation):
        if reservation.get_booking_reference() in [r.get_booking_reference() for r in self.__reservation_list]:
            return False
        self.__reservation_list.append(reservation)
        return True
    
    def add_service(self, service):
        if service.get_name() in [s.get_name() for s in self.__service_list]:
            return False
        self.__service_list.append(service)
        return True
    
    def add_flight(self, flight):
        if flight.get_flight_number() in [f.get_flight_number() for f in self.__flight_list]:
            return False
        self.__flight_list.append(flight)
        return True
    
    def add_flight_instance(self, flight_instance):
        self.__flight_instance_list.append(flight_instance)
        return True
    
    def add_aircraft(self, aircraft):
        if aircraft.get_aircraft_number() in [a.get_aircraft_number() for a in self.__aircraft_list]:
            return False
        self.__aircraft_list.append(aircraft)
        return True
    
    def get_reservation_list(self):
        return self.__reservation_list
    
    def get_service_list(self):
        return self.__service_list
    
    def search_reservation_from_reference(self, booking_reference):
        for r in self.__reservation_list:
            if r.get_booking_reference() == booking_reference:
                return r
        return None
    
    def search_flight_instance(self, date, flight_number):
        for f in self.__flight_instance_list:
            print(f"{f.get_date()} vs {date}, {f.get_flight_number()} vs {flight_number}")
            if f.get_date() == date and f.get_flight_number() == flight_number:
                return f

    def search_service_from_name(self, name):
        for s in self.__service_list:
            if s.get_name() == name:
                return s
    
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
        
    def get_flight_seat_list(self):
        return self.__flight_seats
    
    def search_seat_from_number(self, seat_number):
        for f_seat in self.__flight_seats:
            if f_seat.get_seat_number() == seat_number:
                return f_seat
        
    def get_date(self):
        return self.__date
    
    def add_flight_seat(self, flight_seat):
        if flight_seat.get_seat_number() in [s.get_seat_number() for s in self.__flight_seats]:
            return False
        self.__flight_seats.append(flight_seat)
        return True

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
        self.__seat_category = seat_category
        
    def get_cost(self):
        return self.__seat_category.get_cost()
    
    def get_seat_number(self):
        return self.__seat_number
    
    def get_seat_category(self):
        return self.__seat_category
    
class SeatCategory():
    def __init__(self, category, price):
        self.__category_name = str(category)
        self.__price = float(price)
        
    def get_cost(self):
        return self.__price

class FlightSeat(Seat):
    def __init__(self, seat):
        super().__init__(seat.get_seat_number(), seat.get_seat_category())
        self.__occupied = False
    
    def get_cost(self):
        return self.__seat_category.get_cost()
    
    def is_occupied(self):
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
    def get_name(self):
        return self.__service_name
    
class Passenger():
    def __init__(self, title, first_name, middle_name, last_name, date_of_birth, phone_number):
        self.__title = str(title)
        self.__first_name = str(first_name)
        self.__middle_name = str(middle_name) if middle_name else None
        self.__last_name = str(last_name)
        self.__date_of_birth = date_of_birth
        self.__phone_number = phone_number if phone_number else None
        self.__flight_seat_list = []
        
    def add_flight_seat(self, flight_seat):
        self.__flight_seat_list.append(flight_seat)
        
    def get_first_name(self):
        return self.__first_name
    
    def get_middle_name(self):
        return self.__middle_name
    
    def get_last_name(self):
        return self.__last_name
    
class Reservation():
    def __init__(self, flight_instance, booking_reference, reservation_date, flight_seats = []):
        self.__passengers = []
        self.__flight_instance = flight_instance
        self.__reservation_date = reservation_date
        self.__flight_seats = flight_seats
        self.__services = []
        self.__booking_reference = booking_reference
        
    def __generate_reservation_id(self):
        return str(uuid.uuid4())
    
    def get_booking_reference(self):
        return self.__booking_reference
    
    def get_passenger_from_names(self, first_name, middle_name, last_name):
        for p in self.__passengers:
            p_first = p.get_first_name()
            p_middle = p.get_middle_name()
            p_last = p.get_last_name()
            if p_first == first_name and p_middle == middle_name and p_last == last_name:
                return p
        return None
    
    def add_passenger(self, passenger):
        self.__passengers.append(passenger)

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
            
            seatf1 = FlightSeat(Seat(alphabet[i] + str(j), seat_class))
            seatf2 = FlightSeat(Seat(alphabet[i] + str(j), seat_class))
            
            flight_instance1.add_flight_seat(seatf1)
            flight_instance2.add_flight_seat(seatf2)
            
    passenger1 = Passenger("Mr.", "John", "Doe", "Smith", "1990-01-01", "081-234-5678")
    passenger2 = Passenger("Mrs.", "Jane", "", "Smith", "1990-01-01", "069-420-6969")
    
    reservation1 = Reservation(flight_instance1, "ID1", "2021-01-01")
    reservation2 = Reservation(flight_instance2, "ID2", "2021-01-01")
    
    reservation1.add_passenger(passenger1)
    
    moreBaggage5 = Service("+5 kg Baggage", 200)
    moreBaggage10 = Service("+10 kg Baggage", 400)
    moreBaggage15 = Service("+15 kg Baggage", 600)
    insurance = Service("Insurance", 800)
    
    airport_system.add_service(moreBaggage5)
    airport_system.add_service(moreBaggage10)
    airport_system.add_service(moreBaggage15)
    airport_system.add_service(insurance)
    
    airport_system.add_aircraft(aircraft1)
    airport_system.add_aircraft(aircraft2)
    
    airport_system.add_flight(flight1)
    airport_system.add_flight(flight2)
    
    airport_system.add_flight_instance(flight_instance1)
    airport_system.add_flight_instance(flight_instance2)
    
    airport_system.add_reservation(reservation1)
    airport_system.add_reservation(reservation2)
    
    
init_db()

@app.get("/")
def default():
    return airport_system.get_reservation_list()

@app.get("/get-seats-list")
def get_seats_list(date, flight_number):
    return airport_system.search_flight_instance(date, flight_number).get_flight_seat_list()

@app.put("/choose-seat")
def choose_seat(date, booking_reference, flight_number, first_name, middle_name, last_name, seat_number):
    flight_instance = airport_system.search_flight_instance(date, flight_number)
    f_seat = flight_instance.search_seat_from_number(seat_number)
    reservation = airport_system.search_reservation_from_reference(booking_reference)
    passenger = reservation.get_passenger_from_names(first_name, middle_name, last_name)
    
    if(f_seat and not f_seat.is_occupied()):
        passenger.add_flight_seat(f_seat)
        return True
    return False

@app.get("/get-all-services")
def get_all_services():
    return airport_system.get_service_list()

@app.put("/apply-services")
def apply_services(date, booking_reference, flight_number, first_name, middle_name, last_name, service_name):
    reservation = airport_system.search_reservation_from_reference(booking_reference)
    passenger = reservation.get_passenger_from_names(first_name, middle_name, last_name)
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)