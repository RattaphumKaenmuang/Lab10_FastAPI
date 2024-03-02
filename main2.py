
from starlette.responses import HTMLResponse
from typing import Union , Optional
import uvicorn
from fastapi import FastAPI

class AirportSystem:
    __admin_list = []
    __reservation_list = []	
    __flight_list = []
    __flight_instance_list = []
    __service_list = []
    __aircraft_list = []
    __payment_method_list = []
    __airport_list = []

    def add_payment_method(payment_method) :
        AirportSystem.__payment_method_list.append(payment_method)

    def get_payment_method() :
        return Airport.__payment_method_list

    def get_reservation_list():
        return AirportSystem.__reservation_list

    def check_in(booking_reference, lastname):
        a = []
        for i in range(len(AirportSystem.get_passenger_from_name(booking_reference, lastname).seat)):
            a.append(AirportSystem.create_boarding_pass(AirportSystem.search_reservation_from_reference(booking_reference), AirportSystem.get_passenger_from_name(booking_reference, lastname), i))
        return a
    
    def add_airport(airport):
        return AirportSystem.__airport_list.append(airport)

    def create_reservation(booking_reference):
        reservation = Reservation(booking_reference)
        if reservation not in AirportSystem.__reservation_list:
            AirportSystem.__reservation_list.append(reservation)
            return reservation
        return "Reservation already exists"
    
    def search_reservation_from_reference(booking_reference):
        for i in AirportSystem.__reservation_list:
            if i.booking_reference == booking_reference:
                return i
            
    def get_passenger_from_name(booking_reference, first_name, middle_name, last_name):
        for i in AirportSystem.search_reservation_from_reference(booking_reference).passengers:
            if i.first_name == first_name and i.middle_name == middle_name and i.last_name == last_name:
                return i

    def create_boarding_pass(reservation, passenger, returnl = 0):
        reservation.boarding_pass = BoardingPass(reservation, passenger, returnl)
        return BoardingPass(reservation, passenger, returnl) #return for checking in swagger
    
    def get_flight_instance_list():
        return AirportSystem.__flight_instance_list
    
    def check_flight_instance(froml, to, date_depart, date_return = None):
        flight_list = []
        
        for i in AirportSystem.__flight_instance_list:
            if i.froml.name.upper() == froml.upper() and i.to.name.upper() == to.upper() and i.date == date_depart:
                flight_list.append(i)
                
        if date_return != None:
            for i in AirportSystem.__flight_instance_list:
                if i.froml.name.upper() == to.upper() and i.to.name.upper() == froml.upper() and i.date == date_return:
                    flight_list.append(i)
        
        return flight_list
    
    def get_detail_of_flight(list_flight):
            all_detail = []
            for flight in list_flight:
                  sub_detail = {"from":flight.froml.name , "to":flight.to.name,
                                "flight_number":flight.flight_number, "time_departure":flight.time_departure,
                                "time_arrival":flight.time_arrival,"aircraft":flight.aircraft.aircraft_number,
                                "depart":flight.date}
                  all_detail.append(sub_detail)
            return all_detail  
    
    def choose_flight(flight, depart_time, arrive_time):
        for i in flight:
            if i.time_departure == depart_time and i.time_arrival == arrive_time:
                return i
    
    def create_passenger(title, first_name, middle_name, last_name, birth_date, phone_number, email):
        return Passenger(title, first_name, middle_name, last_name, birth_date, phone_number, email)
    
    def get_flight_seat_list(flight):
        return flight.flight_seats
    
    def choose_seat(passenger, flight, seat):
        for i in flight.flight_seats:
            if i.seat_number == seat:
                passenger.seat = i
                flight.remove_seat(seat)
        return passenger
    
    def show_reservation(booking_reference) :
        for reservation in AirportSystem.__reservation_list :
            if reservation.booking_reference == booking_reference :
                detail = {"booking_reference" : booking_reference, 
                        "name" : reservation.passengers[0].name, 
                        "from_location" : reservation.flight_instances[0].froml.name, 
                        "to" : reservation.flight_instances[0].to.name, 
                        "borading_time" : reservation.flight_instances[0].boarding_time, 
                        "flight" : reservation.flight_instances[0].flight_number, 
                        "aircraft" : reservation.flight_instances[0].aircraft.aircraft_number,
                        "extra_service" : reservation.extra_service,
                        "total_payment" : reservation.total_cost,
                        "status" : reservation.status}
                return detail
            else :
                return "Invalid Booking Reference"
            
    def find_reservation(booking_reference):
        for reservation in AirportSystem.__reservation_list :
            if reservation.booking_reference == booking_reference :
                return reservation
            
    def get_admin_list():
        return AirportSystem.__admin_list
        
    def create_admin(title, firstname, middlename, lastname, birthday, phone_number, email):
        new_admin = Admin(title, firstname, middlename, lastname, birthday, phone_number, email)
        AirportSystem.__admin_list.append(new_admin)
        return new_admin #return for checking in swagger

    def check_admin(lastname):
        for i in AirportSystem.__admin_list:
            if i.lastname == lastname:
                return i
            
    def flight_list():
        return AirportSystem.__flight_list

    def create_flight_instance(admin, flight_instance):
        for i in AirportSystem.__admin_list:
            if i == admin:
                AirportSystem.__flight_instance_list.append(flight_instance)
                return flight_instance #return for checking in swagger
        return "Not an admin, cannot create flight instance."

    def create_flight(flight):
        AirportSystem.__flight_list.append(flight)
        return flight #return for checking in swagger

    def aircraft_list():
        return AirportSystem.__aircraft_list

    def create_aircraft(aircraft):
        AirportSystem.__aircraft_list.append(aircraft)
        return aircraft #return for checking in swagger

    def get_flight_instance_from_flight_number(flight_number):
        for i in AirportSystem.__flight_list:
            if i.flight_number == flight_number:
                return i #return for checking in swagger
        return "Flight not found"
    
    def get_aircraft_from_aircraft_number(aircraft_number):
        for i in AirportSystem.__aircraft_list:
            if i.aircraft_number == aircraft_number:
                return i #return for checking in swagger
        return "Aircraft not found"

