
import unittest

# unit tests for the IT Service Desk Ticket Management System
# tests cover normal, boundary and invalid conditions
# together with inheritance, polymorphism and ticket management functionality


# bringing in the classes to be tested
from ticket_system import (
    Ticket,
    HardwareTicket,
    SoftwareTicket,
    TicketManager
)

# this is the main test class, it contains all the tests for the ticket system
# the methods inside this class are the actual test cases
class TestTicket(unittest.TestCase):
    # this creates a new HardwareTicket object before each test case is run, so each test case has a fresh object to work with
    def setUp(self):
        self.ticket = HardwareTicket(1, "Laptop issue", "Laptop will not start", "Dell Latitude")

    # this test checks that the ticket was created correctly and that the attributes are set correctly
    # assertequal just matches the expected value with the actual value. if they are not equal, the test will fail
    def test_hardware_ticket_creation(self):
        self.assertEqual(self.ticket.ticket_id, 1)
        self.assertEqual(self.ticket.title, "Laptop issue")
        self.assertEqual(self.ticket.device, "Dell Latitude")

    # this test checks that the default values for priority, status, and assigned technician are set correctly
    # again, its just checking that the expected value (medium, open, and unassigned) matches the actual value
    def test_default_values(self):
        self.assertEqual(self.ticket.priority, "Medium")
        self.assertEqual(self.ticket.status, "Open")
        self.assertEqual(self.ticket.assigned_technician, "Unassigned")

    # this test checks that the title is not empty or just whitespace, otherwise it raises a ValueError
    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            HardwareTicket(2, "   ", "Won't start", "Dell")

    # this test checks that the description is not empty or just whitespace, otherwise it raises a ValueError
    def test_empty_description_rejected(self):
        with self.assertRaises(ValueError):
            HardwareTicket(3, "Laptop issue", "   ", "Dell")
            
    # this test checks that the device is not empty or just whitespace, otherwise it raises a ValueError
    def test_empty_device_rejected(self):
        with self.assertRaises(ValueError):
            HardwareTicket(4, "Laptop issue", "Won't start", "   ")
            
    # this test checks that the priority can be updated to a valid value, and that the new value is set correctly
    def test_update_priority(self):
        self.ticket.update_priority("High")
        self.assertEqual(self.ticket.priority, "High")

    # this test checks that an invalid priority value raises a ValueError, and that the original priority stays the same
    def test_invalid_priority(self):
        with self.assertRaises(ValueError):
            self.ticket.update_priority("Urgent")
        # original priority is unchanged
        self.assertEqual(self.ticket.priority, "Medium")

    # this test checks that the priority is set to have the first letter capitalised, even if the input is in lowercase
    def test_priority_case_normalisation(self):
        self.ticket.update_priority("high")
        self.assertEqual(self.ticket.priority, "High")

    # this test checks the lowest valid priority
    def test_low_priority_boundary(self):
        self.ticket.update_priority("Low")
        self.assertEqual(self.ticket.priority, "Low")

    # this test checks the highest valid priority
    def test_critical_priority_boundary(self):
        self.ticket.update_priority("Critical")
        self.assertEqual(self.ticket.priority, "Critical")

    # this test checks that the status can be updated to a valid value, and that the new value is set correctly
    def test_update_status(self):
        self.ticket.update_status("In Progress")
        self.assertEqual(self.ticket.status, "In Progress")

    # this test checks that an invalid status value raises a ValueError, and that the original status stays the same
    def test_invalid_status(self):
        with self.assertRaises(ValueError):
            self.ticket.update_status("Pending")
        # original status is unchanged
        self.assertEqual(self.ticket.status, "Open")

    # this test checks that the status is set to have the first letter capitalised, even if the input is in lowercase
    def test_status_case_normalisation(self):
        self.ticket.update_status("closed")
        self.assertEqual(self.ticket.status, "Closed")

    # this test checks the final valid status
    def test_closed_status_boundary(self):
        self.ticket.update_status("Closed")
        self.assertEqual(self.ticket.status, "Closed")
        
    # this test checks that a technician can be assigned to the ticket, and that the assigned technician is set correctly
    # as mentioned in the system code, I don't have predetermined selectable technicians. Any string input will be accepted here
    def test_assign_technician(self):
        self.ticket.assign_technician("John Smith")
        self.assertEqual(self.ticket.assigned_technician, "John Smith")

    # this test checks that an empty or whitespace-only technician name raises a ValueError, and that the original assigned technician stays the same
    def test_empty_technician_rejected(self):
        with self.assertRaises(ValueError):
            self.ticket.assign_technician("   ")
        # original assigned technician is unchanged
        self.assertEqual(self.ticket.assigned_technician, "Unassigned")

    # this test checks that the get details method returns a string that contains the device and ticket ID
    def test_hardware_details(self):
        details = self.ticket.get_details()
        # assertin checks that the expected substring is in the actual string, if not, the test will fail
        self.assertIn("Device: Dell Latitude", details)
        self.assertIn("Ticket ID: 1", details)


