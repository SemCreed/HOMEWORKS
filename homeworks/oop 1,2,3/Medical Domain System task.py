from abc import ABC, abstractmethod
from typing import List
from datetime import date

# Abstract Base Classes
class MedicalProfessional(ABC):
    def __init__(self, name: str, license_number: str, years_experience: int):
        self.name = name
        self.license_number = license_number
        self.years_experience = years_experience
    
    @abstractmethod
    def diagnose(self, patient_name: str, symptoms: List[str]) -> str:
        pass
    
    def introduce(self) -> str:
        return f"I am {self.name}, a medical professional with {self.years_experience} years experience."


class HospitalStaff(ABC):
    def __init__(self, employee_id: str, department: str, shift: str):
        self.employee_id = employee_id
        self.department = department
        self.shift = shift
    
    @abstractmethod
    def perform_duty(self) -> str:
        pass
    
    def get_schedule(self) -> str:
        return f"Works in {self.department} department during {self.shift} shift"


# Concrete Classes
class Doctor(MedicalProfessional):
    def __init__(self, name: str, license_number: str, years_experience: int, 
                 specialization: str, consultation_fee: float):
        super().__init__(name, license_number, years_experience)
        self.specialization = specialization
        self.consultation_fee = consultation_fee
        self.patients_today = []
    
    def diagnose(self, patient_name: str, symptoms: List[str]) -> str:
        self.patients_today.append(patient_name)
        diagnosis = f"Based on symptoms {symptoms}, preliminary diagnosis for {patient_name}"
        
        if "fever" in symptoms and "cough" in symptoms:
            return diagnosis + ": Likely respiratory infection"
        elif "headache" in symptoms and "nausea" in symptoms:
            return diagnosis + ": Possible migraine"
        else:
            return diagnosis + ": Requires further tests"
    
    def prescribe_medication(self, patient_name: str, medication: str) -> str:
        return f"Prescribed {medication} for {patient_name}"
    
    def get_credentials(self) -> str:
        return f"Dr. {self.name}, {self.specialization} specialist"


class Nurse(MedicalProfessional, HospitalStaff):
    def __init__(self, name: str, license_number: str, years_experience: int,
                 employee_id: str, department: str, shift: str, 
                 certifications: List[str]):
        # Multiple inheritance initialization using super()
        MedicalProfessional.__init__(self, name, license_number, years_experience)
        HospitalStaff.__init__(self, employee_id, department, shift)
        self.certifications = certifications
        self.tasks_completed = 0
    
    def diagnose(self, patient_name: str, symptoms: List[str]) -> str:
        return f"Nurse assessment for {patient_name}: Monitoring vital signs for symptoms {symptoms}"
    
    def perform_duty(self) -> str:
        self.tasks_completed += 1
        return f"Performed nursing duties in {self.department}"
    
    def administer_medication(self, patient_name: str, medication: str) -> str:
        return f"Administered {medication} to {patient_name}"
    
    def check_vitals(self, patient_name: str) -> str:
        return f"Checked vitals for {patient_name}: BP 120/80, HR 72, Temp 98.6°F"


class Surgeon(Doctor):
    def __init__(self, name: str, license_number: str, years_experience: int,
                 specialization: str, consultation_fee: float, 
                 surgeries_performed: int):
        super().__init__(name, license_number, years_experience, specialization, consultation_fee)
        self.surgeries_performed = surgeries_performed
        self.schedule_surgeries = []
    
    def diagnose(self, patient_name: str, symptoms: List[str]) -> str:
        if "severe pain" in symptoms or "bleeding" in symptoms:
            return f"Emergency surgical consultation needed for {patient_name}"
        return super().diagnose(patient_name, symptoms)
    
    def perform_surgery(self, patient_name: str, procedure: str) -> str:
        self.surgeries_performed += 1
        self.schedule_surgeries.append((patient_name, procedure, date.today()))
        return f"Performed {procedure} on {patient_name}. Total surgeries: {self.surgeries_performed}"
    
    def get_surgery_stats(self) -> str:
        return f"Surgeries performed: {self.surgeries_performed}"


