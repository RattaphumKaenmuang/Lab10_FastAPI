
from starlette.responses import HTMLResponse
from typing import Union , Optional
import uvicorn
from fastapi import FastAPI

class AirportSystem:
    __admin_list = []
    __reservation_list = []	
    __flight_list = []
    __flight_instance_list = []
    __aircraft_list = []
    __payment_method_list = []
    __airport_list = []

    def add_payment_method(payment_method) :
        AirportSystem.__payment_method_list.append(payment_method)

    def get_payment_method() :
        return Airport.__payment_method_list

    def reservation_list():
        reservations = []
        for reservation in AirportSystem.__reservation_list:
            reservations.append(reservation.convert_to_json())
        return reservations

    def check_in(booking_reference, name, returnl = False):
        passenger = AirportSystem.check_passenger(booking_reference, name)
        reservation = AirportSystem.find_reservation(booking_reference)
        return AirportSystem.create_boarding_pass(reservation, passenger, returnl)
    
    def create_airport(airport):
        AirportSystem.__airport_list.append(airport)
        return airport
    
    def get_airport_list():
        return AirportSystem.__airport_list

    def create_reservation(reservation):
        AirportSystem.__reservation_list.append(reservation)
        return reservation.convert_to_json()
    
    def find_reservation(booking_reference):
        for reservation in AirportSystem.__reservation_list:
            if reservation.booking_reference == booking_reference:
                return reservation
            
    def check_passenger(booking_reference, name):
        for passenger in AirportSystem.find_reservation(booking_reference).passengers:
            if passenger.name == name:
                return passenger

    def create_boarding_pass(reservation, passenger, returnl = 0):
        reservation.boarding_pass = BoardingPass(reservation, passenger, returnl)
        return BoardingPass(reservation, passenger, returnl)
    
    def flight_instance_list():
        flight_instances = []
        for flight_instance in AirportSystem.__flight_instance_list:
            flight_instances.append(flight_instance.convert_to_json())
        return flight_instances
    
    def check_flight_instance(froml, to, date_depart, date_return = None):
        flight_list = []

        for flight_instance in AirportSystem.__flight_instance_list:
            if flight_instance.froml.name.upper() == froml.upper() and flight_instance.to.name.upper() == to.upper() and flight_instance.date == date_depart:
                flight_list.append(flight_instance)

        if date_return != None:
            for flight_instance in AirportSystem.__flight_instance_list:
                if flight_instance.froml.name.upper() == to.upper() and flight_instance.to.name.upper() == froml.upper() and flight_instance.date == date_return:
                    flight_list.append(flight_instance)

        return flight_list
    
    def get_detail_of_flight(flight_instance_list):
            all_detail = []
            
            for flight_instance in flight_instance_list:
                  sub_detail = {"from":flight_instance.froml.name , "to":flight_instance.to.name,
                                "flight_instance_number":flight_instance.flight_number, "time_departure":flight_instance.time_departure,
                                "time_arrival":flight_instance.time_arrival,"aircraft":flight_instance.aircraft.aircraft_number,
                                "depart":flight_instance.date}
                  all_detail.append(sub_detail)
        
            return all_detail  
    
    def choose_flight_instance(flight_instance_list, depart_time, arrive_time):
        for flight_instance in flight_instance_list:
            if flight_instance.time_departure == depart_time and flight_instance.time_arrival == arrive_time:
                return flight_instance
    
    def create_passenger(title, first_name, middle_name, last_name, birthday, phone_number, email):
        
        return Passenger(title, first_name, middle_name, last_name, birthday, phone_number, email)
    
    def check_flight_seat(flight_seat):
        flight_seats = []
        for seat in flight_seat:
            flight_seats.append(seat.convert_to_json())        
        return flight_seats

    def choose_flight_seat(passenger, flight_instance, seat_number):
        # for p_flight_seat in passenger.seat:
        #     for f_flight_seat in AirportSystem.
        #     if flight_seat.seat_number ==

        for flight_seat in flight_instance.flight_seats:
            if seat_number == flight_seat.seat_number:
                old_seat = flight_instance.get_flight_seat_from_seat_num()
                old_seat.occupied = False
                passenger.seat = flight_seat
                flight_seat.occcupied = True
        return passenger
    
    def show_reservation(booking_reference) :
        reservation = AirportSystem.find_reservation(booking_reference)
        reservation_detail = {"booking_reference": reservation.booking_reference,
                              "passengers": []
                             }
        
        for passenger in reservation.passengers:
            passenger_detail = {
                "title": passenger.title,
                "name": passenger.name,
                "birthday": passenger.birthday,
                "phone_number": passenger.phone_number,
                "email": passenger.email,
                "seat": passenger.seat[0].seat_number if passenger.seat else None,
                "extra_service": [
                    {
                        "service_name": service.__class__.__name__,
                        "weight" : service.bag_weight if hasattr(service, "weight") else None,
                        "price" : service.price if hasattr(service, "price") else None,
                        "status" : service.insurance_status if hasattr(service, "have_or_not") else None
                    }

                    for service in passenger.extra_service
                ]
            }

            reservation_detail["passengers"].append(passenger_detail)
            
        reservation_detail["total_cost"] = reservation.calculate_total_cost()
        reservation_detail["status"] = reservation.status

        return reservation_detail
            
    def admin_list():
        admins = []
        for admin in AirportSystem.__admin_list:
            admins.append(admin.convert_to_json())
        return admins
        
    def create_admin(title, first_name, middle_name, last_name, birth_date, phone_number, email):
        new_admin = Admin(title, first_name, middle_name, last_name, birth_date, phone_number, email)
        AirportSystem.__admin_list.append(new_admin)
        return new_admin

    def check_admin(name):
        for admin in AirportSystem.__admin_list:
            if admin.name == name:
                return admin
            
    def flight_list():
        flights = []
        for flight in AirportSystem.__flight_list:
            flights.append(flight.convert_to_json())
        return AirportSystem.__flight_list

    def create_flight_instance(name , flight_number , aircraft_number , time_departure , time_arrival , date , cost):
        admin = AirportSystem.check_admin(name)
        flight = AirportSystem.check_flight_from_flight_number(flight_number)
        if admin and flight:
            aircraft = AirportSystem.check_aircraft_from_aircraft_number(aircraft_number)
            flight_instance = FlightInstance(flight.froml, flight.to, flight.flight_number, time_departure, time_arrival, aircraft, date, cost)
            AirportSystem.__flight_instance_list.append(flight_instance)
            return flight_instance.convert_to_json() #return for checking in swagger
        return "Not an admin, cannot create flight instance."

    def create_flight(flight):
        AirportSystem.__flight_list.append(flight)
        return flight

    def aircraft_list():
        aircrafts = []
        for aircraft in AirportSystem.__aircraft_list:
            aircrafts.append(aircraft.convert_to_json())
        return 
    
    def seat_data():
        seats_data = []
        for c in range(1,10):
            for r in range(0,6):
                alphabets = "ABCDEF"
                seat_id = f"{alphabets[r]}{c}"
                seat_category = Category("normal_seat",0)
                if r <= 2:
                    seat_category = Category("premium_seat",500)
                if r <= 4:
                    seat_category = Category("happy_seat",200)
                seats_data.append(Seats(seat_id, seat_category))
        return seats_data
    
    def create_aircraft(*aircraft_numbers):
        for aircraft_number in aircraft_numbers:
            aircraft = Aircraft(AirportSystem.seat_data(), aircraft_number)
            AirportSystem.__aircraft_list.append(aircraft)
        return aircraft

    def check_flight_from_flight_number(flight_number):
        for flight in AirportSystem.__flight_list:
            if flight.flight_number == flight_number:
                return flight
            
    def check_aircraft_from_aircraft_number(aircraft_number):
        for aircraft in AirportSystem.__aircraft_list:
            if aircraft.aircraft_number == aircraft_number:
                return aircraft
            