# now moving onto testing polymorphism and inheritance

# this class contains tests for the polymorphism and inheritance aspects of the ticket system
class TestPolymorphism(unittest.TestCase):

    # this test checks that a SoftwareTicket can be created and that its attributes are set correctly
    def test_software_ticket_creation(self):
        ticket = SoftwareTicket(2, "Outlook issue", "Outlook keeps crashing", "Microsoft Outlook")
        self.assertEqual(ticket.ticket_id, 2)
        self.assertEqual(ticket.application, "Microsoft Outlook")

    # this test checks that the application name cannot be empty or whitespace
    def test_empty_application_rejected(self):
        with self.assertRaises(ValueError):
            SoftwareTicket(2, "Outlook issue", "Keeps crashing", "   ")

    # this test checks that the get details method of a SoftwareTicket returns a string that contains the application and ticket ID
    def test_software_ticket_details(self):
        ticket = SoftwareTicket(2, "Outlook issue", "Outlook keeps crashing", "Microsoft Outlook")
        self.assertIn("Application: Microsoft Outlook", ticket.get_details())

    # this test checks that the process ticket method of a hardware ticket returns a string that contains the word 'diagnostics', which it should since this method for a hardware ticket contains this word in the return string
    def test_hardware_processing(self):
        ticket = HardwareTicket(1, "Laptop issue", "Won't start", "Dell")
        result = ticket.process_ticket()
        self.assertIn("diagnostics", result)

    # same as above but for a software ticket, which should contain the word 'configuration' in the return string
    def test_software_processing(self):
        ticket = SoftwareTicket(2, "Outlook issue", "Keeps crashing", "Outlook")
        result = ticket.process_ticket()
        self.assertIn("configuration", result)

    # this test checks that process ticket is different for hardware and software tickets, which it should since they are different subclasses and have different implementations of this method
    def test_subclasses_have_different_processing(self):
        hardware = HardwareTicket(1, "Laptop issue", "Won't start", "Dell")
        software = SoftwareTicket(2, "Outlook issue", "Keeps crashing", "Outlook")
        # this is the actual comparison, checking that both values aren't equal
        self.assertNotEqual(hardware.process_ticket(), software.process_ticket())

    # this test checks that each subclass returns different details
    # demonstrating that get_details() behaves differently based on object type
    def test_subclasses_have_different_details(self):
        hardware = HardwareTicket(1, "Laptop issue", "Won't start", "Dell")

        software = SoftwareTicket(2, "Outlook issue", "Keeps crashing", "Outlook")

        self.assertNotEqual(hardware.get_details(), software.get_details())

    # this test checks that the Ticket class cannot be instantiated directly, which it shouldn't be able to since it is an abstract class
    def test_abstract_ticket_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Ticket(1, "Test", "Test description")


# now to test the Ticket Manager

