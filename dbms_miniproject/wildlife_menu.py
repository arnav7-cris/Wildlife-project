# wildlife_menu.py
import mysql.connector
from mysql.connector import Error

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',  # change this
    'database': 'WildlifeDB'
}

def connect():
    return mysql.connector.connect(**config)

def list_species(conn):
    cur = conn.cursor()
    cur.execute("SELECT SpeciesID, Name, Category, Status FROM Species ORDER BY Name")
    for row in cur.fetchall():
        print(row)
    cur.close()

def add_sighting(conn):
    cur = conn.cursor()
    print("Enter SpeciesID, LocationID, RangerID, Date (YYYY-MM-DD), Quantity, Notes")
    sp = input("SpeciesID: ").strip()
    loc = input("LocationID: ").strip()
    rg = input("RangerID: ").strip()
    date = input("DateSeen (YYYY-MM-DD): ").strip()
    qty = input("Quantity: ").strip() or "1"
    notes = input("Notes: ").strip()
    sql = ("INSERT INTO Sightings (SpeciesID, LocationID, RangerID, DateSeen, Quantity, Notes) "
           "VALUES (%s,%s,%s,%s,%s,%s)")
    cur.execute(sql, (sp, loc, rg, date, qty, notes))
    conn.commit()
    print("Inserted. If species is endangered, an alert row will be created by trigger.")
    cur.close()

def top_species(conn):
    cur = conn.cursor()
    cur.execute("""
      SELECT s.Name, SUM(si.Quantity) AS TotalSeen
      FROM Sightings si JOIN Species s ON si.SpeciesID = s.SpeciesID
      GROUP BY s.Name ORDER BY TotalSeen DESC LIMIT 10
    """)
    for row in cur.fetchall():
        print(row)
    cur.close()

def show_alerts(conn):
    cur = conn.cursor()
    cur.execute("""
      SELECT a.AlertID, s.Name, l.LocationName, r.RangerName, a.DateSeen, a.Message
      FROM Alerts a
      JOIN Species s ON a.SpeciesID = s.SpeciesID
      JOIN Locations l ON a.LocationID = l.LocationID
      LEFT JOIN Rangers r ON a.RangerID = r.RangerID
      ORDER BY a.DateSeen DESC
    """)
    for row in cur.fetchall():
        print(row)
    cur.close()

def call_proc(conn, proc_name, *args):
    cur = conn.cursor()
    cur.callproc(proc_name, args)
    for result in cur.stored_results():
        for row in result.fetchall():
            print(row)
    cur.close()

def menu():
    conn = connect()
    if not conn.is_connected():
        print("Connection failed. Check config.")
        return
    try:
        while True:
            print("\n1) List species  2) Add sighting  3) Top species  4) Show alerts")
            print("5) Sightings by species (proc)  6) Refresh monthly summary  0) Exit")
            c = input("Choice: ").strip()
            if c == '1':
                list_species(conn)
            elif c == '2':
                add_sighting(conn)
            elif c == '3':
                top_species(conn)
            elif c == '4':
                show_alerts(conn)
            elif c == '5':
                name = input("Species name (exact): ").strip()
                call_proc(conn, 'get_sightings_by_species', name)
            elif c == '6':
                call_proc(conn, 'refresh_monthly_summary')
                print("Monthly summary refreshed.")
            elif c == '0':
                break
            else:
                print("Invalid choice.")
    finally:
        conn.close()

if __name__ == '__main__':
    menu()