class Reservation:
    def __init__(self, booking_reference):
        self.__flight_instances = []
        self.__passengers = []
        self.__booking_reference = booking_reference
        self.__total_cost = 0
        self.__boarding_pass = []
        self.__status = "Waiting.."

    def calculate_total_cost(self):
        self.__total_cost = 0
        for flight_instance in range(len(self.flight_instances)):
            self.__total_cost += self.flight_instances[flight_instance].cost * len(self.passengers)

        for passenger in range(len(self.passengers)):
            for seat in range(len(self.passengers[passenger].seat)) :
                self.__total_cost += self.passengers[passenger].seat[seat].seat_category.seat_price
                
            for service in range(len(self.passengers[passenger].extra_service)):
                self.__total_cost += self.passengers[passenger].extra_service[service].price  
        
        return self.__total_cost

    @property 
    def total_cost(self) :
        return self.__total_cost
    
    @total_cost.setter
    def total_cost(self, cost) :
        self.__total_cost = cost
    
    @property
    def status(self) :
        return self.__status
    
    @status.setter
    def status(self, status) :
        self.__status = status

    @property
    def booking_reference(self):
        return self.__booking_reference

    @property
    def passengers(self):
        return self.__passengers
    
    @passengers.setter
    def passengers(self, passenger):
        self.__passengers.append(passenger)
    
    @property
    def boarding_pass(self):
        return self.__boarding_pass

    @boarding_pass.setter
    def boarding_pass(self, boarding_pass):
        self.__boarding_pass.append(boarding_pass)

    @property
    def flight_instances(self):
        return self.__flight_instances
    
    @flight_instances.setter
    def flight_instances(self, flight):
        self.__flight_instances.append(flight)

    def convert_to_json(self):
        flight_instances = []
        for flight_instance in self.__flight_instances:
            flight_instances.append(flight_instance.convert_to_json())
        return {"flight_instance" : flight_instances,
                "passenger" : self.__passengers,
                "booking_reference" : self.__booking_reference,
                "total_cost" : self.__total_cost,
                "boarding_pass" : self.__boarding_pass}