# this class contains tests for the TicketManager class
class TestTicketManager(unittest.TestCase):

    # this method is run before each test case, it creates a new TicketManager object so each test case has a fresh manager to work with
    def setUp(self):
        self.manager = TicketManager()

    # this test checks that a hardware ticket can be created through the manager, and that the ticket ID is set correctly and that the returned object is an instance of HardwareTicket
    def test_create_hardware_ticket(self):
        ticket = self.manager.create_hardware_ticket("Laptop issue", "Won't start", "Dell")
        # this checks that the ticket ID is 1, since this is the first ticket created in this test case
        self.assertEqual(ticket.ticket_id, 1)
        # this checks that the returned object is an instance of HardwareTicket, which it should be since we are creating a hardware ticket
        self.assertIsInstance(ticket, HardwareTicket)

    # same as above but for a software ticket
    def test_create_software_ticket(self):
        ticket = self.manager.create_software_ticket("Outlook issue", "Keeps crashing", "Outlook")
        self.assertEqual(ticket.ticket_id, 1)
        self.assertIsInstance(ticket, SoftwareTicket)

    # this test checks that ticket IDs are unique and incrementing, even when creating different types of tickets
    def test_unique_ticket_ids(self):
        ticket1 = self.manager.create_hardware_ticket("Laptop issue", "Won't start", "Dell")
        ticket2 = self.manager.create_software_ticket("Outlook issue", "Keeps crashing", "Outlook")
        self.assertEqual(ticket1.ticket_id, 1)
        self.assertEqual(ticket2.ticket_id, 2)
        # checking that the ticket IDs are not equal, which they shouldn't be since they are different tickets
        self.assertNotEqual(ticket1.ticket_id, ticket2.ticket_id)

    # this test checks that ticket IDs increment sequentially regardless of ticket type
    def test_ids_increment_correctly(self):
        ticket1 = self.manager.create_hardware_ticket("Issue 1", "Description", "Laptop")
        ticket2 = self.manager.create_software_ticket("Issue 2", "Description", "Outlook")
        self.assertEqual(ticket1.ticket_id, 1)
        self.assertEqual(ticket2.ticket_id, 2)

    # this test checks that a ticket can be found by its ID, and that the returned object is the same as the one that was created
    def test_find_ticket(self):
        created = self.manager.create_hardware_ticket("Laptop issue", "Won't start", "Dell")
        retrieved = self.manager.find_ticket(1)
        # created and retrieved should be referring to the same object
        self.assertIs(created, retrieved)

    # this test checks that trying to find a ticket that doesn't exist raises a KeyError, which it should since the ticket ID is not in the collection
    def test_find_nonexistent_ticket(self):
        with self.assertRaises(KeyError):
            self.manager.find_ticket(999)

    # this test checks that a ticket can be reassigned to a different technician, and that the assigned technician is updated correctly
    def test_reassign_technician(self):
        ticket = self.manager.create_hardware_ticket("Laptop issue", "Won't start", "Dell")
        self.manager.reassign_ticket(1, "John Smith")
        self.assertEqual(ticket.assigned_technician, "John Smith")

    # this test checks that a ticket can be removed and a KeyError raised when a non-existent ticket ID is searched
    def test_remove_ticket(self):
        self.manager.create_hardware_ticket("Laptop issue", "Won't start", "Dell")
        self.manager.remove_ticket(1)
        with self.assertRaises(KeyError):
            self.manager.find_ticket(1)

    # this test checks that tickets cannot be duplicated with the same ID, and that a ValueError is raised when an attempt is made to add a duplicate ticket ID
    def test_duplicate_ticket_id(self):
        ticket1 = HardwareTicket(1, "Laptop issue", "Won't start", "Dell")
        ticket2 = HardwareTicket(1, "Monitor issue", "No display", "HP")
        self.manager.add_ticket(ticket1)
        with self.assertRaises(ValueError):
            self.manager.add_ticket(ticket2)

    # this test checks that only ticket objects can be added to the manager, and that a TypeError is raised when an attempt is made to add a non-ticket object
    def test_only_ticket_objects_can_be_added(self):
        with self.assertRaises(TypeError):
            self.manager.add_ticket("Not a ticket")


if __name__ == "__main__":
    unittest.main(verbosity=2)

# check if any tests missing, need full coverage
