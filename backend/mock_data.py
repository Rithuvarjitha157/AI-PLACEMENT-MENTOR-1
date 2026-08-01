"""
Firebase Firestore Service.

Simple structure:
  students/{student_id}
      - profile fields
      - resume_analysis (map)
      - placement_readiness (map)
      - roadmap (map)
      - chat_history (array of {role, message, timestamp})
      - recruiter_simulations (array of maps)

If USE_MOCK_DB=true (or firebase-admin/credentials are unavailable), falls
back to a simple in-memory dict store — keeps the whole app runnable with
zero Firebase setup during a hackathon demo.
"""
import os
import uuid
import time

USE_MOCK_DB = os.getenv("USE_MOCK_DB", "true").lower() == "true"

_db = None
_mock_store = {}  # student_id -> dict


def _init_firestore():
    global _db
    if _db is not None:
        return _db
    import firebase_admin
    from firebase_admin import credentials, firestore

    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_credentials.json")
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    _db = firestore.client()
    return _db


def _get_client():
    if USE_MOCK_DB:
        return None
    try:
        return _init_firestore()
    except Exception as e:
        print(f"[firebase_service] Firebase init failed, falling back to in-memory store: {e}")
        return None


def create_student(profile: dict) -> str:
    student_id = str(uuid.uuid4())[:8]
    profile = dict(profile)
    profile["student_id"] = student_id
    profile["created_at"] = time.time()

    client = _get_client()
    if client is None:
        _mock_store[student_id] = profile
    else:
        client.collection("students").document(student_id).set(profile)
    return student_id


def get_student(student_id: str) -> dict:
    client = _get_client()
    if client is None:
        return _mock_store.get(student_id)
    doc = client.collection("students").document(student_id).get()
    return doc.to_dict() if doc.exists else None


def update_student(student_id: str, data: dict):
    client = _get_client()
    if client is None:
        if student_id not in _mock_store:
            _mock_store[student_id] = {"student_id": student_id}
        _mock_store[student_id].update(data)
    else:
        client.collection("students").document(student_id).set(data, merge=True)


def append_chat_message(student_id: str, role: str, message: str):
    entry = {"role": role, "message": message, "timestamp": time.time()}
    client = _get_client()
    if client is None:
        student = _mock_store.setdefault(student_id, {"student_id": student_id})
        student.setdefault("chat_history", []).append(entry)
    else:
        doc_ref = client.collection("students").document(student_id)
        doc_ref.set({"chat_history": firestore_array_union([entry])}, merge=True)


def firestore_array_union(values):
    """Lazily import firestore only when actually using real Firestore."""
    from firebase_admin import firestore
    return firestore.ArrayUnion(values)


def get_chat_history(student_id: str) -> list:
    student = get_student(student_id)
    if not student:
        return []
    return student.get("chat_history", [])


def append_recruiter_simulation(student_id: str, simulation: dict):
    simulation = dict(simulation)
    simulation["timestamp"] = time.time()
    client = _get_client()
    if client is None:
        student = _mock_store.setdefault(student_id, {"student_id": student_id})
        student.setdefault("recruiter_simulations", []).append(simulation)
    else:
        doc_ref = client.collection("students").document(student_id)
        doc_ref.set({"recruiter_simulations": firestore_array_union([simulation])}, merge=True)
