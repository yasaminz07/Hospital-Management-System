# Imports
from Admin import Admin
from Doctor import Doctor
from Patient import Patient
from hosp_gui import HospitalGUI

def main():
    """
    The main function to be run when the program starts.
    """

    # Initializing the actors
    admin = Admin('admin', '123', 'B1 1AB')  # username is 'admin', password is '123'
    doctors = [
        Doctor('John', 'Smith', 'Internal Med'),
        Doctor('Jone', 'Smith', 'Pediatrics'),
        Doctor('Jone', 'Carlos', 'Cardiology')
    ]
    
    patients = admin.load_patients(doctors)
    
    discharged_patients = []

    # Keep trying to login until the login details are correct
    while True:
        if admin.login():
            running = True  # Allow the program to run
            break
        else:
            print('Incorrect username or password.')

    while running:
        # Print the menu
        print('Choose the operation:')
        print(' 1- Register/view/update/delete doctor')
        print(' 2- Discharge patients')
        print(' 3- View discharged patients')
        print(' 4- Assign doctor to a patient')
        print(' 5- Update admin details')
        print(' 6- Patients data')
        print(' 7- Management Report')
        print(' 8- Logout')
        print(' 9- Quit')

        # Get the option
        op = input('Option: ')

        if op == '1': 
            # 1- Register/view/update/delete doctor 
            admin.doctor_management(doctors)

        elif op == '2':
            # 2- View or discharge patients
            admin.discharge(patients, discharged_patients)
        
        elif op == '3':
            # 3- View discharged patients
            admin.view_discharge(discharged_patients)

        elif op == '4':
            # 4- Assign doctor to a patient
            admin.assign_doctor_to_patient(patients, doctors)

        elif op == '5':
            # Update admin details
            admin.update_details()

        elif op == '6':
            # Patients data
              # This will handle both loading or saving based on the user's choice
            admin.print_patients(patients)
            
            
        elif op == '7':
            # Management Report
            admin.management_report(patients, doctors)
        
        elif op == '8':
            # Logout
            print("Logging out...")
            admin.logout()  # Call logout method
            running = False  # Exit the program to go back to login

            # Re-enter the login section after logout
            while True:
                try:
                    if admin.login():
                        running = True  # Allow the program to run again after login
                        break
                except Exception as e:
                    print(str(e))

        elif op == '9':
            # Quit
            print('Exiting the program. Goodbye!')
            running = False

        else:
            print('Invalid option. Try again')


if __name__ == '__main__':
    main()