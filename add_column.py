import sqlite3
db = sqlite3.connect('instance/foundation.db')
db.execute("ALTER TABLE donations ADD COLUMN payment_method VARCHAR(50) DEFAULT 'Manual'")
db.commit()
db.close()
print('payment_method column added successfully')
