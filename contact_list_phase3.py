import json
import os
import re
import csv

FILE_NAME = "contacts.json"
CSV_NAME = "contacts_export.csv"


def load_contacts():
    """Load contacts from the JSON file; return an empty list if missing or damaged."""
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Data file is damaged. Starting with an empty list.")
    return []


def save_contacts(contacts):
    with open(FILE_NAME, "w") as f:
        json.dump(contacts, f, indent=4)


def valid_phone(phone):
    return re.fullmatch(r"[6-9]\d{9}", phone) is not None


def valid_email(email):
    return email == "" or re.fullmatch(
        r"[\w.+-]+@[\w-]+\.[\w.]+", email) is not None


def show_menu():
    print("\n===== Contact List Management System =====")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")


def find_matches(contacts, keyword):
    keyword = keyword.lower()
    return [c for c in contacts
            if keyword in c["name"].lower() or keyword in c["phone"]]


def add_contact(contacts):
    name = input("Enter name: ").strip()
    phone = input("Enter mobile number: ").strip()
    if not name or not phone:
        print("Name and mobile required.")
        return
    if not valid_phone(phone):
        print("Invalid mobile number. Enter 10 digits starting with 6-9.")
        return
    if any(c["phone"] == phone for c in contacts):
        print("Number already exists.")
        return
    email = input("Enter email (optional): ").strip()
    if not valid_email(email):
        print("Invalid email address.")
        return
    org = input("Enter organization (optional): ").strip()
    contacts.append({"name": name, "phone": phone,
                     "email": email, "organization": org})
    save_contacts(contacts)
    print("Contact added and saved successfully!")


def view_contacts(contacts):
    if not contacts:
        print("No contacts saved yet.")
        return
    ordered = sorted(contacts, key=lambda c: c["name"].lower())
    print(f"--- {len(ordered)} contact(s), sorted A-Z ---")
    for i, c in enumerate(ordered, 1):
        print(f"{i}. {c['name']} | {c['phone']} | {c['email']} | {c['organization']}")


def search_contact(contacts):
    keyword = input("Enter name or mobile number to search: ").strip()
    if not keyword:
        print("Nothing to search.")
        return
    matches = find_matches(contacts, keyword)
    if not matches:
        print("Contact not found.")
        return
    print(f"{len(matches)} match(es) found:")
    for i, c in enumerate(matches, 1):
        print(f"{i}. {c['name']} | {c['phone']} | {c['email']} | {c['organization']}")


def pick_contact(contacts, action):
    keyword = input(f"Enter name or mobile number to {action}: ").strip()
    matches = find_matches(contacts, keyword) if keyword else []
    if not matches:
        print("Contact not found.")
        return None
    if len(matches) > 1:
        print("More than one match. Please enter the full mobile number.")
        return None
    return matches[0]


def update_contact(contacts):
    c = pick_contact(contacts, "update")
    if c is None:
        return
    print("Press Enter to keep the old value.")
    name = input(f"Name [{c['name']}]: ").strip() or c["name"]
    phone = input(f"Mobile [{c['phone']}]: ").strip() or c["phone"]
    email = input(f"Email [{c['email']}]: ").strip() or c["email"]
    org = input(f"Organization [{c['organization']}]: ").strip() or c["organization"]
    if not valid_phone(phone):
        print("Invalid mobile number. Update cancelled.")
        return
    if phone != c["phone"] and any(x["phone"] == phone for x in contacts):
        print("Number already exists. Update cancelled.")
        return
    if not valid_email(email):
        print("Invalid email address. Update cancelled.")
        return
    c.update({"name": name, "phone": phone, "email": email, "organization": org})
    save_contacts(contacts)
    print("Contact updated successfully!")


def delete_contact(contacts):
    c = pick_contact(contacts, "delete")
    if c is None:
        return
    answer = input(f"Delete {c['name']}? (y/n): ").strip().lower()
    if answer == "y":
        contacts.remove(c)
        save_contacts(contacts)
        print("Contact deleted.")
    else:
        print("Delete cancelled.")


def export_csv(contacts):
    with open(CSV_NAME, "w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["name", "phone", "email", "organization"])
        writer.writeheader()
        writer.writerows(contacts)
    print(f"{len(contacts)} contact(s) exported to {CSV_NAME}")


def main():
    contacts = load_contacts()
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_contact(contacts)
        elif choice == "2":
            view_contacts(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            update_contact(contacts)
        elif choice == "5":
            delete_contact(contacts)
        elif choice == "6":
            export_csv(contacts)
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