class User:
    def __init__(self, title, first_name, middle_name, last_name, birthday, phone_number, email):
        self.__title = title
        self.__first_name = first_name
        self.__middle_name = middle_name
        self.__last_name = last_name
        self.__birthday = birthday
        self.__phone_number = phone_number
        self.__email = email

    @property
    def phone_number(self) :
        return self.__phone_number
    
    @property
    def email(self) :
        return self.__email

    @property
    def birthday(self) :
        return self.__birthday
        
    @property
    def first_name(self):
        return self.__first_name
    
    @property
    def middle_name(self):
        return self.__middle_name

    @property
    def last_name(self):
        return self.__last_name
    
    @property
    def title(self):
        return self.__title
    
    @property
    def name(self):
        if self.__middle_name:
            return self.__first_name + " " + self.__middle_name + " " + self.__last_name
        return self.__first_name + " " + self.__last_name

    def convert_to_json(self):
        return {"title" : self.__title,
                "name" : self.name,
                "birthday" : self.__birthday,
                "phone_number" : self.__phone_number,
                "email" : self.__email}

class Passenger(User):
    def __init__(self, title, first_name, middle_name, last_name, birthday, phone_number, email):
        super().__init__(title, first_name, middle_name, last_name, birthday, phone_number, email)
        self.__seat = []
        self.__extra_service = []
        
    @property
    def seat(self):
        return self.__seat
    
    @seat.setter
    def seat(self, seat):
        self.__seat.append(seat)

    @property
    def extra_service(self):
        return self.__extra_service

    @extra_service.setter
    def extra_service(self, service):
        self.__extra_service.append(service)

    def add_extra_service(self, MoreBaggage_kilo, Insurance_):
        if MoreBaggage_kilo != None :
            self.extra_service = MoreBaggage(int(MoreBaggage_kilo)*300, MoreBaggage_kilo)
        if Insurance_ != None :
            self.extra_service = Insurance(1500, Insurance_)

    def convert_to_json(self):
        return {"title" : self.title,
                "name" : self.name,
                "birthday" : self.birthday,
                "phone_number" : self.phone_number,
                "email" : self.email,
                "seat" : self.__seat,
                "extra_service" : self.__extra_service}

