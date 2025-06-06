import datetime

from starlette.responses import JSONResponse

from patient.services.database import db_manager
from patient.services.exceptions import response_structure


class PatientsManager:

    def __init__(self, session, details=None):
        self.patients = db_manager.get_class("patients")
        self.contacts = db_manager.get_class("contact_details")
        self.session = session

        if details is not None:
            self.first_name = details.get("first_name", None)
            self.middle_name = details.get("middle_name", None)
            self.last_name = details.get("last_name", None)
            self.dob = details.get("date_of_birth", None)
            self.gender = details.get("gender", None)
            self.blood_type = details.get("blood_type", None)

            self.phone_number = (
                details["contacts"]["phone_number"]
                if details["contacts"]["phone_number"]
                else None
            )
            self.email = (
                details["contacts"]["email"] if details["contacts"]["email"] else None
            )
            self.address_1 = (
                details["contacts"]["address_1"]
                if details["contacts"]["address_1"]
                else None
            )
            self.address_2 = (
                details["contacts"]["address_2"]
                if details["contacts"]["address_2"]
                else None
            )
            self.patient_id = details["patient_id"] if details["patient_id"] else None

    async def get_patients_details(self) -> JSONResponse:
        """

        :return:
        """
        try:
            patients = self.session.query(self.patients).filter(active=True).all()

            if not patients:
                return response_structure(404, "No patient details were found")

            return patients

        except Exception as e:
            return response_structure(404, f"Something went wrong : {e}")

    async def add_patient_details(self):
        """

        :return:
        """
        try:

            patients = self.patients(
                first_name=self.first_name,
                middle_name=self.middle_name,
                last_name=self.last_name,
                date_of_birth=self.dob,
                gender=self.gender,
                blood_type=self.blood_type,
            )

            # Add and commit the patient to the session
            self.session.add(patients)
            self.session.flush()

            # Get the ID of the newly inserted patient
            inserted_id = patients.patient_id
            contacts = self.contacts(
                patient_id=inserted_id,
                phone_number=self.phone_number,
                email=self.email,
                address_1=self.address_1,
                address_2=self.address_2,
            )

            self.session.add(contacts)
            self.session.commit()

            return response_structure(
                200, "Successfully added record", {"patient_id": inserted_id}
            )

        except Exception as e:
            self.session.rollback()
            error_message = str(e).split("\n")[0].split(") ")[1].replace('"', "")
            return response_structure(404, f"Something went wrong : {error_message}")

    async def update_patients_details(self, admin_id: int):
        """

        :param admin_id
        :return:
        """
        # Update the patient's details
        try:
            if self.patient_id:
                # Update the patient's details
                updated_patient_rows = (
                    self.session.query(self.patients)
                    .filter(self.patients.patient_id == self.patient_id and self.patient_id.active == True)
                    .update(
                        {
                            "first_name": self.first_name,
                            "middle_name": self.middle_name,
                            "last_name": self.last_name,
                            "date_of_birth": self.dob,
                            "gender": self.gender,
                            "blood_type": self.blood_type,
                            "updated_at": datetime.datetime.now(),
                            "updated_by": admin_id
                        },
                        synchronize_session="fetch",
                    )
                )

                # Update the contact details
                updated_contact_rows = (
                    self.session.query(self.contacts)
                    .filter(self.contacts.patient_id == self.patient_id, self.contacts.active == True)
                    .update(
                        {
                            "phone_number": self.phone_number,
                            "email": self.email,
                            "address_1": self.address_1,
                            "address_2": self.address_2,
                            "updated_by": admin_id,
                            "updated_at": datetime.datetime.now()
                        },
                        synchronize_session="fetch",
                    )
                )

                # Commit the transaction only if both updates are successful
                if updated_patient_rows > 0 or updated_contact_rows > 0:
                    self.session.commit()
                    return response_structure(
                        200,
                        f"Updated {updated_patient_rows} patient record(s) and {updated_contact_rows} contact record(s).",
                    )

                else:
                    return response_structure(404, "No records were found")

        except Exception as e:
            self.session.rollback()
            error_message = str(e).split("\n")[0].split(") ")[1].replace('"', "")
            return response_structure(404, f"Something went wrong : {error_message}")

    async def delete_patient_record(self, patient_id: int, admin_id: int):
        try:
            print(patient_id, admin_id)
            if patient_id and admin_id:
                # Update the patient's details
                updated_patient_rows = (
                    self.session.query(self.patients)
                    .filter(self.patients.patient_id == patient_id and self.patients.active == True)
                    .update(
                        {
                            "active": False,
                            "updated_at": datetime.datetime.now(),
                            "updated_by": admin_id
                        },
                        synchronize_session="fetch",
                    )
                )
                print(patient_id, admin_id)
                # Update the contact details
                updated_contact_rows = (
                    self.session.query(self.contacts)
                    .filter(self.contacts.patient_id == patient_id, self.contacts.active == True)
                    .update(
                        {
                            "active": False,
                            "updated_by": admin_id,
                            "updated_at": datetime.datetime.now()
                        },
                        synchronize_session="fetch",
                    )
                )
                print(patient_id, admin_id)
                # Commit the transaction only if both updates are successful
                if updated_patient_rows > 0 or updated_contact_rows > 0:
                    self.session.commit()
                    return response_structure(
                        200,
                        f"Updated {updated_patient_rows} patient record(s) and {updated_contact_rows} contact record(s).",
                    )

                else:
                    return response_structure(404, "No records were found")

            else:
                return response_structure(404, "Please pass Admin ID and Patient ID")


        except Exception as e:
            self.session.rollback()
            error_message = str(e).split("\n")[0].split(") ")[1].replace('"', "")
            return response_structure(404, f"Something went wrong : {error_message}")

