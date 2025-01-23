from Doctor import Doctor
from Patient import Patient
import random
from datetime import datetime, timedelta
from collections import defaultdict


class Admin:
    """A class that deals with the Admin operations"""
    def __init__(self, username, password, postcode = ''):
        """
        Args:
            username (string): Username
            password (string): Password
            address (string, optional): Address Defaults to ''
        """

        self.__username = username
        self.__password = password
        self._postcode =  postcode
        self.doctors = []  # A list to store doctor objects
        self.patients = []  # A list to store patient objects

    def get_doctors(self):
        return self.doctors  # Returns the list of doctors
    
    # Getter methods to access private variables
    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_postcode(self):
        return self._postcode

    # Setter methods to update private variables
    def update_username(self, new_username):
        self.__username = new_username

    def update_password(self, new_password):
        self.__password = new_password

    def update_address(self, new_postcode):
        self._postcode = new_postcode

    def view(self, patients):
        """
        Display the patient details, including their symptoms.
        Args:
            patients (list<Patient>): The list of patients to display.
        """
        # Print the header and separator only once
        if patients:  # Ensure there are patients to display
            for i, patient in enumerate(patients, start=1):
                print(f'{i:<3}| {patient}')
        
        
    def load_patients(self, doctors):
        """Loads patient data from a text file."""
        
        try:
            with open("database.txt", "r") as f:
                for line in f:
                    if not line.strip():
                        continue  # Skip empty lines

                    # Split line by ":" to get the correct fields
                    first_name, surname, age, mobile, postcode, doc_firstname, doc_surname, symptoms = line.strip().split(":")

                    # Create the patient object
                    patient = Patient(first_name, surname, age, mobile, postcode)
                    self.patients.append(patient)  # Add the patient to the list

                    # If no doctor is assigned (doctor name is empty or 'None'), print a message
                    if doc_firstname == "None" or doc_firstname is None:
                        pass
                    else:
                        # Find the doctor and assign the patient to them
                        for doctor in doctors:
                            if doctor.get_first_name() == doc_firstname and doctor.get_surname() == doc_surname:
                                # Reassign the patient to the new doctor
                                patient.link(doctor.full_name())  # Link the doctor to the patient
                                doctor.add_patient(patient)      # Add the patient to the doctor's list
                                break  # Exit the loop once the correct doctor is found

                    # Set the patient's symptoms (handle case where no symptoms exist)
                    if symptoms != "None":
                        symptoms_list = symptoms.split(",")  # Convert symptoms string into a list
                        for symptom in symptoms_list:
                            patient.add_symptom(symptom)
        

        except FileNotFoundError:
            print("The specified file does not exist.")
        except ValueError:
            print("Data format in the file is incorrect. Each line must have: first_name:surname:age:mobile:postcode:doctor_name:symptoms.")
        except Exception as e:
            print(f"Error loading patient data: {e}")
        
        return(self.patients)

    
    def print_patients(self, patients):
        
        for patient in patients:
            symptoms = ", ".join(patient.get_symptoms()) if patient.get_symptoms() else "None"
            print(f"\nPatient Details:\n"
                f"Full Name: {patient.full_name()}-\n"
                f"Age: {patient.get_age()}\n"
                f"Mobile: {patient.get_mobile()}\n"
                f"Postcode: {patient.get_postcode()}\n"
                f"Doctor: {patient.get_doctor()}\n"
                f"Symptoms: {symptoms}\n")
        
    
    
    def save_patients(self):
        """
        Saves patient data to a text file in the correct format (database.txt).
        Links each patient to their assigned doctor and includes symptoms.
        """
        try:
            with open("database.txt", "w") as f:  # Open the file in write mode
                for patient in self.patients:  # Ensure self.patients is used instead of self.__patients
                    # Prepare the line with patient data
                    doctor_name = patient.get_doctor() if patient.get_doctor() != 'None' else 'None'
                    symptoms = ", ".join(patient.get_symptoms()) if patient.get_symptoms() else 'None'

                    # If the doctor is assigned, we split the doctor's name and add the specialty
                    if doctor_name != 'None':
                        doctor_first_name, doctor_surname = doctor_name.split(" ", 1)
                        line = f"{patient.get_first_name()}:{patient.get_surname()}:{patient.get_age()}:{patient.get_mobile()}:{patient.get_postcode()}:{doctor_first_name}:{doctor_surname}:{symptoms}"
                    else:
                        # If no doctor is assigned, we just write 'None' for the doctor
                        line = f"{patient.get_first_name()}:{patient.get_surname()}:{patient.get_age()}:{patient.get_mobile()}:{patient.get_postcode()}:None:None:{symptoms}"

                    # Write the line to the file
                    f.write(line + "\n")

            print("Patient data saved successfully.")
        except Exception as e:
            print(f"Error saving patient data: {e}")

    def update_patient_file(patient):
            # Read all the lines in the file
            with open('database.txt', 'r') as file:
                lines = file.readlines()

            # Update the patient’s record (doctor assigned)
            with open('database.txt', 'w') as file:
                for line in lines:
                    parts = line.split(":")
                    if parts[0] == patient.get_first_name() and parts[1] == patient.get_surname():
                        # Update doctor in the specific patient's record
                        line = f'{patient.get_first_name()}:{patient.get_surname()}:{patient.get_age()}:{patient.get_mobile()}:{patient.get_postcode()}:{patient.get_doctor()}:{",".join(patient.get_symptoms())}\n'
                    file.write(line)

    def generate_random_date(self):
        """Generate a random appointment date between 1 and 30 days from today."""
        from datetime import datetime, timedelta
        import random

        today = datetime.today()
        random_days = random.randint(1, 30)
        random_date = today + timedelta(days=random_days)
        return random_date.strftime("%Y-%m-%d")

    def management_report(self, patients, doctors):
        """
        Generate a management report that groups patients by surname and doctors by surname,
        and lists scheduled appointments.
        """
        print("----- Management Report ----- \n")

        # Grouping patients by surname
        patient_groups = {}
        for patient in patients:
            surname = patient.get_surname()
            if surname not in patient_groups:
                patient_groups[surname] = []
            patient_groups[surname].append(patient)

        # Grouping doctors by surname
        doctor_groups = {}
        for doctor in doctors:
            surname = doctor.get_surname()
            if surname not in doctor_groups:
                doctor_groups[surname] = []
            doctor_groups[surname].append(doctor)

        # Print patient groups
        print("----- Patients ----- \n")
        # Print the total count of patients above the patient groups
        total_patients = len(patients)  # Count all patients
        print(f"Total Patients: {total_patients}\n")
        for surname, group in patient_groups.items():
            print(f"Family: {surname}")
            for patient in group:
                print(f"  {patient.full_name()} | Age: {patient.get_age()} | Mobile: {patient.get_mobile()}")
                print(f"  Symptoms: {', '.join(patient.get_symptoms()) if patient.get_symptoms() else 'None'}")
                if patient.get_doctor() != "None":
                    print(f"  Appointed to: Dr. {patient.get_doctor()} | Appointment Date: {self.generate_random_date()}")
                print()

        # Print doctor groups
        print("----- Doctors -----")
        # Print the total count of doctors above the doctor groups
        total_doctors = len(doctors)  # Count all doctors
        print(f"\nTotal Doctors: {total_doctors}\n")
        for surname, group in doctor_groups.items():
            print(f"Doctor Surname: {surname}")
            for doctor in group:
                # Get the list of patients assigned to the doctor
                assigned_patients = [p for p in patients if p.get_doctor() == doctor.full_name()]
                assigned_patients_count = len(assigned_patients)  # Count the number of patients assigned to this doctor
                print(f"  Dr. {doctor.full_name()} | Speciality: {doctor.get_speciality()}")
                print(f"  Patients Assigned: {assigned_patients_count}")
                if assigned_patients_count > 0:
                    print(f"  Assigned Patients: {', '.join(p.full_name() for p in assigned_patients)}")
                print()
        
        # Total number of appointments per month per doctor
        print("----- Appointments per Month per Doctor -----\n")
        doctor_appointments_per_month = defaultdict(lambda: defaultdict(int))  # doctor -> month -> count
        for patient in patients:
            if patient.get_doctor() != "None":
                doctor_name = patient.get_doctor()
                # Assume generate_random_date() returns a valid date in YYYY-MM-DD format
                appointment_date = self.generate_random_date()  # Replace with actual date if needed
                month = datetime.strptime(appointment_date, '%Y-%m-%d').strftime('%B')  # Extract month name
                doctor_appointments_per_month[doctor_name][month] += 1

        # Check if there are any appointments scheduled
        if not doctor_appointments_per_month:
            print("  There are no appointments scheduled.\n")
        else:
            # Print appointments per month for each doctor
            for doctor_name, month_counts in doctor_appointments_per_month.items():
                print(f"Dr. {doctor_name}:")
                for month, count in month_counts.items():
                    print(f"  {month}: {count} appointments")
                print()

        # Total number of patients based on the illness type (symptom)
        print("----- Patients Per Illness -----\n")
        illness_type_count = defaultdict(int)  # Illness type -> patient count

        for patient in patients:
            for symptom in patient.get_symptoms():
                # Normalize the symptom (capitalize the first letter, lower the rest)
                normalized_symptom = symptom.strip().capitalize()
                illness_type_count[normalized_symptom] += 1

        # Check if there are any symptoms reported
        if not illness_type_count:
            print("  There are no symptoms reported.\n")
        else:
            # Print the illness type count
            for illness, count in illness_type_count.items():
                print(f"  {illness}: {count} patients\n")


    def display_management_report(self, patients, doctors):
        """Display the management report."""
        self.management_report(patients, doctors)

        # Call this function from your menu or somewhere in your main loop
        self.display_management_report(patients, doctors)
        

    def login(self) :
        """
        A method that deals with the login
        Raises:
            Exception: returned when the username and the password ...
                    ... don`t match the data registered
        Returns:
            string: the username
        """
    
        print("-----Login-----")
        #Get the details of the admin

        username = input('Enter the username: ')
        password = input('Enter the password: ')

        # check if the username and password match the registered ones
        if username == self.__username and password == self.__password :
            print("Login successful")
            return username
        else :
            raise Exception("Invalid username or password")
        
    def logout(self):
        """
        A method that logs out the admin by clearing the username and password
        """
        print("Logged out successfully.")

    def find_index(self,index,doctors):
        
            # check that the doctor id exists          
        if index in range(0,len(doctors)):
            
            return True

        # if the id is not in the list of doctors
        else:
            return False
            
    def get_doctor_details(self) :
        """
        Get the details needed to add a doctor
        Returns:
            first name, surname and ...
                            ... the speciality of the doctor in that order.
        """
        first_name = input('Enter the first name of the doctor: ')
        surname = input('Enter the surname of the doctor: ')
        speciality = input('Enter the speciality of the doctor: ')
        return first_name, surname, speciality
        # register
        
    def doctor_management(self, doctors):
        print("-----Doctor Management-----")
        print('Choose the operation:')
        print(' 1 - Register')
        print(' 2 - View')
        print(' 3 - Update')
        print(' 4 - Delete')
        op = input('Option: ')

        if op == '1':
            first_name, surname, speciality = self.get_doctor_details()
            for doctor in doctors:
                if first_name == doctor.get_first_name() and surname == doctor.get_surname():
                    print('Name already exists.')
                    return
            doctor = Doctor(first_name, surname, speciality)
            doctors.append(doctor)
            print('Doctor registered.')

        elif op == '2':
            print("-----List of Doctors-----")
            if not doctors:
                print('No doctors registered.')
            else:
                for i, doctor in enumerate(doctors):
                    print(f'{i+1}. {doctor.get_first_name()} {doctor.get_surname()} - {doctor.get_speciality()}')

        elif op == '3':
            print("-----Update Doctor's Details-----")
            self.view(doctors)
            try:
                index = int(input('Enter the ID of the doctor: ')) - 1
                if self.find_index(index, doctors):
                    doctor = doctors[index]
                    print('1. First name')
                    print('2. Surname')
                    print('3. Speciality')
                    op = int(input('Choose the field to update: '))
                    if op == 1:
                        doctor.set_first_name(input('Enter new first name: '))
                    elif op == 2:
                        doctor.set_surname(input('Enter new surname: '))
                    elif op == 3:
                        doctor.set_speciality(input('Enter new speciality: '))
                    else:
                        print('Invalid option.')
                else:
                    print('Invalid ID.')
            except ValueError:
                print('Invalid input.')

        elif op == '4':
            print("-----Delete Doctor-----")
            self.view(doctors)
            try:
                index = int(input('Enter the ID of the doctor to delete: ')) - 1
                if self.find_index(index, doctors):
                    doctors.pop(index)
                    print('Doctor deleted.')
                else:
                    print('Invalid ID.')
            except ValueError:
                print('Invalid input.')

    def view_patient(self, patients):
        """
        print a list of patients
        Args:
            patients (list<Patients>): list of all the active patients
        """
        print("-----View Patients-----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
        print('-' * 80)  # Adds a separator for better readability

        # Check if the patients list is empty
        if not patients:
            print("No patients registered.")
            return

        # Loop through the list of patients
        for index, patient in enumerate(patients):
            try:
                patient_name = patient.full_name()  # Use the full_name() method
                doctor_name = patient.get_doctor()  # Use the get_doctor() method
                print(f"{index + 1:2} | {patient_name:25} | {doctor_name:30} | {patient._Patient__age:3} | {patient._Patient__mobile:12} | {patient._Patient__postcode}")
            except AttributeError:
                print(f"Error: Patient at index {index + 1} has missing or invalid data.")


    def assign_doctor_to_patient(self, patients, doctors):
        """
        Allow the admin to assign a doctor to a patient and report symptoms.
        Args:
            patients (list<Patients>): the list of all the active patients
            doctors (list<Doctor>): the list of all the doctors
        """
        print("-----Assign-----")
        print("-----Patients-----")
        print("ID |          Full Name           |      Doctor's Full Name      | Age |    Mobile     | Address |      Symptoms      |")
        print("-" * 120)
        self.view(patients)  # Assuming the view method displays patient info in the same format

        # Ask whether you want to assign a doctor, report symptoms, or go back
        print("Would you like to assign a doctor or report a symptom for a patient?:")
        print("1. Assign a doctor")
        print("2. Report a symptom")
        print("3. Go back")

        action = input("Enter 1, 2, or 3: ").strip()

        if action == '1':
            patient_index = input('Please enter the patient ID to assign a doctor: ')

            try:
                # patient_index is the patient ID minus one (-1) for zero-based indexing
                patient_index = int(patient_index) - 1

                # Check if the id is not in the list of patients
                if patient_index not in range(len(patients)):
                    print('The id entered was not found.')
                    return  # Stop the procedure

            except ValueError:  # The entered ID could not be converted into an integer
                print('The id entered is incorrect.')
                return  # Stop the procedure

            # Get the patient object
            patient = patients[patient_index]

            # Check if the patient already has an assigned doctor
            if patient.get_doctor() != 'None':
                print(f"This patient is currently assigned to Dr. {patient.get_doctor()}.")
                reassign = input("Would you like to reassign them to a different doctor? (Y/N): ").strip().upper()

                if reassign != 'Y':
                    print("No changes made.")
                    return  # Exit if they don't want to reassign

            print("\n-----Doctors Select-----")
            print('Select the doctor that fits these symptoms:')
            patient.print_symptoms()  # Print the patient's symptoms again

            print('--------------------------------------------------')
            print('ID |          Full Name           |  Speciality   ')
            print('--------------------------------------------------')
            self.view(doctors)

            doctor_index = input('Please enter the doctor ID: ')

            try:
                # doctor_index is the doctor ID minus one (-1) for zero-based indexing
                doctor_index = int(doctor_index) - 1

                # Check if the id is in the list of doctors
                if self.find_index(doctor_index, doctors) != False:
                    # Link the patient to the new doctor and vice versa
                    doctor = doctors[doctor_index]

                    # Unassign the patient from their current doctor, if any
                    if patient.get_doctor() != 'None':
                        current_doctor = next((d for d in doctors if d.full_name() == patient.get_doctor()), None)
                        if current_doctor:
                            current_doctor.remove_patient(patient)  # Remove patient from the current doctor

                    # Reassign the patient to the new doctor
                    patient.link(doctor.full_name())  # Use the link method of Patient
                    doctor.add_patient(patient)      # Use the add_patient method of Doctor

                    print(f'The patient is now assigned to Dr. {doctor.full_name()}.')
                    print("\nUpdated symptoms for the patient:")
                    patient.print_symptoms()  # Print symptoms after assignment

                    # Save the updated information to the file
                    self.save_patients()  # <-- Save the changes here

                # If the doctor ID is not in the list of doctors
                else:
                    print('The doctor id entered was not found.')

            except ValueError:  # The entered ID could not be converted into an integer
                print('The id entered is incorrect.')

        elif action == '2':
            patient_index = input('Please enter the patient ID to report symptoms: ')

            try:
                # patient_index is the patient ID minus one (-1) for zero-based indexing
                patient_index = int(patient_index) - 1

                # Check if the id is not in the list of patients
                if patient_index not in range(len(patients)):
                    print('The id entered was not found.')
                    return  # Stop the procedure

            except ValueError:  # The entered ID could not be converted into an integer
                print('The id entered is incorrect.')
                return  # Stop the procedure

            # Get the patient object
            patient = patients[patient_index]

            patient.remove_all_symptoms()

            # Allow reporting symptoms
            print("\n-----Report Symptoms-----")
            while True:
                symptom = input("Enter a symptom for the patient (or type 'done' to finish): ").strip()
                if symptom.lower() == 'done':
                    break
                elif symptom:  # Ensure non-empty input
                    patient.add_symptom(symptom)  # Add the symptom to the patient's symptom list
                    print(f"Symptom '{symptom}' has been added.")
                    print("\nUpdated symptoms for the patient:")
                    patient.print_symptoms()  # Use the existing method to display symptoms
                else:
                    print("Symptom cannot be empty. Please try again.")

            print("\nUpdated symptoms for the patient:")
            patient.print_symptoms()

            # Save the updated information to the file
            self.save_patients()  # <-- Save the changes here

        elif action == '3':
            print("Returning to the menu.")
            return  # Go back to the menu

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    def discharge(self, patients, discharge_patients):
        """
        Allow the admin to discharge a patient when treatment is done.
        Args:
            patients (list<Patient>): the list of all the active patients
            discharge_patients (list<Patient>): the list of all the non-active patients
        """
        while True:
            print("\n-------------------------------------------- Discharge Patient --------------------------------------------")

            # Print the list of active patients
            print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode | Symptoms')
            for index, patient in enumerate(patients, start=1):
                symptoms = ', '.join(patient._Patient__symptoms) if patient._Patient__symptoms else 'None'  # Accessing the private symptom list
                print(f"{index:<3}| {patient.full_name():<25}    | {patient.get_doctor():<25}    | {patient._Patient__age:<3} |  {patient._Patient__mobile:<12} |  {patient._Patient__postcode:<8}| {symptoms:<10}")

            # Ask the admin if they want to discharge a patient
            choice = input("\nDo you want to discharge a patient? (Y/N): ").strip().upper()

            if choice == 'N':
                print("Exiting discharge process.")
                break
            elif choice == 'Y':
                # Ask for the patient ID
                patient_index = input("Please enter the patient ID to discharge: ").strip()

                try:
                    # Convert patient_index to int and adjust for 0-based indexing
                    patient_index = int(patient_index) - 1

                    # Check if the index is valid
                    if 0 <= patient_index < len(patients):
                        # Display patient details and confirm discharge
                        patient = patients[patient_index]
                        symptoms = ', '.join(patient._Patient__symptoms)
                        print(f"\nSelected Patient:\n"
                            f"Full Name: {patient.full_name()}\n"
                            f"Doctor: {patient.get_doctor()}\n"
                            f"Age: {patient._Patient__age}\n"
                            f"Mobile: {patient._Patient__mobile}\n"
                            f"Postcode: {patient._Patient__postcode}\n"
                            f"Symptoms: {symptoms}")
                        
                        confirm = input("\nConfirm discharge of this patient? (Y/N): ").strip().upper()
                        if confirm == 'Y':
                            # Remove the patient from the active list and add to the discharged list
                            discharged_patient = patients.pop(patient_index)
                            discharge_patients.append(discharged_patient)
                            print(f"Patient {discharged_patient.full_name()} has been successfully discharged and removed from the system.")
                        else:
                            print("Discharge canceled.")
                    else:
                        print("The ID entered does not exist in the list of patients.")

                except ValueError:
                    print("The ID entered is not valid. Please enter a numeric value.")
            else:
                print("Invalid choice. Please enter 'Y' or 'N'.")


    def view_discharge(self, discharged_patients):
        """
        Prints the list of all discharged patients.
        Args:
            discharge_patients (list<Patient>): the list of all the non-active patients
        """
        print("\n----- Discharged Patients -----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode | Symptoms')

        if not discharged_patients:
            print("No discharged patients available.")
        else:
            for index, patient in enumerate(discharged_patients, start=1):
                symptoms = ', '.join(patient._Patient__symptoms)  # Access private symptoms list
                print(f"{index:<3}| {patient.full_name():<25}    | {patient.get_doctor():<25}    | {patient._Patient__age:<3} |  {patient._Patient__mobile:<12} |  {patient._Patient__postcode:<8}| {symptoms}")

        
    def update_details(self):
            """
            Allows the user to update and change username, password and address
            """

            print('Choose the field to be updated:')
            print(' 1 Username')
            print(' 2 Password')
            print(' 3 Address')
            op = int(input('Input: '))
            updated = False  # Flag to track if any update was successful

            if op == 1:
                username = input('Enter new username: ')
                if username == input('Enter the new username again: '):
                    self.__username = username
                    print('Username updated.')
                    updated = True

            elif op == 2:
                password = input('Enter the new password: ')
                # validate the password
                if password == input('Enter the new password again: '):
                    self.__password = password
                    print('Password updated.')
                    updated = True

            elif op == 3:
                postcode = input('Enter the new address: ')

                if postcode == input('Enter the new address again: '):
                    self._postcode = postcode
                    print('Address updated.')
                    updated = True
                
            if not updated:
                print('Invalid option or inputs did not match. Please try again.')