class Reservation:
    def __init__(self, booking_reference):
        self.__flight_instances = []
        self.__passengers = []
        self.__booking_reference = booking_reference
        self.__total_cost = 0
        self.__boarding_pass = []
        self.__status = "Waiting.."

    def total_cost(self) :
        # self.__total_cost += self.__flight_instances... 
        # flight_instance serivice seats 
        pass

    property 
    def total_cost(self) :
        return self.__total_cost
    
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


class User:
    def __init__(self, title, firstname, middlename, lastname, birthday, phone_number, email):
        self.__title = title
        self.__firstname = firstname
        self.__middlename = middlename
        self.__lastname = lastname
        self.__birthday = birthday
        self.__phone_number = phone_number
        self.__email = email
        
    @property
    def lastname(self):
        return self.__lastname
    
    @property
    def title(self):
        return self.__title
    
    @property
    def name(self):
        if self.__middlename:
            return self.__firstname + " " + self.__middlename + " " + self.__lastname
        return self.__firstname + " " + self.__lastname

class Passenger(User):
    def __init__(self, title, firstname, middlename, lastname, birthday, phone_number, email):
        super().init(title, firstname, middlename, lastname, birthday, phone_number, email)
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
    def extra_service(self, flight):
        self.__extra_service.append(flight)

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

