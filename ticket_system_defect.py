
from abc import ABC, abstractmethod

# the base Ticket class will be abstract, so I am using ABC to make it an abstract base class that can't be instantiated
# I am also importing abstractmethod for polymorphism to force subclasses to dictate their own implementation on a method

class Ticket(ABC):

    # setting valid values for priority and status
    VALID_PRIORITIES = ["Low", "Medium", "High", "Critical"]
    VALID_STATUSES = ["Open", "In Progress", "Resolved", "Closed"]

    def __init__(self, ticket_id, title, description):
        # if title is not a string or is empty, raise a ValueError
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Ticket title cannot be empty.")
        # same with description
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Ticket description cannot be empty.")

        # double underscore for private attributes (encapsulation)
        # default priority, status, and assigned technician values are set
        self.__ticket_id = ticket_id
        self.__title = title.strip()
        self.__description = description.strip()
        self.__priority = "Medium"
        self.__status = "Open"
        self.__assigned_technician = "Unassigned"

    # using property decorator here so I can refer to these methods without parentheses, more like an attribute instead of a method (just makes it easier)
    # the actual code shows double underscores to show private attributes, but the property decorator allows me to access them without the double underscores
    @property
    def ticket_id(self):
        return self.__ticket_id
    @property
    def title(self):
        return self.__title
    @property
    def description(self):
        return self.__description
    @property
    def priority(self):
        return self.__priority
    @property
    def status(self):
        return self.__status
    @property
    def assigned_technician(self):
        return self.__assigned_technician

    # this method returns the ticket ID; we will use this later
    def get_ticket_id(self):
        return self.__ticket_id

    # this method returns all ticket details
    # I've used new lines just so the output is more readable when printed
    def get_details(self):
        return (
            f"Ticket ID: {self.__ticket_id}\n"
            f"Title: {self.__title}\n"
            f"Description: {self.__description}\n"
            f"Priority: {self.__priority}\n"
            f"Status: {self.__status}\n"
            f"Assigned Technician: {self.__assigned_technician}"
        )

    # if the provided priority is not a valid priority as set above, raise a ValueError
    def validate_priority(self, priority):
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority. Choose from: {self.VALID_PRIORITIES}")
        return True

     # same as above but for status instead of priority
    def validate_status(self, status):
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status. Choose from: {self.VALID_STATUSES}")
        return True
    
    # if the user wants to update priority, validate the new priority before updating it
    def update_priority(self, priority):
        self.validate_priority(priority)
        self.__priority = priority
        
    # same as above but for status instead of priority
    def update_status(self, status):
        self.validate_status(status)
        self.__status = status

    # assigning a technician
    # if the technician name is not a string or is empty, raise a ValueError
    # I considered adding pre-determined names for technicians, but I wanted to keep it simple and allow any name to be assigned
    def assign_technician(self, technician):
        if not isinstance(technician, str) or not technician.strip():
            raise ValueError("Technician name cannot be empty.")
        self.__assigned_technician = technician.strip()

    # this is the abstract method to demonstrate the concept of polymorphism
    # subclasses must implement this method. Its behaviour will depend on the type of ticket
    # for the assignment, I have kept it simple with just two ticket types, a hardware ticket and a software ticket
    @abstractmethod
    def process_ticket(self):
        pass

# that concludes the Ticket class. Moving onto the subclasses now

# first subclass: Hardware Ticket

class HardwareTicket(Ticket):

    # initializing the Hardware Ticket with the same base attributes, but adding a device attribute
    def __init__(self, ticket_id, title, description, device):
        super().__init__(ticket_id, title, description)
        # if the device is not a string or is empty, raise a ValueError
        if not isinstance(device, str) or not device.strip():
            raise ValueError("Device cannot be empty.")
        # double underscore since device is private, and strip whitespace from the device name
        self.__device = device.strip()

    # property decorator for device for same reason as others before
    @property
    def device(self):
        return self.__device

    # for a Hardware Ticket, process ticket will return a basic string with instructions for the technician to follow
    def process_ticket(self):
        return (f"Hardware support required for {self.ticket_id}: "
                f"1) Inspect {self.__device}, "
                f"2) Check cables and power, "
                f"3) Run diagnostics, "
                f"4) Replace faulty components if necessary."
        )

    # here get details will return the base ticket information plus the ticket type and device name
    def get_details(self):
        return (super().get_details() + f"\nTicket Type: Hardware" + f"\nDevice: {self.__device}")


# now moving onto the Software Ticket subclass
# this will be almost identical to Hardware Ticket, but replacing device with application

# second subclass: Software Ticket

