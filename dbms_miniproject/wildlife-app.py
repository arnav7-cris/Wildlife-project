import streamlit as st
import mysql.connector
import pandas as pd

# ---------- DATABASE CONNECTION ----------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",  # change if needed
        database="WildlifeDB"
    )

# ---------- MAIN APP ----------
st.set_page_config(page_title="🐅 Wildlife Management Dashboard", layout="wide")
st.title("🐅 Wildlife Management Dashboard")

# Sidebar menu with your required options in order
menu = st.sidebar.selectbox(
    "Select Option",
    [
        "📅 View Sightings by date (range)",
        "📋 View Full Sightings",
        "➕ Add Sighting",
        "📈 Top Species",
        "🚨 View Alerts"
    ]
)

# ---------- VIEW SIGHTINGS BY DATE (RANGE) ----------
if menu == "📅 View Sightings by date (range)":
    st.subheader("📅 Sightings Report (by Date Range)")

    start_date = st.sidebar.date_input("Start Date")
    end_date = st.sidebar.date_input("End Date")
    if start_date > end_date:
        st.sidebar.error("Start Date cannot be after End Date.")

    species_name = st.sidebar.text_input("Species Name (optional)")

    conn = get_connection()
    query = """
        SELECT s.SightingID, sp.Name AS Species, l.LocationName, r.RangerName,
               s.DateSeen, s.Quantity, s.Notes
        FROM Sightings s
        JOIN Species sp ON s.SpeciesID = sp.SpeciesID
        JOIN Locations l ON s.LocationID = l.LocationID
        LEFT JOIN Rangers r ON s.RangerID = r.RangerID
        WHERE s.DateSeen BETWEEN %s AND %s
    """
    params = (start_date, end_date)
    if species_name:
        query += " AND sp.Name LIKE %s"
        params = (start_date, end_date, f"%{species_name}%")

    df = pd.read_sql(query, conn, params=params)
    conn.close()

    with st.container():
        st.markdown('<div class="blur-container">', unsafe_allow_html=True)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            chart_data = df.groupby("Species")["Quantity"].sum().reset_index()
            st.bar_chart(chart_data, x="Species", y="Quantity")
        else:
            st.info("No data found for the selected filters.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- VIEW FULL SIGHTINGS ----------
elif menu == "📋 View Full Sightings":
    st.subheader("📋 Sightings Report (All Sightings)")

    species_name = st.sidebar.text_input("Species Name (optional)")
    conn = get_connection()
    query = """
        SELECT s.SightingID, sp.Name AS Species, l.LocationName, r.RangerName,
               s.DateSeen, s.Quantity, s.Notes
        FROM Sightings s
        JOIN Species sp ON s.SpeciesID = sp.SpeciesID
        JOIN Locations l ON s.LocationID = l.LocationID
        LEFT JOIN Rangers r ON s.RangerID = r.RangerID
    """
    if species_name:
        query += " WHERE sp.Name LIKE %s"
        df = pd.read_sql(query, conn, params=(f"%{species_name}%",))
    else:
        df = pd.read_sql(query, conn)
    conn.close()

    with st.container():
        st.markdown('<div class="blur-container">', unsafe_allow_html=True)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            chart_data = df.groupby("Species")["Quantity"].sum().reset_index()
            st.bar_chart(chart_data, x="Species", y="Quantity")
        else:
            st.info("No data found.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- ADD SIGHTING ----------
elif menu == "➕ Add Sighting":
    st.subheader("➕ Add a New Sighting")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT SpeciesID, Name FROM Species ORDER BY Name")
    species = cur.fetchall()
    cur.execute("SELECT LocationID, LocationName FROM Locations ORDER BY LocationName")
    locations = cur.fetchall()
    cur.execute("SELECT RangerID, RangerName FROM Rangers ORDER BY RangerName")
    rangers = cur.fetchall()
    cur.close()

    species_dict = {name: sid for sid, name in species}
    location_dict = {name: lid for lid, name in locations}
    ranger_dict = {name: rid for rid, name in rangers}

    sp_name = st.selectbox("Species", list(species_dict.keys()))
    loc_name = st.selectbox("Location", list(location_dict.keys()))
    rg_name = st.selectbox("Ranger", list(ranger_dict.keys()))
    date_seen = st.date_input("Date Seen")
    qty = st.number_input("Quantity", min_value=1, value=1)
    notes = st.text_area("Notes (optional)")

    if st.button("Submit Sighting"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            sql = """
                INSERT INTO Sightings (SpeciesID, LocationID, RangerID, DateSeen, Quantity, Notes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql, (species_dict[sp_name], location_dict[loc_name],
                              ranger_dict[rg_name], date_seen, qty, notes))
            conn.commit()
            st.success("✅ Sighting added successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cur.close()
            conn.close()

# ---------- TOP SPECIES ----------
elif menu == "📈 Top Species":
    st.subheader("📈 Top 10 Most-Sighted Species")

    conn = get_connection()
    query = """
        SELECT s.Name AS Species, SUM(si.Quantity) AS TotalSeen
        FROM Sightings si
        JOIN Species s ON si.SpeciesID = s.SpeciesID
        GROUP BY s.Name
        ORDER BY TotalSeen DESC
        LIMIT 10
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df, x="Species", y="TotalSeen")
    else:
        st.info("No sightings data available.")

# ---------- VIEW ALERTS ----------
elif menu == "🚨 View Alerts":
    st.subheader("🚨 Endangered Species Alerts")

    conn = get_connection()
    query = """
        SELECT a.AlertID, s.Name AS Species, l.LocationName, r.RangerName,
               a.DateSeen, a.Message
        FROM Alerts a
        JOIN Species s ON a.SpeciesID = s.SpeciesID
        JOIN Locations l ON a.LocationID = l.LocationID
        LEFT JOIN Rangers r ON a.RangerID = r.RangerID
        ORDER BY a.DateSeen DESC
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No alerts found.")

# --- Chatbot Section ---
chatbot_qa = {
    "What is an endangered species?": "An endangered species is one that is at risk of extinction due to loss of habitat or declining population.",
    "How are sightings recorded?": "Rangers record sightings by entering species, location, date, and quantity into the system.",
    "What is the purpose of alerts?": "Alerts are automatically created when endangered species are sighted, helping authorities take quick action.",
    "How can I view recent sightings?": "You can filter sightings by date range in the main dashboard.",
    "Who records sightings?": "Wildlife rangers and authorized personnel record sightings.",
    "How often is data updated?": "Data is updated whenever new sightings are entered into the database.",
    "What does the quantity field mean?": "It shows how many animals of that species were seen in that sighting.",
    "How do I search for a species?": "Use the sidebar text box to search by species name.",
    "What happens if an endangered animal is spotted?": "A trigger automatically inserts an alert into the Alerts table to notify authorities."
}

st.sidebar.header("🤖 Wildlife Chatbot")
user_question = st.sidebar.selectbox("Ask a question:", ["Select..."] + list(chatbot_qa.keys()))

if user_question != "Select...":
    st.markdown(f"**You asked:** {user_question}")
    st.info(chatbot_qa[user_question])
