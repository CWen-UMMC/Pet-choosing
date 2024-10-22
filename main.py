# Changhong Wen
# Purpose: This is Pet chooser assignment
# Create
# Read
# Update
# Delete
#


import pymysql.cursors
from creds import *
from pets import Pets

def fetch_pets(cursor):
    """Fetch all pets from the database and return a list of Pets objects."""
    sqlSelect = """
    SELECT
        pets.id,
        pets.name AS pet_name,
        pets.age,
        types.animal_type,
        owners.name AS owner_name
    FROM
        pets
    JOIN
        types ON pets.animal_type_id = types.id
    JOIN
        owners ON pets.owner_id = owners.id;
    """
    cursor.execute(sqlSelect)
    pets_list = []
    for row in cursor:
        pet = Pets(
            pet_id=row['id'],
            name=row['pet_name'],
            species=row['animal_type'],
            age=row['age'],
            owner=row['owner_name']
        )
        pets_list.append(pet)
    return pets_list

def display_pets(pets):
    """Display a list of pet names for selection."""
    print("\nPlease choose a pet from the list below:\n")
    for index, pet in enumerate(pets, start=1):
        print(f"[{index}] {pet.name}")
    print("\n[Q] Quit")

def get_user_choice():
    """Get user input and return the choice."""
    choice = input("\nChoice: ").strip()
    return choice

def main():
    print("Starting the program...")

    # Connect to the database
    try:
        myConnection = pymysql.connect(
            host=hostname,
            user=username,
            password=password,
            db=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Successfully connected to the database.")
    except Exception as e:
        print("An error has occurred while connecting to the database.")
        print(f"Error: {e}")
        exit()

    # Fetch data and create pet objects
    try:
        with myConnection.cursor() as cursor:
            pets = fetch_pets(cursor)
            if not pets:
                print("No pets found in the database.")
                myConnection.close()
                exit()
            print("Fetched pet data successfully.")
    except Exception as e:
        print("An error occurred while fetching data from the database.")
        print(f"Error: {e}")
        myConnection.close()
        exit()

    # Main loop for user interaction
    try:
        while True:
            display_pets(pets)
            choice = get_user_choice()

            if choice.lower() == 'q':
                print("Goodbye!")
                break

            try:
                choice_index = int(choice) - 1
                if 0 <= choice_index < len(pets):
                    selected_pet = pets[choice_index]
                    print(f"\nYou have chosen {selected_pet}\n")
                    input("Press [ENTER] to continue.")
                else:
                    print("\nInvalid choice. Please select a valid number from the list or 'Q' to quit.")
            except ValueError:
                print("\nInvalid choice. Please enter a number corresponding to a pet or 'Q' to quit.")
            except Exception as e:
                print("\nAn unexpected error occurred while processing your choice.")
                print(f"Error: {e}")
    except Exception as e:
        print("\nAn unexpected error occurred during the program execution.")
        print(f"Error: {e}")
    finally:
        try:
            myConnection.close()
            print("Connection closed.")
        except pymysql.MySQLError:
            print("The connection was already closed. No further action is needed.")
        except Exception as e:
            print(f"An unexpected error occurred while closing the connection: {e}")

if __name__ == "__main__":
    main()