class Pharmacist(HospitalStaff):
    def __init__(self, employee_id: str, department: str, shift: str,
                 name: str, license_number: str, pharmacy_type: str):
        super().__init__(employee_id, department, shift)
        self.name = name
        self.license_number = license_number
        self.pharmacy_type = pharmacy_type
        self.medications_dispensed = []
    
    def perform_duty(self) -> str:
        return f"Dispensing medications in {self.pharmacy_type} pharmacy"
    
    def dispense_medication(self, patient_name: str, medication: str, dosage: str) -> str:
        self.medications_dispensed.append((patient_name, medication, dosage))
        return f"Dispensed {medication} ({dosage}) to {patient_name}"
    
    def check_interactions(self, medication1: str, medication2: str) -> str:
        interactions = {
            ("Warfarin", "Aspirin"): "High risk of bleeding",
            ("Statins", "Grapefruit"): "Increased side effects"
        }
        
        key = (medication1, medication2)
        reverse_key = (medication2, medication1)
        
        if key in interactions:
            return interactions[key]
        elif reverse_key in interactions:
            return interactions[reverse_key]
        else:
            return "No known dangerous interactions"


class Patient:
    def __init__(self, name: str, age: int, patient_id: str, 
                 blood_type: str, allergies: List[str]):
        self.name = name
        self.age = age
        self.patient_id = patient_id
        self.blood_type = blood_type
        self.allergies = allergies
        self.medical_history = []
    
    def add_record(self, condition: str, date: date) -> None:
        self.medical_history.append((condition, date))
    
    def get_medical_summary(self) -> str:
        return f"Patient {self.name} (ID: {self.patient_id}), Age: {self.age}, Blood Type: {self.blood_type}"
    
    def check_allergy(self, medication: str) -> bool:
        return medication in self.allergies


class MedicalEquipment:
    def __init__(self, equipment_id: str, name: str, department: str,
                 maintenance_date: date, status: str):
        self.equipment_id = equipment_id
        self.name = name
        self.department = department
        self.maintenance_date = maintenance_date
        self.status = status
        self.usage_count = 0
    
    def use_equipment(self, patient_name: str) -> str:
        self.usage_count += 1
        return f"Used {self.name} for {patient_name}. Total uses: {self.usage_count}"
    
    def schedule_maintenance(self, new_date: date) -> str:
        self.maintenance_date = new_date
        return f"Scheduled maintenance for {self.name} on {new_date}"
    
    def get_equipment_info(self) -> str:
        return f"{self.name} (ID: {self.equipment_id}) in {self.department} - Status: {self.status}"


# Demonstration of polymorphism
def demonstrate_polymorphism():
    print("=== Medical System Demo ===\n")
    
    # Create different medical professionals
    doctor = Doctor("Alice Chen", "MED12345", 10, "Cardiology", 200.0)
    nurse = Nurse("Bob Wilson", "NUR67890", 5, "EMP001", "Emergency", "Night", ["ACLS", "PALS"])
    surgeon = Surgeon("Carol Davis", "SUR54321", 15, "Neurosurgery", 500.0, 350)
    
    # Polymorphism: same method, different implementations
    medical_staff = [doctor, nurse, surgeon]
    
    for staff in medical_staff:
        print(f"{staff.__class__.__name__}: {staff.introduce()}")
        print(f"Diagnosis: {staff.diagnose('John Patient', ['fever', 'cough'])}")
        print("-" * 50)
    
    # Multiple inheritance demonstration
    print("\n=== Multiple Inheritance (Nurse) ===")
    print(f"Nurse as MedicalProfessional: {nurse.introduce()}")
    print(f"Nurse as HospitalStaff: {nurse.get_schedule()}")
    print(f"Nurse duty: {nurse.perform_duty()}")
    
    # Super usage demonstration
    print("\n=== Super() Usage ===")
    print(f"Surgeon credentials: {surgeon.get_credentials()}")
    
    # Hospital staff demonstration
    print("\n=== Hospital Staff ===")
    pharmacist = Pharmacist("EMP002", "Pharmacy", "Day", 
                           "David Miller", "PHA98765", "Hospital")
    print(pharmacist.perform_duty())
    print(pharmacist.dispense_medication("John Patient", "Amoxicillin", "500mg TID"))
    print(f"Drug interaction check: {pharmacist.check_interactions('Warfarin', 'Aspirin')}")
    
    # Patient demonstration
    print("\n=== Patient Management ===")
    patient = Patient("Emma Johnson", 45, "PAT00123", "O+", ["Penicillin", "Sulfa"])
    patient.add_record("Hypertension", date(2020, 3, 15))
    print(patient.get_medical_summary())
    print(f"Allergic to Penicillin? {patient.check_allergy('Penicillin')}")
    
    # Medical equipment
    print("\n=== Medical Equipment ===")
    xray_machine = MedicalEquipment("EQP001", "X-Ray Machine", "Radiology", 
                                    date(2023, 12, 1), "Operational")
    print(xray_machine.get_equipment_info())
    print(xray_machine.use_equipment("Emma Johnson"))


if __name__ == "__main__":
    demonstrate_polymorphism()
