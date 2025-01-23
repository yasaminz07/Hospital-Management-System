class Doctor:
    """A class that deals with the Doctor operations"""

    def __init__(self, first_name, surname, speciality):
        """
        Args:
            first_name (string): First name
            surname (string): Surname
            speciality (string): Doctor's speciality
        """
        self.__first_name = first_name
        self.__surname = surname
        self.__speciality = speciality
        self.__patients = []

    def full_name(self):
        """Returns the full name of the doctor."""
        return f"{self.__first_name} {self.__surname}"

    # Getter and Setter for First Name
    def get_first_name(self):
        return self.__first_name

    def set_first_name(self, new_first_name):
        if new_first_name.strip():  # Validation to ensure the name is not empty
            self.__first_name = new_first_name
        else:
            raise ValueError("First name cannot be empty.")

    # Getter and Setter for Surname
    def get_surname(self):
        return self.__surname

    def set_surname(self, new_surname):
        if new_surname.strip():  # Validation to ensure the surname is not empty
            self.__surname = new_surname
        else:
            raise ValueError("Surname cannot be empty.")

    # Getter and Setter for Speciality
    def get_speciality(self):
        return self.__speciality

    def set_speciality(self, new_speciality):
        if new_speciality.strip():  # Validation to ensure the speciality is not empty
            self.__speciality = new_speciality
        else:
            raise ValueError("Speciality cannot be empty.")

    def add_patient(self, patient):
        """Adds a patient to the doctor's list of patients."""
        self.__patients.append(patient)
    
    def remove_patient(self, patient):
        """Removes a patient from the doctor's list of patients."""
        if patient in self.__patients:
            self.__patients.remove(patient)

    # Get the list of patients assigned to the doctor
    def get_patients(self):
        """Returns the list of patients assigned to the doctor."""
        return self.__patients

    # Check if a patient is already assigned to this doctor
    def has_patient(self, patient):
        """Returns True if the patient is assigned to this doctor, else False."""
        return patient in self.__patients

    def __str__(self):
        """String representation of the doctor."""
        return f'{self.full_name():^29}|{self.__speciality:^15}'