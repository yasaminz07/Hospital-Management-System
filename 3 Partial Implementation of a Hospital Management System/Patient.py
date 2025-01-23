class Patient:
    """Patient class"""

    def __init__(self, first_name, surname, age, mobile, postcode, doctor="None", symptoms=None):
        if symptoms is None:
            symptoms = []  # Default empty list for symptoms
        self.__symptoms = symptoms
        self.__first_name = first_name
        self.__surname = surname
        self.__age = age
        self.__mobile = mobile
        self.__postcode = postcode
        self.__doctor = doctor  # Default "None" if no doctor is assigned
    
    def assign_doctor(self, doctor):
        """Assigns a doctor to the patient."""
        self.__doctor = doctor.full_name()  # Or you could store the entire doctor object if needed.
   
    def replace_symptoms(self, symptoms):
        """
        Adds symptoms to the patient's symptom list.
        Args:
            symptoms (str): A string of symptoms separated by '
        """
        self.__symptoms = symptoms.split(", ")

    def remove_all_symptoms(self):
        """Removes the list of symptoms of all data"""
        self.__symptoms = []
    
    def full_name(self) :
        """full name is first_name and surname"""
        return f"{self.__first_name} {self.__surname}"
        
    def get_first_name(self):
        return self.__first_name
    
    def get_surname(self):
        return self.__surname

    def get_doctor(self) :
        """Returns the doctor of the patient """
        return self.__doctor
        

    def link(self, doctor):
        """Assign the doctor object to the patient"""
        self.__doctor = doctor  # store the actual doctor object, not just the doctor's name

    def print_symptoms(self):
        """Prints all the symptoms."""
        if self.__symptoms:
            print(f"Symptoms: {', '.join(self.__symptoms)}")
        else:
            print("No Patient symptoms recorded")
    
    def add_symptom(self, symptom):
        """
        Adds a symptom to the patient's symptom list.
        Args:
            symptom (str): The symptom to add.
        """
        self.__symptoms.append(symptom)

    def get_symptoms(self):
        """Returns the list of symptoms."""
        return self.__symptoms
    
    def get_age(self):
        """Returns the patient's age."""
        return self.__age

    def get_mobile(self):
        """Returns the patient's mobile number."""
        return self.__mobile

    def get_postcode(self):
        """Returns the patient's postcode."""
        return self.__postcode

    def __str__(self):
        doctor = self.__doctor if self.__doctor != "None" else ""  # Leave empty if no doctor
        symptoms = ', '.join(self.__symptoms) if self.__symptoms else 'None'
        return f'{self.full_name():^29}|{self.__doctor:^30}|{self.__age:^5}|{self.__mobile:^15}|{self.__postcode:^9}|{symptoms:^20}|'
    
    def text(self):
        with open("database.txt", "a") as file:  # Change to 'a' mode to append
            symptoms = ','.join(self.__symptoms) if self.__symptoms else 'None'
            file.write(f'{self.__first_name}:{self.__surname}:{self.__age}:{self.__mobile}:{self.__postcode}:{self.__doctor}:{symptoms}\n')
    