class SoftwareTicket(Ticket):

    # initialize Software Ticket with same base attributes, but adding an application attribute
    def __init__(self, ticket_id, title, description, application):
        super().__init__(ticket_id, title, description)
        # if the application is not a string or is empty, raise a ValueError
        if not isinstance(application, str) or not application.strip():
            raise ValueError("Application cannot be empty.")
        # double underscore since application is private, and strip whitespace from the application name
        self.__application = application.strip()

    # property decorator for application for same reason as others before
    @property
    def application(self):
        return self.__application

    # for a Software Ticket, process ticket will return a basic string with instructions for the technician to follow
    def process_ticket(self):
        return (f"Software support required for {self.ticket_id}: "
                f"1) Review logs for {self.__application}, "
                f"2) Check configuration, "
                f"3) Install updates, "
                f"4) Escalate unresolved issues to the development team."
        )

    # here get details will return the base ticket information plus the ticket type and application name
    def get_details(self):
        return (super().get_details() + f"\nTicket Type: Software" + f"\nApplication: {self.__application}")


# now moving onto the Ticket Manager class
# this will be responsible for managing all tickets

# second class: Ticket Manager

class TicketManager:

    # create a list to hold all tickets and a variable to keep track of the next ticket ID
    def __init__(self):
        self.__tickets = []
        self.__next_id = 1

    # when creating a hardware ticket, give it a title, description, and device
    def create_hardware_ticket(self, title, description, device):
        ticket = HardwareTicket(self.__next_id, title, description, device)
        # add the ticket to the collection and increment the next ticket ID
        self.add_ticket(ticket)
        self.__next_id += 1
        return ticket

    # when creating a software ticket, give it a title, description, and application
    def create_software_ticket(self, title, description, application):
        ticket = SoftwareTicket(self.__next_id, title, description, application)
        # add the ticket to the collection and increment the next ticket ID
        self.add_ticket(ticket)
        self.__next_id += 1
        return ticket

    # adding a ticket
    def add_ticket(self, ticket):
        # if the ticket is not an instance of the Ticket class, raise a TypeError
        if not isinstance(ticket, Ticket):
            raise TypeError("Only Ticket objects can be added.")
        # if a ticket with the same ID already exists, raise a ValueError
        # t is just an expression to cycle through the tickets in the list and check if any of them have the same ticket ID as the new ticket being added
        if any(t.get_ticket_id() == ticket.get_ticket_id()
               for t in self.__tickets):
            raise ValueError("A ticket with this ID already exists.")
        # add the ticket to the end of collection
        self.__tickets.append(ticket)

    # finding a ticket
    def find_ticket(self, ticket_id):
        # if the ticket ID exists in the collection, return the ticket
        for ticket in self.__tickets:
            if ticket.get_ticket_id() == ticket_id:
                return ticket
        # if the ticket ID doesn't exist, raise a KeyError
        raise KeyError(f"Ticket {ticket_id} could not be found.")

    # display all tickets
    def display_all_tickets(self):
        # if there are no tickets in the collection, print a message saying so
        if not self.__tickets:
            print("There are currently no tickets.")
            return
        # if there are tickets, print this header
        print("\n========= ALL SUPPORT TICKETS =========")
        # then print each ticket's details with a line to to separate them for readability
        for ticket in self.__tickets:
            print(ticket.get_details())
            print("--------------------------------------")

    # reassigning a ticket to another technician
    def reassign_ticket(self, ticket_id, technician):
        # find the ticket by ID, then assign the new technician to it
        ticket = self.find_ticket(ticket_id)
        ticket.assign_technician(technician)

    # removing a ticket
    def remove_ticket(self, ticket_id):
        # find the ticket by ID, then remove it from the collection
        ticket = self.find_ticket(ticket_id)
        self.__tickets.remove(ticket)
        print(f"Ticket {ticket_id} successfully removed.")


# that is all of the classes and behaviours for the system
# everything below is for the user interface

# for the interface, I am going with a simple CLI
# I would've liked to go with a GUI using Tkinter as I have experience with it, but I wanted to keep it simple and focus on the OOP concepts

# obs: input validation is completed within the user interface rather than the classes above. This is a design weakness.
# from a programming perspective, it would be better to validate input within the class itself, rather than the CLI
# particularly if the UI is eventually upgraded to a GUI, it would complicate that design process

# user can't enter empty strings for any input, so this function will keep prompting the user until they enter a non-empty string
def get_non_empty_input(prompt):
    # while loop will keep prompting the user until they enter a non-empty string
    while True:
        # strip removes whitespace from the input, so an input of just spaces is empty
        value = input(prompt).strip()
        # if the input is not empty, return it. Otherwise, prompt the user to try again
        if value:
            return value
        print("Input cannot be empty. Please try again.")