class Admin(User):
    pass
    
class BoardingPass:
    def __init__(self, reservation, passenger, returnl = 0):
        self.__flight_seat_number = passenger.seat[returnl]
        self.__flight_number = reservation.flight_instances[returnl]
        self.__passenger_title = passenger.title
        self.__passenger_name = passenger.name
        self.__aircraft_number = reservation.flight_instances[returnl].aircraft.aircraft_number
        self.__booking_reference = reservation.booking_reference
        self.__departure_date = reservation.flight_instances[returnl].date
        self.__boarding_time = reservation.flight_instances[returnl].boarding_time
        self.__from = reservation.flight_instances[returnl].froml
        self.__to = reservation.flight_instances[returnl].to

    def convert_to_json(self):
        return {"flight_seat_number" : self.__flight_seat_number.seat_number ,
                "flight_number" : self.__flight_number.flight_number,
                "title" : self.__passenger_title,
                "name" : self.__passenger_name,
                "aircraft_number" : self.__aircraft_number,
                "booking_reference" : self.__booking_reference,
                "departure_time" : self.__departure_date,
                "boarding_time" : self.__boarding_time,
                "from" : self.__from,
                "to" : self.__to}

class Flight:
    def __init__(self, froml, to, flight_number):
        self.__from = froml
        self.__to = to
        self.__flight_number = flight_number

    @property
    def flight_number(self):
        return self.__flight_number  
      
    @property
    def froml(self):
        return self.__from
    
    @property
    def to(self):
        return self.__to

    def convert_to_json(self):
        return {"from" : self.__from,
                "to" : self.__to, 
                "flight_number" : self.__flight_number}

class FlightInstance(Flight):
    def __init__(self, froml, to, flight_number, time_departure, time_arrival, aircraft, date, cost):
        super().__init__(froml, to, flight_number)
        self.__flight_seats = []
        for seat in aircraft.seats:
            self.__flight_seats.append(SeatFlight(seat))
        self.__time_departure = time_departure
        self.__time_arrival = time_arrival
        self.__aircraft = aircraft
        self.__date = date
        self.__cost = int(cost)

    @property
    def date(self):
        return self.__date
    
    @property
    def boarding_time(self):
        return self.__time_departure + " - " + self.__time_arrival
    
    @property
    def aircraft(self):
        return self.__aircraft
    
    @property
    def time_departure(self):
        return self.__time_departure
    
    @property
    def time_arrival(self):
        return self.__time_arrival
    
    @property
    def flight_seats(self):
        return self.__flight_seats
    
    @property
    def cost(self):
        return self.__cost

    def convert_to_json(self):
        return {"from" : self.froml,
                "to" : self.to, 
                "flight_number" : self.flight_number,
                "time_daparture" : self.__time_departure,
                "time_arrival" : self.__time_arrival,
                "date" : self.__date,
                "aircraft_number" : self.__aircraft.aircraft_number,
                "cost" : self.__cost}

    def get_flight_seat_from_seat_num(self, seat_num):
        for flight_seat in self.__flight_seats:
            if flight_seat.seat_number == seat_num:
                return flight_seat
    
class Aircraft:
    def __init__(self, seats, aircraft_number):
        self.__seats = seats
        self.__aircraft_number = aircraft_number

    @property
    def aircraft_number(self):
        return self.__aircraft_number
    
    @property
    def seats(self):
        return self.__seats

    def convert_to_json(self):
        return {"seats" : self.__seats ,
                "aircraft_number" : self.__aircraft_number}

