import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from collections import defaultdict
from datetime import datetime
from datetime import timedelta
import random
from Doctor import Doctor
from Admin import Admin
from Patient import Patient

class HospitalGUI:

    def __init__(self):
        # Create an Admin instance with a predefined username and password
        self.admin = Admin(username="admin", password="123")

        self.parent = tk.Tk()
        self.parent.title("Hospital Management System")
        self.parent.geometry("900x700")  # Set window size (width x height)
        
        self.admin = Admin('admin', '123', 'B1 1AB')  # username is 'admin', password is '123'
        self.doctors = [
        Doctor('John', 'Smith', 'Internal Med'),
        Doctor('Jone', 'Smith', 'Pediatrics'),
        Doctor('Jone', 'Carlos', 'Cardiology')
        ]
        self.patients = [
        Patient('Sara', 'Smith', 20, '07012345678', 'B1 234'),
        Patient('Mike', 'Jones', 37, '07555551234', 'L2 2AB'),
        Patient('David', 'Smith', 15, '07123456789', 'C1 ABC')
        ]
        self.discharged_patients = []  # List of discharged patients
        # Set background color for the main window
        self.parent.configure(bg="#89CFF0")

        # Create a frame to center the widgets
        self.center_frame = tk.Frame(self.parent, bg="#89CFF0")
        self.center_frame.pack(expand=True)

        self.create_widgets()

        # Handle when the user tries to close the window (e.g., using the 'X' button)
        self.parent.protocol("WM_DELETE_WINDOW")

        self.parent.mainloop()

    def create_widgets(self):
        # Create and place the username label and entry
        tk.Label(self.center_frame, text="Username:", bg="#89CFF0").pack(pady=5)
        self.username_entry = tk.Entry(self.center_frame)
        self.username_entry.pack(pady=5)

        # Create and place the password label and entry
        tk.Label(self.center_frame, text="Password:", bg="#89CFF0").pack(pady=5)
        self.password_entry = tk.Entry(self.center_frame, show="*")
        self.password_entry.pack(pady=5)

        # Create and place the login button
        tk.Button(
            self.center_frame,
            text="Login",
            command=self.validate_login,
            bg="white",  # Set background color to white
            fg="black",  # Text color
            activebackground="gray",  # Background when clicked
            activeforeground="white",  # Text color when clicked
            relief="flat",  # Remove button border
            padx=15,  # Add padding for a larger button
            pady=2
        ).pack(pady=10)

    def validate_login(self):
        userid = self.username_entry.get()
        password = self.password_entry.get()

        # Validate credentials using the Admin instance
        try:
            if userid == self.admin._Admin__username and password == self.admin._Admin__password:
                messagebox.showinfo("Login Successful", f"Welcome, {userid}!")
                self.show_admin_menu()  # Proceed to admin menu
            else:
                raise Exception("Invalid username or password")
        except Exception as e:
            messagebox.showerror("Login Failed", str(e))

    def show_admin_menu(self):
        # Hide the login widgets and show the admin menu widgets
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        # Admin Menu
        tk.Label(self.center_frame, text="Choose the operation:", bg="#89CFF0").pack(pady=5)

        tk.Button(
            self.center_frame,
            text="Register/View/Update/Delete Doctor",
            command=self.manage_doctors,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
    ).pack(pady=10, fill='x')

        tk.Button(
            self.center_frame,
            text="Discharge Patients",
            command=self.discharge_patients,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
    ).pack(pady=10, fill='x')

        tk.Button(
            self.center_frame,
            text="View Discharged Patients",
            command=self.view_discharged_patients,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
    ).pack(pady=10, fill='x')

        tk.Button(
            self.center_frame,
            text="Assign Doctor to a Patient",
            command=self.assign_doctor_to_patient,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
    ).pack(pady=10, fill='x')

        tk.Button(
            self.center_frame,
            text="Update Admin Details",
            command=self.update_admin_details,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
    ).pack(pady=10, fill='x')

        tk.Button(
            self.center_frame,
            text="Management Report",
            command=self.show_management_report,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
    ).pack(pady=10, fill='x')
        
        tk.Button(
            self.center_frame,
            text="Logout",
            command=self.logout,  # Call the logout method
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
    ).pack(pady=10, fill='x')

        tk.Button(
            self.center_frame,
            text="Quit",
            command=self.quit_app,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
    ).pack(pady=10, fill='x')

        # Make sure the window size adjusts to fit the content
        self.parent.geometry('900x700')  # Adjust window size if needed

    def logout(self):
        # Clear the current login session and show the login screen again
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        # Hide admin menu widgets and show login screen
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        self.create_widgets()  # Show login widgets again

    def go_back_to_admin_menu(self):
        # Close the doctor management window and go back to the admin menu
        self.manage_doctors_window.destroy()
        self.show_admin_menu()

    def manage_doctors(self):
        # Clear the existing widgets
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        # Display the doctor management options
        tk.Label(self.center_frame, text="Choose an operation:", bg="#89CFF0").pack(pady=5)

        # Buttons for different operations
        tk.Button(
            self.center_frame,
            text="Register Doctor",
            command=self.show_register_form,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10, fill='x')

        tk.Button(
            self.center_frame,
            text="View Doctors",
            command=self.view_doctors,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10, fill='x')

        tk.Button(
            self.center_frame,
            text="Update Doctor",
            command=self.show_update_doctor_form,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10, fill='x')

        tk.Button(
            self.center_frame,
            text="Delete Doctor",
            command=self.show_delete_doctor_form,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10, fill='x')

        # Back button to go back to the admin menu
        tk.Button(
            self.center_frame,
            text="Back",
            command=self.show_admin_menu,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10, fill='x')

    def show_register_form(self):
        # Clear the existing widgets
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        # Register Doctor form
        tk.Label(self.center_frame, text="First Name:", bg="#89CFF0").pack(pady=5)
        self.first_name_entry = tk.Entry(self.center_frame)
        self.first_name_entry.pack(pady=5)

        tk.Label(self.center_frame, text="Surname:", bg="#89CFF0").pack(pady=5)
        self.surname_entry = tk.Entry(self.center_frame)
        self.surname_entry.pack(pady=5)

        tk.Label(self.center_frame, text="Speciality:", bg="#89CFF0").pack(pady=5)
        self.speciality_entry = tk.Entry(self.center_frame)
        self.speciality_entry.pack(pady=5)

        tk.Button(
            self.center_frame,
            text="Submit",
            command=self.register_doctor,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10)

        # Back button to go back to doctor management options
        tk.Button(
            self.center_frame,
            text="Back",
            command=self.manage_doctors,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10)

    def register_doctor(self):
        first_name = self.first_name_entry.get()
        surname = self.surname_entry.get()
        speciality = self.speciality_entry.get()

        # Check if all fields are filled
        if not first_name or not surname or not speciality:
            messagebox.showerror("Error", "Please fill all fields.")
            return

        # Create the new doctor
        doctor = Doctor(first_name, surname, speciality)


        # Check if doctor already exists
        for existing_doctor in self.doctors:
            if existing_doctor.get_first_name() == doctor.get_first_name() and \
            existing_doctor.get_surname() == doctor.get_surname():
                messagebox.showerror("Error", "This doctor already exists.")
                return
        else:
            # Show success message
            messagebox.showinfo("Success", f"Doctor {first_name} {surname} registered.")

        # Add the new doctor to the list
        self.doctors.append(doctor)

        # Clear the form after submission
        self.first_name_entry.delete(0, tk.END)
        self.surname_entry.delete(0, tk.END)
        self.speciality_entry.delete(0, tk.END)

        # Go back to the doctor management screen
        self.manage_doctors()

    def view_doctors(self):
        # Clear the existing widgets
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        tk.Label(self.center_frame, text="List of Doctors:", bg="#89CFF0").pack(pady=5)

        
        if not self.doctors:
            tk.Label(self.center_frame, text="No doctors registered.", bg="#89CFF0").pack(pady=5)
        else:
            for i, doctor in enumerate(self.doctors):
                # Show doctor index and details in the format: 1. John Smith - Internal Medicine
                tk.Label(self.center_frame, 
                        text=f"{i + 1}. {doctor.get_first_name()} {doctor.get_surname()} - {doctor.get_speciality()}", 
                        bg="#89CFF0").pack(pady=5)

        # Back button to go back to doctor management options
        tk.Button(
            self.center_frame,
            text="Back",
            command=self.manage_doctors,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10)

    def show_update_doctor_form(self):
        # Clear the existing widgets
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        # Label for the Listbox
        tk.Label(self.center_frame, text="Select a Doctor to Update:", bg="#89CFF0").pack(pady=5)

        # Listbox to display doctors
        self.doctors_listbox = tk.Listbox(self.center_frame, width=50, height=10)
        self.doctors_listbox.pack(pady=5)

        # Populate the Listbox with registered doctors
        for doctor in self.doctors:
            self.doctors_listbox.insert(tk.END, f"{doctor.get_first_name()} {doctor.get_surname()} - {doctor.get_speciality()}")

        # Button to proceed to update selected doctor
        tk.Button(
            self.center_frame,
            text="Update Selected Doctor",
            command=self.open_update_doctor_window,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10)

        # Back button to return to doctor management
        tk.Button(
            self.center_frame,
            text="Back",
            command=self.manage_doctors,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10)

    def open_update_doctor_window(self):
        # Get the selected doctor
        selected_index = self.doctors_listbox.curselection()
        if not selected_index:
            tk.messagebox.showwarning("Warning", "Please select a doctor to update.")
            return

        # Retrieve the selected doctor
        selected_doctor = self.doctors[selected_index[0]]

        # Create a new window for updating doctor details
        update_window = tk.Toplevel(self.parent)
        update_window.title("Update Doctor Details")
        update_window.geometry("900x700")
        update_window.configure(bg="#89CFF0")

        # Labels and entry fields for updating details
        tk.Label(update_window, text="First Name:", bg="#89CFF0").pack(pady=5)
        first_name_entry = tk.Entry(update_window)
        first_name_entry.insert(0, selected_doctor.get_first_name())
        first_name_entry.pack(pady=5)

        tk.Label(update_window, text="Username:", bg="#89CFF0").pack(pady=5)
        surname_entry = tk.Entry(update_window)
        surname_entry.insert(0, selected_doctor.get_surname())
        surname_entry.pack(pady=5)

        tk.Label(update_window, text="Speciality:", bg="#89CFF0").pack(pady=5)
        speciality_entry = tk.Entry(update_window)
        speciality_entry.insert(0, selected_doctor.get_speciality())
        speciality_entry.pack(pady=5)

        # Update button to save changes
        tk.Button(
            update_window,
            text="Save Changes",
            command=lambda: self.save_updated_doctor(
                selected_doctor,
                first_name_entry.get(),
                surname_entry.get(),
                speciality_entry.get(),
                update_window
            ),
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10)

        # Cancel button to close the update window
        tk.Button(
            update_window,
            text="Cancel",
            command=update_window.destroy,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10)

    def save_updated_doctor(self, doctor, first_name, surname, speciality, update_window):
        # Update the doctor's details
        doctor.set_first_name(first_name)
        doctor.set_surname(surname)
        doctor.set_speciality(speciality)

        # Show success message
        tk.messagebox.showinfo("Success", "Doctor details updated successfully.")
        
        # Close the update window
        update_window.destroy()

        # Refresh the update doctor form
        self.show_update_doctor_form()


    def show_delete_doctor_form(self):
        # Clear the existing widgets
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        # Delete Doctor form
        tk.Label(self.center_frame, text="Enter Doctor ID to Delete:", bg="#89CFF0").pack(pady=5)
        self.delete_doctor_id_entry = tk.Entry(self.center_frame)
        self.delete_doctor_id_entry.pack(pady=5)

        tk.Button(
            self.center_frame,
            text="Delete",
            command=self.delete_doctor,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10)

        # Back button to go back to doctor management options
        tk.Button(
            self.center_frame,
            text="Back",
            command=self.manage_doctors,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10)

    def show_delete_doctor_form(self):
        # Clear the existing widgets
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        # Label for Delete Doctor page
        tk.Label(self.center_frame, text="Delete Doctor", bg="#89CFF0").pack(pady=10)

        # Listbox to display doctors
        self.doctors_listbox = tk.Listbox(self.center_frame, width=50, height=10)
        self.doctors_listbox.pack(pady=5)

        # Populate the Listbox with registered doctors
        for doctor in self.doctors:
            self.doctors_listbox.insert(
                tk.END, f"{doctor.get_first_name()} {doctor.get_surname()} - {doctor.get_speciality()}"
            )

        # Button to delete selected doctor
        tk.Button(
            self.center_frame,
            text="Delete Selected Doctor",
            command=self.delete_selected_doctor,
            bg="white",
            fg="black",
            activebackground="darkred",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10)

        # Back button to go back to doctor management options
        tk.Button(
            self.center_frame,
            text="Back",
            command=self.manage_doctors,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5
        ).pack(pady=10)

    def delete_selected_doctor(self):
        # Get the selected doctor from the Listbox
        selected_index = self.doctors_listbox.curselection()
        if not selected_index:
            tk.messagebox.showwarning("Warning", "Please select a doctor to delete.")
            return

        # Confirm deletion
        confirm = tk.messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected doctor?")
        if confirm:
            # Remove the doctor from the list
            deleted_doctor = self.doctors.pop(selected_index[0])

            # Show success message
            tk.messagebox.showinfo(
                "Success",
                f"Doctor {deleted_doctor.get_first_name()} {deleted_doctor.get_surname()} has been deleted."
            )

            # Refresh the delete doctor form
            self.show_delete_doctor_form()

    def discharge_patients(self):
        # Create a new frame for the discharge functionality
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        tk.Label(self.center_frame, text="Discharge Patients", bg="#89CFF0").pack(pady=10)

        # Create a listbox to display patients
        self.patients_listbox = tk.Listbox(self.center_frame, height=10, width=40)
        for patient in self.patients:
            self.patients_listbox.insert(tk.END, patient.full_name())  # Display patient's full name
        self.patients_listbox.pack(pady=10)

        # Create discharge button
        discharge_button = tk.Button(
            self.center_frame, 
            text="Discharge", 
            command=self.confirm_discharge_patient, 
            bg="#1E90FF", 
            fg="white", 
            padx=20, 
            pady=10
        )
        discharge_button.pack(pady=10)

        # Back Button
        back_button = tk.Button(
            self.center_frame,
            text="Back",
            command=self.show_admin_menu,  # Go back to admin menu
            bg="white",
            fg="black",
            padx=20,
            pady=10
        )
        back_button.pack(pady=10)

    def confirm_discharge_patient(self):
        selected_index = self.patients_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "Please select a patient to discharge.")
            return

        # Get the selected patient from the list
        selected_patient = self.patients[selected_index[0]]

        # Confirm discharge
        confirm = messagebox.askyesno("Confirm Discharge", f"Are you sure you want to discharge {selected_patient.full_name()}?")
        if confirm:
            # Remove patient from the main list and Listbox
            self.patients.pop(selected_index[0])
            self.patients_listbox.delete(selected_index[0])

            # Add the patient to discharged patients list
            self.discharged_patients.append(selected_patient)

            messagebox.showinfo("Success", f"{selected_patient.full_name()} has been discharged.")



    def view_discharged_patients(self):
        # Create a new frame to display the discharged patients
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        tk.Label(self.center_frame, text="Discharged Patients", bg="#89CFF0").pack(pady=10)

        # If there are no discharged patients, show a message
        if not self.discharged_patients:
            messagebox.showinfo("No Discharged Patients", "There are no discharged patients.")
            self.show_admin_menu()
            return

        # Create a listbox to display discharged patients
        self.discharged_patients_listbox = tk.Listbox(self.center_frame, height=10, width=40)
        for patient in self.discharged_patients:
            self.discharged_patients_listbox.insert(tk.END, patient.full_name())  # Display discharged patient's full name
        self.discharged_patients_listbox.pack(pady=10)

        # Back Button
        back_button = tk.Button(
            self.center_frame,
            text="Back",
            command=self.show_admin_menu,  # Go back to admin menu
            bg="white",
            fg="black",
            padx=20,
            pady=10
        )
        back_button.pack(pady=10)


    def display_patients(self):
        """Display the list of patients."""
        patient_window = tk.Toplevel(self.root)
        patient_window.title("Select Patient")
        patient_window.geometry("600x400")

        listbox = tk.Listbox(patient_window, height=10, width=80)
        listbox.pack(pady=10)

        for index, patient in enumerate(self.patients):
            listbox.insert(tk.END, f"{index + 1}. {patient.get_first_name()} {patient.get_surname()} | Age: {patient.get_age()}")

        return listbox
    
    def assign_doctor_to_patient(self):
        # Clear the previous widgets and setup the frame for doctor assignment
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        tk.Label(self.center_frame, text="Assign Doctor to Patient", bg="#89CFF0").pack(pady=10)

        # Create the Treeview widget to display patient details in columns (Only once)
        self.treeview = ttk.Treeview(
            self.center_frame, 
            columns=("Patient Info", "Doctor", "Age", "Mobile", "Postcode", "Symptom"), 
            show="headings"
        )
        
        # Define the columns
        self.treeview.heading("Patient Info", text="Patient Info")
        self.treeview.heading("Doctor", text="Assigned Doctor")
        self.treeview.heading("Age", text="Age")
        self.treeview.heading("Mobile", text="Mobile")
        self.treeview.heading("Postcode", text="Postcode")
        self.treeview.heading("Symptom", text="Symptoms")

        # Set column widths (adjust as necessary)
        self.treeview.column("Patient Info", width=150)
        self.treeview.column("Doctor", width=200)
        self.treeview.column("Age", width=70)
        self.treeview.column("Mobile", width=130)
        self.treeview.column("Postcode", width=100)
        self.treeview.column("Symptom", width=200)

        # Insert the patient details into the Treeview using individual attributes
        for patient in self.patients:
            patient_name = patient.full_name()  # Call the full_name method for the patient's full name
            doctor = patient.get_doctor()
            
            # Check if the doctor is assigned or is "None" (string)
            if doctor != "None":
                doctor_name = f"{doctor.get_first_name()} {doctor.get_surname()}"
            else:
                doctor_name = "No Doctor Assigned"

            age = patient._Patient__age  # Access the private attribute for age
            mobile = patient._Patient__mobile  # Access the private attribute for mobile
            postcode = patient._Patient__postcode  # Access the private attribute for postcode
            symptom = getattr(patient, "symptom", "No Symptom Reported")  # Get the symptom if available

            # Insert each piece of information into the respective columns
            self.treeview.insert("", tk.END, values=(patient_name, doctor_name, age, mobile, postcode, symptom))

        # Pack the Treeview widget once all data is inserted
        self.treeview.pack(pady=10)

        # Symptom reporting section
        symptom_label = tk.Label(self.center_frame, text="Report Symptom:", bg="#89CFF0")
        symptom_label.pack(pady=(10, 0))
        self.symptom_entry = tk.Entry(self.center_frame, width=50)
        self.symptom_entry.pack(pady=5)
        report_button = tk.Button(
            self.center_frame, 
            text="Report Symptom", 
            command=self.report_symptom,
            bg="#1E90FF", 
            fg="white"
        )
        report_button.pack(pady=5)

        # Create a listbox to display doctors
        self.doctors_listbox = tk.Listbox(self.center_frame, height=5, width=40)
        for doctor in self.doctors:
            self.doctors_listbox.insert(tk.END, f"{doctor.get_first_name()} {doctor.get_surname()}")
        self.doctors_listbox.pack(pady=10)

        # Button to assign the selected doctor to the selected patient
        assign_button = tk.Button(
            self.center_frame,
            text="Assign Doctor",
            command=self.confirm_assign_doctor,
            bg="#1E90FF",
            fg="white",
            padx=20,
            pady=10
        )
        assign_button.pack(pady=10)

        # Back Button to return to the previous page (admin menu or patient management)
        back_button = tk.Button(
            self.center_frame,
            text="Back",
            command=self.show_admin_menu,
            bg="white",
            fg="black",
            padx=20,
            pady=10
        )
        back_button.pack(pady=10)

    def report_symptom(self):
        # Get the selected patient from the Treeview
        selected_patient_index = self.treeview.selection()
        if not selected_patient_index:
            messagebox.showerror("Error", "No patient selected.")
            return

        # Fetch the patient object based on the selected index
        selected_patient_info = self.treeview.item(selected_patient_index[0])['values'][0]
        selected_patient = None
        for patient in self.patients:
            if selected_patient_info == str(patient.full_name()):  # Compare full name
                selected_patient = patient
                break

        if not selected_patient:
            messagebox.showerror("Error", "Selected patient not found.")
            return

        # Get the symptom from the entry
        symptom = self.symptom_entry.get().strip()
        if not symptom:
            messagebox.showerror("Error", "Please enter a symptom.")
            return

        # Assign the symptom to the patient
        setattr(selected_patient, "symptom", symptom)

        # Retrieve the doctor's name without the specialty
        doctor = selected_patient.get_doctor()
        doctor_name = f"{doctor.get_first_name()} {doctor.get_surname()}" if doctor != "None" else "No Doctor Assigned"

        # Update the Treeview with the reported symptom
        self.treeview.item(selected_patient_index[0], values=(
            str(selected_patient.full_name()),  # Patient's full name
            doctor_name,                        # Doctor's name (without specialty)
            selected_patient._Patient__age,     # Patient's age
            selected_patient._Patient__mobile,  # Patient's mobile
            selected_patient._Patient__postcode, # Patient's postcode
            symptom                              # Reported symptom
        ))

        # Inform the user that the symptom has been reported
        messagebox.showinfo("Success", f"Symptom '{symptom}' has been reported for {selected_patient.full_name()}.")


    def confirm_assign_doctor(self):
        # Get the selected patient from the Treeview
        selected_patient_index = self.treeview.selection()
        if not selected_patient_index:
            messagebox.showerror("Error", "No patient selected.")
            return

        # Fetch the patient object based on the selected index
        selected_patient_info = self.treeview.item(selected_patient_index[0])['values'][0]
        selected_patient = None
        for patient in self.patients:
            if selected_patient_info == str(patient.full_name()):  # Compare full name
                selected_patient = patient
                break

        if not selected_patient:
            messagebox.showerror("Error", "Selected patient not found.")
            return

        # Check if the patient is already assigned to a doctor
        if selected_patient.get_doctor() != "None":  # If there's already an assigned doctor
            # Ask the user if they want to reassign the doctor
            response = messagebox.askyesno(
                "Reassign Doctor", 
                f"Patient {selected_patient.full_name()} is already assigned to a doctor. Would you like to reassign them?"
            )
            if not response:  # If the user selects 'No', stay on the current page
                return

        # Get the selected doctor from the Listbox
        selected_doctor_index = self.doctors_listbox.curselection()
        if not selected_doctor_index:
            messagebox.showerror("Error", "No doctor selected.")
            return

        # Fetch the doctor object based on the selected index
        selected_doctor_info = self.doctors_listbox.get(selected_doctor_index[0])
        selected_doctor_name = selected_doctor_info.split(' - ')[0]  # Extract doctor's full name from list
        selected_doctor = None
        for doctor in self.doctors:
            if f"{doctor.get_first_name()} {doctor.get_surname()}" == selected_doctor_name:
                selected_doctor = doctor
                break

        if not selected_doctor:
            messagebox.showerror("Error", "Selected doctor not found.")
            return

        # Link the selected doctor to the patient (reassign if needed)
        selected_patient.link(selected_doctor)

        # Retrieve the doctor's name without the specialty
        doctor_name_without_specialty = f"{selected_doctor.get_first_name()} {selected_doctor.get_surname()}"

        # Get the current symptom for the patient
        current_symptom = getattr(selected_patient, "symptom", "No Symptom Reported")

        # Update only the selected row with the doctor's name and preserve the symptom
        self.treeview.item(selected_patient_index[0], values=(
            str(selected_patient.full_name()),  # Patient's full name
            doctor_name_without_specialty,      # Doctor's name without specialty
            selected_patient._Patient__age,     # Patient's age
            selected_patient._Patient__mobile,  # Patient's mobile
            selected_patient._Patient__postcode, # Patient's postcode
            current_symptom                      # Preserve the symptom
        ))

        # Inform the user that the doctor has been assigned
        messagebox.showinfo("Success", f"Doctor {selected_doctor.full_name()} has been assigned to {selected_patient.full_name()}.")


    def update_admin_details(self):
        # Clear previous widgets
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        tk.Label(self.center_frame, text="Update Admin Details", bg="#89CFF0").pack(pady=10)

        # Display current details and provide edit buttons
        self.show_current_details()

    def show_current_details(self):
        # Clear previous widgets again just in case
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        current_username = tk.Label(self.center_frame, text=f"Username: {self.admin.get_username()}", bg="#89CFF0")
        current_username.pack(pady=5)

        edit_username_button = tk.Button(self.center_frame, text="Edit Username", command=self.update_username, bg="#1E90FF", fg="white", padx=20, pady=5)
        edit_username_button.pack(pady=5)

        current_password = tk.Label(self.center_frame, text=f"Password: {'*' * len(self.admin.get_password())}", bg="#89CFF0")
        current_password.pack(pady=5)

        edit_password_button = tk.Button(self.center_frame, text="Edit Password", command=self.update_password, bg="#1E90FF", fg="white", padx=20, pady=5)
        edit_password_button.pack(pady=5)

        current_address = tk.Label(self.center_frame, text=f"Address: {self.admin.get_postcode()}", bg="#89CFF0")
        current_address.pack(pady=5)

        edit_address_button = tk.Button(self.center_frame, text="Edit Address", command=self.update_address, bg="#1E90FF", fg="white", padx=20, pady=5)
        edit_address_button.pack(pady=5)

        # Back Button to return to the previous page
        back_button = tk.Button(self.center_frame, text="Back", command=self.show_admin_menu, bg="red", fg="white", padx=20, pady=10)
        back_button.pack(pady=10)

    def update_username(self):
        self.prompt_for_new_value("username")

    def update_password(self):
        self.prompt_for_new_value("password")

    def update_address(self):
        self.prompt_for_new_value("address")

    def prompt_for_new_value(self, field):
        # Clear previous widgets
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        # Request new input for the selected field
        prompt_label = tk.Label(self.center_frame, text=f"Enter new {field}:", bg="#89CFF0")
        prompt_label.pack(pady=5)

        new_value_entry = tk.Entry(self.center_frame)
        new_value_entry.pack(pady=5)

        confirm_label = tk.Label(self.center_frame, text=f"Confirm new {field}:", bg="#89CFF0")
        confirm_label.pack(pady=5)

        confirm_value_entry = tk.Entry(self.center_frame)
        confirm_value_entry.pack(pady=5)

        # Confirm button to update the value
        confirm_button = tk.Button(self.center_frame, text="Confirm", 
                                command=lambda: self.confirm_update(field, new_value_entry.get(), confirm_value_entry.get()),
                                bg="#1E90FF", fg="white", padx=20, pady=5)
        confirm_button.pack(pady=10)

        # Back Button to return to previous step
        back_button = tk.Button(self.center_frame, text="Back", command=self.show_current_details, bg="red", fg="white", padx=20, pady=10)
        back_button.pack(pady=10)

    def confirm_update(self, field, new_value, confirm_value):
        # Check if the entered values match and are not empty
        if not new_value or not confirm_value:
            messagebox.showerror("Error", f"{field.capitalize()} cannot be empty. Please enter a valid {field}.")
            return
        if new_value != confirm_value:
            messagebox.showerror("Error", f"The {field} does not match. Please try again.")
        else:
            # Update the admin details
            if field == "username":
                self.admin.update_username(new_value)
            elif field == "password":
                self.admin.update_password(new_value)
            elif field == "address":
                self.admin.update_address(new_value)

            messagebox.showinfo("Success", f"{field.capitalize()} updated successfully!")
            self.show_current_details()  # Return to the details page


    def logout(self):
        # Clear the current window and reset for login
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()
        self.create_widgets()  # Show the login screen again


    def save_update(self, entry_widget, field, update_function):
        new_value = entry_widget.get().strip()
        
        if new_value:
            update_function(new_value)
            messagebox.showinfo("Success", f"{field} updated.")
            self.update_admin_details()  # Go back to the details page with updated values
        else:
            messagebox.showerror("Error", f"{field} cannot be empty.")
    
    def show_management_report(self):
        """Display the management report page in the same window."""
        # Clear any existing widgets in the center frame
        for widget in self.center_frame.winfo_children():
            widget.pack_forget()

        # Generate the report content
        report = self.management_report(self.patients, self.doctors)

        # Create a Text widget to display the report
        report_text = tk.Text(self.center_frame, height=30, width=80, wrap="word", bg="#F4F4F4", font=("Arial", 12))
        report_text.pack(pady=10)

        # Insert the generated report into the Text widget
        report_text.insert(tk.END, report)

        # Make the Text widget non-editable
        report_text.config(state=tk.DISABLED)

        # Add a back button to return to the admin menu
        back_button = tk.Button(
            self.center_frame,
            text="Back to Menu",
            command=self.show_admin_menu,
            bg="white",
            fg="black",
            activebackground="gray",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5,
        )
        back_button.pack(pady=10)

    def generate_random_date(self):
        """Generate a random appointment date between 1 and 30 days from today."""
        today = datetime.today()
        random_days = random.randint(1, 30)
        random_date = today + timedelta(days=random_days)
        return random_date.strftime("%Y-%m-%d")

    def management_report(self, patients, doctors):
        output = "----- Management Report -----\n\n"
        patient_groups = {}
        for patient in patients:
            surname = patient.get_surname()
            if surname not in patient_groups:
                patient_groups[surname] = []
            patient_groups[surname].append(patient)

        doctor_groups = {}
        for doctor in doctors:
            surname = doctor.get_surname()
            if surname not in doctor_groups:
                doctor_groups[surname] = []
            doctor_groups[surname].append(doctor)

        output += "----- Patients -----\n\n"
        total_patients = len(patients)
        output += f"Total Patients: {total_patients}\n\n"
        for surname, group in patient_groups.items():
            output += f"Family: {surname}\n"
            for patient in group:
                output += f" {patient.full_name()} | Age: {patient.get_age()} | Mobile: {patient.get_mobile()}\n"
                output += f" Symptoms: {', '.join(patient.get_symptoms()) if patient.get_symptoms() else 'None'}\n"
                if patient.get_doctor() != "None":
                    output += f" Appointed to: Dr. {patient.get_doctor()} | Appointment Date: {self.generate_random_date()}\n"
                output += "\n"

        output += "----- Doctors -----\n"
        total_doctors = len(doctors)
        output += f"\nTotal Doctors: {total_doctors}\n\n"
        for surname, group in doctor_groups.items():
            output += f"Doctor Surname: {surname}\n"
            for doctor in group:
                assigned_patients = [p for p in patients if p.get_doctor() == doctor.full_name()]
                assigned_patients_count = len(assigned_patients)
                output += f" Dr. {doctor.full_name()} | Speciality: {doctor.get_speciality()}\n"
                output += f" Patients Assigned: {assigned_patients_count}\n"
                if assigned_patients_count > 0:
                    output += f" Assigned Patients: {', '.join(p.full_name() for p in assigned_patients)}\n"
                output += "\n"

        output += "----- Appointments per Month per Doctor -----\n\n"
        doctor_appointments_per_month = defaultdict(lambda: defaultdict(int))
        for patient in patients:
            if patient.get_doctor() != "None":
                doctor_name = patient.get_doctor()
                appointment_date = self.generate_random_date()
                month = datetime.strptime(appointment_date, '%Y-%m-%d').strftime('%B')
                doctor_appointments_per_month[doctor_name][month] += 1

        if not doctor_appointments_per_month:
            output += " There are no appointments scheduled.\n\n"
        else:
            for doctor_name, month_counts in doctor_appointments_per_month.items():
                output += f"Dr. {doctor_name}:\n"
                for month, count in month_counts.items():
                    output += f" {month}: {count} appointments\n"
                output += "\n"

        output += "----- Patients Per Illness -----\n\n"
        illness_type_count = defaultdict(int)
        for patient in patients:
            for symptom in patient.get_symptoms():
                illness_type_count[symptom] += 1

        if not illness_type_count:
            output += " There are no symptoms reported.\n\n"
        else:
            for illness, count in illness_type_count.items():
                output += f" {illness}: {count} patients\n\n"

        return output

    def quit_app(self):
        # Quit the application properly
        self.parent.quit()  # Ensure that the main window is destroyed
        self.parent.destroy()  # This will fully close the application

# Run the GUI application
if __name__ == "__main__":
    HospitalGUI()
