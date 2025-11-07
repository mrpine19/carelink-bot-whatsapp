# Integração com o sistema existente de Java
class AppointmentManager:
    def __init__(self):
        # Aqui viria a conexão com o sistema Java existente
        self.appointments = {
            "12345": [
                {"date": "2024-01-15", "time": "14:30", "doctor": "Dr. Silva", "specialty": "Cardiologia"},
                {"date": "2024-01-20", "time": "10:00", "doctor": "Dra. Costa", "specialty": "Dermatologia"}
            ]
        }
    
    def get_next_appointment(self, patient_id):
        # Simulação - na prática, integraria com o sistema Java
        if patient_id in self.appointments and self.appointments[patient_id]:
            return self.appointments[patient_id][0]
        return None
    
    def confirm_appointment(self, patient_id, appointment_date):
        # Lógica para confirmar consulta
        return True
    
    def cancel_appointment(self, patient_id, appointment_date):
        # Lógica para cancelar consulta
        return True