class Airport:
    def __init__(self, name, short_name):
            self.__name = name
            self.__short_name = short_name
    @property
    def name(self):
            return self.__name
    
class Seats:
    def __init__(self, seat_number, seat_category):
        self.__seat_number = seat_number
        self.__seat_category = seat_category

    @property
    def seat_number(self):
        return self.__seat_number
    
    @property
    def seat_category(self):
        return self.__seat_category


class SeatFlight(Seats):
    def __init__(self, seat, occupied = False):
        super().__init__(seat.seat_number, seat.seat_category)
        self.__occupied = occupied
    
    @property
    def occupied(self):
        return self.__occupied
    
    @occupied.setter
    def occupied(self, occupied):
        self.__occupied = occupied
        return "Success"

    def convert_to_json(self):
        return {"seat_number" : self.seat_number,
                "seat_category" : self.seat_category,
                "seat_occupied" : self.__occupied}

class Category:
    def __init__(self, name, price):
        self.__name = name
        self.__price = int(price)

    @property
    def seat_price(self) :
        return self.__price
    
class Payment:
    def __init__(self, paid_time):
        self.__paid_time = paid_time

class CreditCard(Payment):
    payment_fee = 240
    def __init__(self, paid_time, card_number, cardholder_name, expiry_date, cvv):
        super().__init__(paid_time)
        self.__card_number = card_number
        self.__cardholder_name = cardholder_name
        self.__expiry_date = expiry_date
        self.__cvv = cvv
        self.__total_amount = 0

    def pay(self, reservation) :
        self.__total_amount += (reservation.total_cost + CreditCard.payment_fee)
        reservation.calculate_total_cost()
        reservation.total_cost += self.__total_amount
        if reservation.total_cost <= 0 :
            return "Invalid Cost"
        reservation.status = "Paid"
        return reservation.status

class Qr(Payment):
    payment_fee = 0
    def __init__(self, paid_time):
       super().__init__(paid_time)
       self.__total_amount = 0
    
    def pay(self, reservation) :
        self.__total_amount += (reservation.total_cost + Qr.payment_fee)
        reservation.calculate_total_cost()
        reservation.total_cost += self.__total_amount
        if reservation.total_cost <= 0 :
            return "Invalid Cost"
        reservation.status = "Paid"
        return reservation.status

class Service:
    def __init__(self, price):
        self.__price = int(price)

    @property
    def price(self) :
        return self.__price

class Insurance(Service):
    def __init__(self, price, have_or_not):
        super().__init__(price)
        self.__status = have_or_not

    @property
    def insurance_status(self) :
        return self.__status
    
class MoreBaggage(Service):
    
    def __init__(self, price, weight):
        super().__init__(price)
        self.__weight = weight

    @property
    def bag_weight(self) :
        return self.__weight

normal_seat = Category("normal_seat",0)
happy_seat = Category("happy_seat",200)
premium_seat = Category("happy_seat",500)

seats_data = []
for c in range(1,10):
    for r in range(0,6):
        alphabets = "ABCDEF"
        seat_id = f"{alphabets[r]}{c}"
        seat_category = normal_seat
        if r <= 2:
            seat_category = premium_seat
        if r <= 4:
            seat_category = happy_seat
        seats_data.append(Seats(seat_id, seat_category))


AirportSystem.create_airport(Airport("Don Mueang", "[BKK]"))
AirportSystem.create_airport(Airport("Chiang Mai", "[CNX]"))
AirportSystem.create_airport(Airport("Phuket", "[BKK]"))

AirportSystem.create_flight(Flight(AirportSystem.get_airport_list()[0], AirportSystem.get_airport_list()[1], "DD 712"))
AirportSystem.create_flight(Flight(AirportSystem.get_airport_list()[1], AirportSystem.get_airport_list()[0], "DD 721"))