class FlightInstance(Flight):
    def __init__(self, froml, to, flight_number, time_departure, time_arrival, aircraft, date, cost):
        super().__init__(froml, to, flight_number)
        self.__flight_seats = []
        for i in aircraft.seats:
            self.__flight_seats.append(SeatFlight(i.seat_number, i.seat_category))
        self.__time_departure = time_departure
        self.__time_arrival = time_arrival
        self.__aircraft = aircraft
        self.__date = date
        self.__cost = cost

    @property
    def date(self):
        return self.__date
    
    @property
    def boarding_time(self):
        return self.__time_arrival + " " + self.__time_departure
    
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
    
    def get_seat_from_number(self, seat_number):
        for i in self.flight_seats:
            if i.seat_number == seat_number:
                return i
    
    def remove_seat(self, seat_number):
        return self.__flight_seats.remove(self.get_seat_from_number(seat_number))
    
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

class Category:
    def __init__(self, name, price):
        self.__name = name
        self.__price = price

class SeatFlight(Seats):
    def __init__(self, seat, occupied):
        super().__init__(seat, occupied)

class Payment:
    def __init__(self, paid_time, amount):
        self.__paid_time = paid_time
        self.__amount = amount

class CreditCard(Payment):
    payment_fee = 240
    def __init__(self, paid_time, amount, card_number, cardholder_name, expiry_date, cvv):
        super().__init__(paid_time, amount)
        self.__amount += CreditCard.payment_fee
        self.__card_number = card_number
        self.__cardholder_name = cardholder_name
        self.__expiry_date = expiry_date
        self.__cvv = cvv
    
    @property
    def card_numebr(self) :
        return self.__card_number
    
    @property
    def amount(self) :
        return self.__amount

    # def pay return done
    def pay(reservation) :
        if reservation.total_cost <= 0 :
            return "Invalid Cost"
        reservation.status = "paid"
        return "Done"

class Qr(Payment):
   payment_fee = 0
   def __init__(self, paid_time, amount):
       super().__init__(paid_time, amount)

class Service:
    def __init__(self, price):
        self.__price = price

class Insurance(Service):
    def __init__(self, price, have_or_not):
        super().__init__(price)
        self.__status = have_or_not

class MoreBaggage(Service):
    
    def __init__(self, price, weight):
        super().__init__(price)
        self.__weight = weight


airport1 = Airport("Don Mueang", "[BKK]")
airport2 = Airport("Chiang Mai", "[CNX]")
airport3 = Airport("Hyderabad, India", "[HYD]")
airport4 = Airport("Phuket", "[BKK]")
airport5 = Airport("Chiang Mai", "[CNX]")
airport6 = Airport("Hyderabad, India", "[HYD]")

AirportSystem.create_flight(Flight(airport1, airport2, "ABC"))
AirportSystem.create_flight(Flight(airport2, airport1, "ACB"))
AirportSystem.create_aircraft(Aircraft([Seats("A1", Category("happy_seat",100)), Seats("A2", Category("premium seat",120))], "101"))


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

@app.get("/all_admin")
def all_admin():
    return AirportSystem.admin_list()

@app.post("/create_admin")
def create_admin(title : str, firstname : str, lastname : str, birthday : str, phone_number : str, email : str, middlename : Optional[str] = None):
    return AirportSystem.create_admin(title, firstname, middlename, lastname, birthday, phone_number, email)

@app.get("/all_flight")
def all_flight():
    return AirportSystem.flight_list()

@app.get("/all_aircraft")
def all_aircraft():
    return AirportSystem.aircraft_list()

@app.post("/create_flight_instance")
def create_flight_instance(lastname : str, flight_number : str, aircraft_number : str, time_departure : str, time_arrival : str, date : str, cost : float):
    flight = AirportSystem.get_flight_instance_from_flight_number(flight_number)
    return AirportSystem.create_flight_instance(AirportSystem.check_admin(lastname), FlightInstance(flight.froml, flight.to, flight.flight_number, time_departure, time_arrival, AirportSystem.get_aircraft_from_aircraft_number(aircraft_number), date, cost))


@app.get("/all_reservation")
def all_reservation():
    return AirportSystem.get_reservation_list()

@app.post("/reservation")
def new_reservation(booking_reference : str):
    return AirportSystem.create_reservation(booking_reference)