# this function gets a ticket ID from the user and checks it's valid
def get_ticket_id():
    while True:
        # try block to catch any ValueError exceptions that may occur when converting the input to an integer
        try:
            ticket_id = int(input("Enter ticket ID: "))
            # has to be a positive number
            if ticket_id <= 0:
                print("Ticket ID must be a positive number.")
                continue
            return ticket_id
        # except block to catch the ValueError exception and print an error message
        except ValueError:
            print("Please enter a valid whole number.")

# the main function will run the CLI and allow the user to interact with the system
def main():
    # create an instance of the TicketManager class to manage the tickets
    manager = TicketManager()
    # the while loop will keep the menu running until the user chooses to exit
    # otherwise the menu will disappear after one action and the user would have to restart the program to do anything else
    while True:
        # print all options for the user to choose from
        print("====================================")
        print("       IT SERVICE DESK SYSTEM")
        print("====================================")
        print("1. Create hardware ticket")
        print("2. Create software ticket")
        print("3. Display all tickets")
        print("4. View and process a ticket")
        print("5. Update ticket priority")
        print("6. Update ticket status")
        print("7. Assign / reassign technician")
        print("8. Remove ticket")
        print("9. Exit")
        # remove whitespace then accept the input
        choice = input("Select an option (1-9): ").strip()

        # try block to catch any exceptions that may occur during execution of the user's choice
        try:
            # create hardware ticket
            # if choice is 1, prompt user for title, description, and device, then create a hardware ticket
            if choice == "1":
                title = get_non_empty_input("Ticket title: ")
                description = get_non_empty_input("Description: ")
                device = get_non_empty_input("Device: ")
                ticket = manager.create_hardware_ticket(title, description, device)
                print(f"Hardware ticket {ticket.ticket_id} created.")

            # create software ticket
            # if choice is 2, prompt user for title, description, and application, then create a software ticket
            elif choice == "2":
                title = get_non_empty_input("Ticket title: ")
                description = get_non_empty_input("Description: ")
                application = get_non_empty_input("Application: ")
                ticket = manager.create_software_ticket(title, description, application)
                print(f"Software ticket {ticket.ticket_id} created.")

            # display all tickets
            # if choice is 3, call the display all tickets method of the TicketManager class to print all tickets
            elif choice == "3":
                manager.display_all_tickets()

            # find and process a ticket
            # if choice is 4, prompt user for ticket ID, find the ticket, then print its details and processing instructions
            elif choice == "4":
                ticket_id = get_ticket_id()
                ticket = manager.find_ticket(ticket_id)
                print(ticket.get_details())
                print("Processing instructions:")
                print(ticket.process_ticket())

            # update priority
            # if choice is 5, prompt user for ticket ID, find the ticket, then prompt for new priority and update it
            elif choice == "5":
                ticket_id = get_ticket_id()
                ticket = manager.find_ticket(ticket_id)
                print("Available priorities:", Ticket.VALID_PRIORITIES)
                priority = input("New priority: ").strip().title()
                ticket.update_priority(priority)
                print("Priority successfully updated.")

            # update status
            # if choice is 6, prompt user for ticket ID, find the ticket, then prompt for new status and update it
            elif choice == "6":
                ticket_id = get_ticket_id()
                ticket = manager.find_ticket(ticket_id)
                print("Available statuses:", Ticket.VALID_STATUSES)
                status = input("New status: ").strip().title()
                ticket.update_status(status)
                print("Status successfully updated.")

            # assign or reassign technician
            # if choice is 7, prompt user for ticket ID, find the ticket, then prompt for technician name and assign it
            elif choice == "7":
                ticket_id = get_ticket_id()
                technician = get_non_empty_input("Technician name: ")
                manager.reassign_ticket(ticket_id, technician)
                print("Technician successfully assigned.")

            # remove ticket
            # if choice is 8, prompt user for ticket ID, then remove the ticket from the collection
            elif choice == "8":
                ticket_id = get_ticket_id()
                manager.remove_ticket(ticket_id)

            # exit
            # if choice is 9, print a message and break the loop to exit the program
            elif choice == "9":
                print("Exiting IT Service Desk System.")
                break
            # if the user enters an invalid choice, print a message saying so
            else:
                print("Invalid selection. Please choose 1-9.")
        # except block to catch any exceptions that may occur during execution of the user's choice
        except (ValueError, KeyError, TypeError) as error:
            print(f"Error: {error}")


# start application
if __name__ == "__main__":
    main()
