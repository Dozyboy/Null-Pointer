import json
import sqlite3
from pathlib import Path
from threading import RLock

from app.modules.patients.schemas import PatientProfile


class SqlitePatientRepository:
    """Lưu hồ sơ bệnh nhân giả lập trong cơ sở dữ liệu SQLite dùng chung."""

    def __init__(self, database_path: Path) -> None:
        self._database_path = database_path
        self._lock = RLock()
        self._database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS patients (
                    id TEXT PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    date_of_birth TEXT NOT NULL,
                    gender TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT,
                    national_id TEXT NOT NULL UNIQUE,
                    health_insurance_number TEXT NOT NULL UNIQUE,
                    address TEXT NOT NULL,
                    emergency_contact_name TEXT NOT NULL,
                    emergency_contact_phone TEXT NOT NULL,
                    blood_type TEXT NOT NULL,
                    allergies_json TEXT NOT NULL,
                    chronic_conditions_json TEXT NOT NULL,
                    mobility_support INTEGER NOT NULL DEFAULT 0,
                    visual_support INTEGER NOT NULL DEFAULT 0,
                    hearing_support INTEGER NOT NULL DEFAULT 0,
                    current_encounter_id TEXT NOT NULL,
                    attending_doctor_name TEXT NOT NULL,
                    doctor_room_code TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_patients_full_name
                ON patients(full_name)
                """
            )

    def seed(self, patients: list[PatientProfile]) -> None:
        with self._lock, self._connect() as connection:
            connection.executemany(
                """
                INSERT OR IGNORE INTO patients (
                    id, full_name, date_of_birth, gender, phone, email,
                    national_id, health_insurance_number, address,
                    emergency_contact_name, emergency_contact_phone, blood_type,
                    allergies_json, chronic_conditions_json, mobility_support,
                    visual_support, hearing_support, current_encounter_id,
                    attending_doctor_name, doctor_room_code, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [self._to_parameters(patient) for patient in patients],
            )

    def list_all(self) -> list[PatientProfile]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM patients ORDER BY full_name COLLATE NOCASE, id"
            ).fetchall()
        return [self._to_entity(row) for row in rows]

    def get(self, patient_id: str) -> PatientProfile | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM patients WHERE id = ?",
                (patient_id,),
            ).fetchone()
        return self._to_entity(row) if row is not None else None

    @staticmethod
    def _to_parameters(patient: PatientProfile) -> tuple[object, ...]:
        return (
            patient.id,
            patient.full_name,
            patient.date_of_birth.isoformat(),
            patient.gender.value,
            patient.phone,
            patient.email,
            patient.national_id,
            patient.health_insurance_number,
            patient.address,
            patient.emergency_contact_name,
            patient.emergency_contact_phone,
            patient.blood_type,
            json.dumps(patient.allergies, ensure_ascii=False),
            json.dumps(patient.chronic_conditions, ensure_ascii=False),
            int(patient.mobility_support),
            int(patient.visual_support),
            int(patient.hearing_support),
            patient.current_encounter_id,
            patient.attending_doctor_name,
            patient.doctor_room_code,
            patient.created_at.isoformat(),
        )
    @staticmethod
    def _to_entity(row: sqlite3.Row) -> PatientProfile:
        return PatientProfile(
            id=row["id"],
            full_name=row["full_name"],
            date_of_birth=row["date_of_birth"],
            gender=row["gender"],
            phone=row["phone"],
            email=row["email"],
            national_id=row["national_id"],
            health_insurance_number=row["health_insurance_number"],
            address=row["address"],
            emergency_contact_name=row["emergency_contact_name"],
            emergency_contact_phone=row["emergency_contact_phone"],
            blood_type=row["blood_type"],
            allergies=json.loads(row["allergies_json"]),
            chronic_conditions=json.loads(row["chronic_conditions_json"]),
            mobility_support=bool(row["mobility_support"]),
            visual_support=bool(row["visual_support"]),
            hearing_support=bool(row["hearing_support"]),
            current_encounter_id=row["current_encounter_id"],
            attending_doctor_name=row["attending_doctor_name"],
            doctor_room_code=row["doctor_room_code"],
            created_at=row["created_at"],
        )
