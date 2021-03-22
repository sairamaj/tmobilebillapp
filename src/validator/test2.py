import glob
import tabula

class Entry:
    def __init__(self, number, amount, equipment, total):
        self.number = number
        self.amount = amount
        self.equipment = equipment
        self.total = total

def parseBill(fileName):
    table = tabula.read_pdf(fileName,pages=2)
    ds = table[0]

    entries = []
    row = 0
    for val in ds.values:
        if row >= 2:
            entries.append(Entry(val[0],val[2],val[3],val[5]))
        row = row+1

    return entries

for file in glob.glob('tmobile\*.pdf'):
    entries = parseBill(file)
    for entry in entries:
        print(f"{entry.number} | {entry.amount}| {entry.equipment}| {entry.total}")
    print('________________________________________')