@app.get("/all_flight_instance")
def all_flight_instance():
    return AirportSystem.flight_instance_list()

@app.get("/see_flight_instance")
def see_flight_instance(froml : str, to : str, date_depart : str, return_depart : Optional[str] = None):
    flight = AirportSystem.check_flight_instance(froml, to, date_depart, return_depart)
    flight_detail = AirportSystem.get_detail_of_flight(flight)
    return flight_detail

@app.post("/select_flight_instance")
def select_flight_instance(booking_reference : str, froml : str, to : str, date : str, depart_time : str, arrive_time : str, return_date : Optional[str] = None, return_depart_time : Optional[str] = None, return_arrive_time : Optional[str] = None):
    AirportSystem.search_reservation_from_reference(booking_reference).flight_instances = AirportSystem.choose_flight(AirportSystem.check_flight_instance(froml, to, date) , depart_time, arrive_time)
    if return_date != None:
        AirportSystem.search_reservation_from_reference(booking_reference).flight_instances = AirportSystem.choose_flight(AirportSystem.check_flight_instance(to, froml, date) , return_depart_time, return_arrive_time)
    return AirportSystem.search_reservation_from_reference(booking_reference)

@app.post("/passenger")
def new_passenger(booking_reference : str, title : str, firstname : str, lastname : str, birthday : str, phone_number : str, email : str, middlename : Optional[str] = None):
    AirportSystem.search_reservation_from_reference(booking_reference).passengers = AirportSystem.create_passenger(title, firstname, middlename, lastname, birthday, phone_number, email)
    return AirportSystem.search_reservation_from_reference(booking_reference)

@app.get("/see_seat")
def see_seat(froml : str, to : str, date : str, depart_time : str, arrive_time : str):
    return AirportSystem.get_flight_seat_list(AirportSystem.choose_flight(AirportSystem.check_flight_instance(froml, to, date) , depart_time, arrive_time))

@app.put("/select_seat")
def select_seat(booking_reference : str, lastname : str, seat : str, return_seat : Optional[str] = None):
    AirportSystem.choose_seat(AirportSystem.get_passenger_from_name(booking_reference, lastname), AirportSystem.search_reservation_from_reference(booking_reference).flight_instances[0], seat)
    if return_seat != None:
        AirportSystem.choose_seat(AirportSystem.get_passenger_from_name(booking_reference, lastname), AirportSystem.search_reservation_from_reference(booking_reference).flight_instances[1], return_seat)
    return AirportSystem.get_passenger_from_name(booking_reference, lastname)

@app.get("/payment_credit")
def pay_by_credit(method: str, detail: dict) :
    if method == "credit" :
        card1 = CreditCard(detail["paid_time"], detail["amount"], detail["card_number"], detail["cardholder_name"], detail["expiry_date"], detail["cvv"])
        return card1.pay()

@app.get("/pay_qr")
def pay_by_qr(method: str, detail: dict) :
    if method == "qr" :
        qr1 = Qr(detail)
        return qr1.pay()

@app.get("/boarding_pass")
def board_pass(booking_reference : str, lastname : str):
    return AirportSystem.check_in(booking_reference, lastname)
    
@app.get("/see_reservation")
def show_reservation(booking_reference : str) :
    return AirportSystem.show_reservation(booking_reference)


@app.post("/service")
def service (booking_reference: str, MoreBaggage_kilo : Optional[int] = None, Insurance_ : Optional[str] = None):
    passenger = AirportSystem.get_passenger_from_name()
    if MoreBaggage_kilo != None :
        passenger.extra_service = MoreBaggage(int(MoreBaggage_kilo)*300,MoreBaggage_kilo)
    if Insurance_ != None :
        passenger.extra_service = Insurance(1500,Insurance_)
    return "Added service"

if __name__ == "__main__":
    uvicorn.run("AirportSystem:app", host="127.0.0.1", port=8000, log_level="info")