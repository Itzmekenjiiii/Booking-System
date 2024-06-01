#================================================================================================================================================================================================================================

# GRAB BOOKING SYSTEM
# - grab booking system is used by customers to book some riders to deliver their things from pick-up location, to drop-off location.
# - it's also use to book a rider to pick-up a customers and drop-off to drop-off location.

#OBJECTIVES:
#To show how Grab Booking System Works.

# INFORMATION NEEDED:
# pick up location
# drop off location
# customer or passenger name
# driver name  
# status (pending)


# CHOICES:
# edit booking
# delete booking
# save to json
# load to json
# add booking
# assign a driver

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 

import json
from datetime import datetime

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# MAIN CLASS:
class Ride:
    def __init__(self, pickup_location, dropoff_location, passenger_name, driver_name=None, status="Pending"):
        
        #PICK UP AND DROP OFF LOCATION:
        self.pickup_location = pickup_location
        self.dropoff_location = dropoff_location
        
        #CUSTOMER AND DRIVER INFO:
        self.passenger_name = passenger_name
        self.driver_name = driver_name
        
        #STATUS (SHOW IF "PENDING")
        self.status = status
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# SHOW \ DISPLAY:
    def to_dict(self):
        return {
            'pickup_location': self.pickup_location,
            'dropoff_location': self.dropoff_location,
            'passenger_name': self.passenger_name,
            'driver_name': self.driver_name,
            'status': self.status
        }
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#CLASS FOR BOOKING:
class RideBookingSystem:
    def __init__(self, file_path):
        self.file_path = file_path
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#ADD OR BOOK A RIDE:
    def book_ride(self, ride):
        self.rides = self.load_rides()
        self.rides.append(ride.to_dict())
        #REMINDER:
        self.save_rides(self.rides) #ALWAYS SAVE THE DATA (pagkainput ng data naka automatic save na sa JSON FILES.)
        print("Ride booked successfully!")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#GET A DRIVER TO THE PENDING BOOKS:
    def get_pending_rides(self):
        rides = self.load_rides() #ALWAYS SAVE THE DATA (pwede din nmn tanggalin para naka manual save ka.)
        return [Ride(**ride) for ride in rides if ride['status'] == 'Pending']
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#ASSIGN A DRIVER:
#(contains drop off and pick up location)
    def assign_driver(self, ride, driver_name):
        rides = self.load_rides()
        for r in rides:
            if r['pickup_location'] == ride.pickup_location and r['dropoff_location'] == ride.dropoff_location:
                r['driver_name'] = driver_name
                r['status'] = 'Assigned'
                break
        self.save_rides(rides) #ALWAYS SAVE THE DATA (kung tatanggalin, wag mo lang kakalimutan mag manual save para hindi mawala yung data mo.)
        print(f"Driver assigned to ride from {ride.pickup_location} to {ride.dropoff_location}")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#EDIT THE BOOKING:
#(choose the booking you want to edit)
#can change the drop off and pick up location if it is still pending.
    def edit_ride(self, ride, new_pickup_location, new_dropoff_location):
        rides = self.load_rides()
        for r in rides:
            if r['pickup_location'] == ride.pickup_location and r['dropoff_location'] == ride.dropoff_location:
                r['pickup_location'] = new_pickup_location
                r['dropoff_location'] = new_dropoff_location
                break           
        self.save_rides(rides) #ALWAYS SAVE THE DATA (PARA HINDI MAWALA!)
        print("Ride booking edited successfully!")           
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------      
#DELETE A PENDING BOOKING:
#can use to cancel the booking as long as it is pending and no drivers assigned.
    def delete_ride(self, ride):
        rides = self.load_rides()
        rides = [r for r in rides if not (r['pickup_location'] == ride.pickup_location and r['dropoff_location'] == ride.dropoff_location)]
        self.save_rides(rides) #ALWAYS SAVE THE DATA (PARA HINDI MAWALA!)
        print("Ride booking deleted successfully!")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#LOAD TO JSON FILES:
