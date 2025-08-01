import sqlite3


conn = sqlite3.connect('donation_system.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    User_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Address TEXT,
    Phone TEXT UNIQUE
)
''')


cursor.execute('''
CREATE TABLE IF NOT EXISTS Medicine (
    Medicine_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Expiry_Date TEXT NOT NULL,
    Quantity INTEGER CHECK (Quantity > 0),
    Category TEXT
)
''')

# جدول الصيدليات
cursor.execute('''
CREATE TABLE IF NOT EXISTS Pharmacy (
    Pharmacy_ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Address TEXT NOT NULL
)
''')

# جدول التبرعات
cursor.execute('''
CREATE TABLE IF NOT EXISTS Donation (
    Donation_ID INTEGER PRIMARY KEY,
    User_ID INTEGER NOT NULL,
    Medicine_ID INTEGER NOT NULL,
    Pharmacy_ID INTEGER NOT NULL,
    Donation_Date TEXT DEFAULT CURRENT_DATE,
    Status TEXT CHECK (Status IN ('Pending', 'Accepted', 'Rejected')),
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Medicine_ID) REFERENCES Medicine(Medicine_ID),
    FOREIGN KEY (Pharmacy_ID) REFERENCES Pharmacy(Pharmacy_ID)
)
''')

# جدول التوزيع
cursor.execute('''
CREATE TABLE IF NOT EXISTS Distribution (
    Distribution_ID INTEGER PRIMARY KEY,
    Donation_ID INTEGER UNIQUE NOT NULL,
    Pharmacy_ID INTEGER NOT NULL,
    Distribution_Date TEXT DEFAULT CURRENT_DATE,
    FOREIGN KEY (Donation_ID) REFERENCES Donation(Donation_ID),
    FOREIGN KEY (Pharmacy_ID) REFERENCES Pharmacy(Pharmacy_ID)
)
''')

# إدخال بيانات تجريبية
cursor.executemany("INSERT OR IGNORE INTO Users VALUES (?, ?, ?, ?)", [
    (1, 'Layan Ahmed', 'Menoufia - Shebin El Kom', '01012345678'),
    (2, 'Mohamed Adel', 'Tanta - Gharbia', '01098765432'),
    (3, 'Sara Youssef', 'Cairo - Nasr City', '01122223333')
])

cursor.executemany("INSERT OR IGNORE INTO Medicine VALUES (?, ?, ?, ?, ?)", [
    (1, 'Panadol', '2025-12-31', 5, 'Painkiller'),
    (2, 'Amoxicillin', '2026-01-15', 10, 'Antibiotic'),
    (3, 'Vitamin C', '2026-05-01', 20, 'Supplement')
])

cursor.executemany("INSERT OR IGNORE INTO Pharmacy VALUES (?, ?, ?)", [
    (1, 'Al-Shefa Pharmacy', 'Menoufia - Shebin El Kom'),
    (2, 'Al-Hayah Pharmacy', 'Cairo - Nasr City')
])

cursor.executemany("INSERT OR IGNORE INTO Donation VALUES (?, ?, ?, ?, ?, ?)", [
    (1, 1, 1, 1, '2025-05-01', 'Accepted'),
    (2, 2, 2, 2, '2025-05-03', 'Pending'),
    (3, 3, 3, 2, '2025-05-04', 'Accepted')
])

cursor.executemany("INSERT OR IGNORE INTO Distribution VALUES (?, ?, ?, ?)", [
    (1, 1, 1, '2025-05-02'),
    (2, 3, 2, '2025-05-05')
])

# مثال استعلامات
cursor.execute('''
SELECT Donation_ID, Donation_Date, Status
FROM Donation
WHERE Status = 'Accepted';
''')
accepted_donations = cursor.fetchall()
print("Accepted Donations:")
for d in accepted_donations:
    print(d)

cursor.execute('''
SELECT Users.Name AS User_Name, Medicine.Name AS Medicine_Name
FROM Donation
JOIN Users ON Donation.User_ID = Users.User_ID
JOIN Medicine ON Donation.Medicine_ID = Medicine.Medicine_ID;
''')
donations = cursor.fetchall()
print("\nDonation Details:")
for d in donations:
    print(d)

# حفظ البيانات
conn.commit()
conn.close()

print("\nDatabase created successfully ")