AirportSystem.create_flight(Flight(AirportSystem.get_airport_list()[0], AirportSystem.get_airport_list()[2], "DD 813"))
AirportSystem.create_flight(Flight(AirportSystem.get_airport_list()[2], AirportSystem.get_airport_list()[0], "DD 831"))

AirportSystem.create_flight(Flight(AirportSystem.get_airport_list()[1], AirportSystem.get_airport_list()[2], "DD 823"))
AirportSystem.create_flight(Flight(AirportSystem.get_airport_list()[2], AirportSystem.get_airport_list()[1], "DD 832"))

AirportSystem.create_aircraft("B737-1", "B737-2", "B737-2")

app = FastAPI()

@app.get("/")
def normal():
    html_content = """
    <html>
<head>
<style>
.myButton {
	box-shadow: 1px 7px 24px -7px #276873;
	background:linear-gradient(to bottom, #599bb3 5%, #408c99 100%);
	background-color:#599bb3;
	border-radius:21px;
	display:inline-block;
	cursor:pointer;
	color:#ffffff;
	font-family:Arial;
	font-size:23px;
	font-weight:bold;
	padding:19px 43px;
	text-decoration:none;
	text-shadow:0px 0px 0px #3d768a;
}
.myButton:hover {
	background:linear-gradient(to bottom, #408c99 5%, #599bb3 100%);
	background-color:#408c99;
}
.myButton:active {
	position:relative;
	top:1px;
}
</style>
</head>
<body>
<center><a href="/docs" class="myButton">GO TO DOCS</a></center>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.get("/all_admin", tags=["admin"])
def all_admin():
    return AirportSystem.admin_list()

@app.post("/create_admin", tags=["admin"])
def create_admin(title : str, first_name : str, last_name : str, birth_date : str, phone_number : str, email : str, middle_name : Optional[str] = None):
    return AirportSystem.create_admin(title, first_name, middle_name, last_name, birth_date, phone_number, email).convert_to_json()

@app.get("/all_flight", tags=["flight"])
def all_flight():
    return AirportSystem.flight_list()

@app.get("/all_aircraft", tags=["aircraft"])
def all_aircraft():
    return AirportSystem.aircraft_list()

@app.post("/create_flight_instance", tags=["flight"])
def create_flight_instance(name : str, flight_number : str, aircraft_number : str, time_departure : str, time_arrival : str, date : str, cost : float):
    return AirportSystem.create_flight_instance(name, flight_number, aircraft_number, time_departure, time_arrival, date, cost)


@app.get("/all_reservation", tags=["reservation"])
def all_reservation():
    return AirportSystem.reservation_list()

@app.post("/reservation", tags=["reservation"])
def new_reservation(booking_reference : str):
    return AirportSystem.create_reservation(Reservation(booking_reference))

@app.get("/all_flight_instance", tags=["flight"])
def all_flight_instance():
    return AirportSystem.flight_instance_list()

@app.get("/see_flight_instance", tags=["flight"])
def see_flight_instance(froml : str, to : str, date_depart : str, return_depart : Optional[str] = None):
    return AirportSystem.get_detail_of_flight(AirportSystem.check_flight_instance(froml, to, date_depart, return_depart))

@app.post("/select_flight_instance", tags=["flight"])
def select_flight_instance(booking_reference : str, froml : str, to : str, date : str, depart_time : str, arrive_time : str, return_date : Optional[str] = None, return_depart_time : Optional[str] = None, return_arrive_time : Optional[str] = None):
    # depart_flight_instance = AirportSystem.check_flight_instance(froml, to, date)
    # reservation = AirportSystem.find_reservation(booking_reference)

    # if depart_flight_instance and reservation:
    #     reservation.flight_instances = AirportSystem.choose_flight_instance(depart_flight_instance, depart_time, arrive_time)

    #     if return_date:
    #         return_flight_instance = AirportSystem.check_flight_instance(to, froml, return_date)
    #         reservation.flight_instances = AirportSystem.choose_flight_instance(return_flight_instance, return_depart_time, return_arrive_time)
    
    # return reservation
    if AirportSystem.check_flight_instance(froml, to, date) and AirportSystem.find_reservation(booking_reference):
        AirportSystem.find_reservation(booking_reference).flight_instances = AirportSystem.choose_flight_instance(AirportSystem.check_flight_instance(froml, to, date), depart_time, arrive_time)

        if return_date:
            return_flight_instance = AirportSystem.check_flight_instance(to, froml, return_date)
            AirportSystem.find_reservation(booking_reference).flight_instances = AirportSystem.choose_flight_instance(return_flight_instance, return_depart_time, return_arrive_time)
    
    return AirportSystem.find_reservation(booking_reference).convert_to_json()

@app.post("/passenger")
def new_passenger(booking_reference : str, title : str, first_name : str, last_name : str, birthday : str, phone_number : str, email : str, middle_name : Optional[str] = None):
    AirportSystem.find_reservation(booking_reference).passengers = AirportSystem.create_passenger(title, first_name, middle_name, last_name, birthday, phone_number, email)
    return AirportSystem.find_reservation(booking_reference).convert_to_json()

@app.get("/see_seat" , tags=["seat"])
def see_seat(froml : str, to : str, date : str, depart_time : str, arrive_time : str):
    return AirportSystem.check_flight_seat(AirportSystem.choose_flight_instance(AirportSystem.check_flight_instance(froml, to, date) , depart_time, arrive_time).flight_seats)

@app.post("/select_seat", tags=["seat"])
def select_seat(booking_reference : str, name : str, seat : str, return_seat : Optional[str] = None):
    # passenger = AirportSystem.check_passenger(booking_reference, name)
    # reservation = AirportSystem.find_reservation(booking_reference)
    # depart_flight_instance = reservation.flight_instances[0]

    # AirportSystem.choose_flight_seat(passenger, depart_flight_instance, seat)
    # if return_seat != None:
    #     return_flight_instance = reservation.flight_instances[1]
    #     AirportSystem.choose_flight_seat(passenger, return_flight_instance, return_seat)
    # return passenger
    AirportSystem.choose_flight_seat(AirportSystem.check_passenger(booking_reference, name), AirportSystem.find_reservation(booking_reference).flight_instances[0], seat)
    if return_seat != None:
        AirportSystem.choose_flight_seat(AirportSystem.check_passenger(booking_reference, name), AirportSystem.find_reservation(booking_reference).flight_instances[1], return_seat)
    return AirportSystem.check_passenger(booking_reference, name).convert_to_json()

@app.post("/payment_credit", tags=["payment"])
def pay_by_credit(booking_referrence: str, card_number: str, cardholder_name: str, expiry_date: str, cvv: str, paid_time: str):
    return CreditCard(paid_time, card_number, cardholder_name, expiry_date, cvv).pay(AirportSystem.find_reservation(booking_referrence))

@app.post("/pay_qr", tags=["payment"])
def pay_by_qr(booking_referrence: str, paid_time: str) :
    return Qr(paid_time).pay(AirportSystem.find_reservation(booking_referrence))

@app.get("/boarding_pass")
def board_pass(booking_reference : str, name : str, returnl : Optional[bool] = False):
    return AirportSystem.check_in(booking_reference, name, returnl).convert_to_json()
    
@app.get("/see_reservation" , tags=["reservation"])
def show_reservation(booking_reference : str) :
    return AirportSystem.show_reservation(booking_reference)

@app.post("/service")
def service (booking_reference: str, name : str,  MoreBaggage_kilo : Optional[int] = None, Insurance_ : Optional[str] = None):
    AirportSystem.check_passenger(booking_reference, name).add_extra_service(MoreBaggage_kilo,Insurance_)
    return AirportSystem.check_passenger(booking_reference, name).extra_service

if __name__ == "__main__":
    uvicorn.run("AirportSystem:app", host="127.0.0.1", port=8000, log_level="info")