#if your data is saved in json file before you exit the program, you will see your pending data if you press load in the next.
    def load_rides(self):
        try:
            with open(self.file_path, 'r') as file:
                rides_data = json.load(file)
                if isinstance(rides_data, list):  # Check if the loaded data is a list
                    rides = rides_data
                elif isinstance(rides_data, dict) and 'grab' in rides_data:
                    rides = rides_data['grab']
                else:
                    print("Invalid rides data format.")
                    return []

                if rides:
                    for index, ride in enumerate(rides, start=1):
                        print("-----------------")
                        print(f"|| BOOKING {index}:  ||")
                        print("-----------------")
                        print("===============================")
                        print()
                        print(f"   Pickup Location: {ride['pickup_location']}")
                        print(f"   Dropoff Location: {ride['dropoff_location']}")
                        print(f"   Passenger Name: {ride['passenger_name']}")
                        print(f"   Driver Name: {ride['driver_name']}")
                        print(f"   Status: {ride['status']}")
                        print()
                        print("================================")
                        print("\n")
                    return rides
                else:
                    print("No booking found. Please try another booking.")
                    return []
        except FileNotFoundError:
            print("Booking file not found. Creating a new file.")
            return []
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return []    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------       
#SAVE TO JSON FILES:
#use to save files\ booking data.
#although auto save na lahat ng data na iinput mo(you can use this manually to make sure.)
    def save_rides(self, rides):
        try:
            with open(self.file_path, 'w') as file:
                json.dump(rides, file, indent=4)
            print("Rides saved to JSON file.")
        except Exception as e:
            print("Error saving rides to JSON file:", e)       
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------          
#MENU
#contains choices like, book a ride, assign, edit, delete, load, save, and exit.
    def menu(self):
        while True:
            print("=====================================================")
            print("|| Welcome to Kenji Text_Based Grab Booking System ||")
            print("=====================================================")
            print("\n")
            print("How may i help you?")
            print("\n")
            print("-----------------------------------------")
            print("1. Book a ride")
            print("2. Assign a driver to a pending ride")
            print("3. Edit a ride")
            print("4. Delete a ride")
            print("5. Display pending rides")
            print("6. Save rides to JSON file")
            print("7. Load rides from JSON file")
            print("8. Exit")
            print("-----------------------------------------")
            print("\n")          
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            choice = input("Enter your choice: ")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            if choice == '1':
                pickup_location = input("Enter pickup location: ")
                dropoff_location = input("Enter dropoff location: ")
                passenger_name = input("Enter passenger name: ")
                new_ride = Ride(pickup_location, dropoff_location, passenger_name)
                self.book_ride(new_ride)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            elif choice == '2':
                pending_rides = self.get_pending_rides()
                if pending_rides:
                    for i, ride in enumerate(pending_rides, start=1):
                        print(f"{i}. Passenger: {ride.passenger_name}, Pickup: {ride.pickup_location}, Dropoff: {ride.dropoff_location}")
                    ride_index = int(input("Select a ride to assign a driver (enter the index): ")) - 1
                    if 0 <= ride_index < len(pending_rides):
                        driver_name = input("Enter driver name: ")
                        self.assign_driver(pending_rides[ride_index], driver_name)
                    else:
                        print("Invalid ride index.")
                else:
                    print("No pending book rides.")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            elif choice == '3':
                pending_rides = self.get_pending_rides()
                if pending_rides:
                    for i, ride in enumerate(pending_rides, start=1):
                        print(f"{i}. Passenger: {ride.passenger_name}, Pickup: {ride.pickup_location}, Dropoff: {ride.dropoff_location}")
                    ride_index = int(input("Select a ride to edit (enter the index): ")) - 1
                    if 0 <= ride_index < len(pending_rides):
                        new_pickup_location = input("Enter new pickup location: ")
                        new_dropoff_location = input("Enter new dropoff location: ")
                        self.edit_ride(pending_rides[ride_index], new_pickup_location, new_dropoff_location)
                    else:
                        print("Invalid ride index.")
                else:
                    print("No pending book rides.")    
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            elif choice == '4':
                pending_rides = self.get_pending_rides()
                if pending_rides:
                    for i, ride in enumerate(pending_rides, start=1):
                        print(f"{i}. Passenger: {ride.passenger_name}, Pickup: {ride.pickup_location}, Dropoff: {ride.dropoff_location}")
                    ride_index = int(input("Select a ride to delete (enter the index): ")) - 1
                    if 0 <= ride_index < len(pending_rides):
                        self.delete_ride(pending_rides[ride_index])
                    else:
                        print("Invalid ride index.")
                else:
                    print("No pending book rides.")
 #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                   
            elif choice == '5':
                pending_rides = self.get_pending_rides()
                if pending_rides:
                    print("Pending book rides:")
                    for ride in pending_rides:
                        print(f"Passenger: {ride.passenger_name}, Pickup: {ride.pickup_location}, Dropoff: {ride.dropoff_location}")
                else:
                    print("No pending book rides.")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                   
            elif choice == '6':
                self.save_rides(self.load_rides())
                print("Booking saved to JSON file.")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                
            elif choice == '7':
                self.load_rides()
                print("Booking loaded from JSON file.")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                
            elif choice == '8':
                print("Exiting...")
                print("THANK YOU...")
                break
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------           
            else:
                print("Invalid choice. Please try again.")
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                

if __name__=="__main__":
    grab = RideBookingSystem("rides.json")
    grab.menu()