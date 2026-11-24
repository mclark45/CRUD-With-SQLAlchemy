from sqlalchemy import create_engine, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from typing import Optional
from datetime import datetime

engine = create_engine("sqlite:///contacts.db", echo=False)

class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    favorite: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        star = "★" if self.favorite else " "
        return (
            f"[{star}] {self.first_name} "
            f"{self.last_name} | "
            f"{self.email} | "
            f"Phone: {self.phone}"
        )

# Create table if it doesn't exist
Base.metadata.create_all(engine)

def add_contact(first_name, last_name, email, phone=None):
    with Session(engine) as session:

        existing = session.query(Contact).filter_by(email=email).first()

        if existing:
            print(f"Contact already exists: {email}")
            return

        contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
        )

        session.add(contact)
        session.commit()

        print(f"Added: {contact}")


def list_contacts():
    with Session(engine) as session:

        contacts = (session.query(Contact).order_by(Contact.last_name).all())

        print("\n=== CONTACTS ===")

        for contact in contacts:
            print(contact)

        return contacts


def find_contact(email):
    with Session(engine) as session:

        contact = (
            session.query(Contact)
            .filter_by(email=email)
            .first()
        )

        if contact:
            print(f"Found: {contact}")
        else:
            print("Contact not found.")

        return contact


def update_phone(email, new_phone):
    with Session(engine) as session:

        contact = (
            session.query(Contact)
            .filter_by(email=email)
            .first()
        )

        if not contact:
            print("Contact not found.")
            return

        contact.phone = new_phone

        session.commit()

        print(
            f"Updated phone for {contact.first_name}: "
            f"{new_phone}"
        )


def toggle_favorite(email):
    with Session(engine) as session:

        contact = (
            session.query(Contact)
            .filter_by(email=email)
            .first()
        )

        if not contact:
            print("Contact not found.")
            return

        contact.favorite = not contact.favorite

        session.commit()

        print(
            f"{contact.first_name} favorite status "
            f"set to {contact.favorite}"
        )


def delete_contact(email):
    with Session(engine) as session:

        contact = (
            session.query(Contact)
            .filter_by(email=email)
            .first()
        )

        if not contact:
            print("Contact not found.")
            return

        session.delete(contact)
        session.commit()

        print(f"Deleted: {email}")


# -----------------------------
# DEMONSTRATION
# -----------------------------

print("=== ADDING CONTACTS ===")

add_contact(
    "John",
    "Smith",
    "john@example.com",
    "555-1111"
)

add_contact(
    "Sara",
    "Wilson",
    "sara@example.com",
    "555-2222"
)

add_contact(
    "Mike",
    "Brown",
    "mike@example.com",
    "555-3333"
)

add_contact(
    "Emma",
    "Davis",
    "emma@example.com"
)

add_contact(
    "Alex",
    "Taylor",
    "alex@example.com",
    "555-4444"
)


print("\n=== LIST CONTACTS ===")
list_contacts()

print("\n=== FIND CONTACT ===")
find_contact("mike@example.com")

print("\n=== UPDATE PHONE ===")
update_phone(
    "emma@example.com",
    "555-9999"
)

print("\n=== TOGGLE FAVORITES ===")
toggle_favorite("john@example.com")
toggle_favorite("emma@example.com")

print("\n=== DELETE CONTACT ===")
delete_contact("sara@example.com")

print("\n=== FINAL CONTACT LIST ===")
list_contacts()