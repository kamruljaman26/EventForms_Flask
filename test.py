from app import Session, User, db
import xlsxwriter
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, 'UserData.xlsx')
print(my_file)

workbook = xlsxwriter.Workbook(my_file)

# Sheet1, Sheet2 etc., but we can also specify a name.
worksheet = workbook.add_worksheet("User Data")

# Start from the first cell. Rows and
row = 0
col = 0

# Add Header
worksheet.write(0, col, 'Name')
worksheet.write(0, col + 1, 'Phone Numer')
worksheet.write(0, col + 2, 'Email Address')
worksheet.write(0, col + 3, 'NID/Pass')
worksheet.write(0, col + 4, 'Total Participant')
worksheet.write(0, col + 5, 'Session ID')

# Update Row
row += 1

# Collect Data From DB
result = db.session.query(User).all()

for user in result:
    worksheet.write(row, col, user.name)
    worksheet.write(row, col + 1, user.phone)
    worksheet.write(row, col + 2, user.email)
    worksheet.write(row, col + 3, user.nid_pas_num)
    worksheet.write(row, col + 4, user.participant)
    worksheet.write(row, col + 5, user.session_id)
    row += 1

workbook.close()
