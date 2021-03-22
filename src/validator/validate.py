import glob
import tabula

numberOfLines = 12


class Entry:
    def __init__(self, number, amount, equipment, total):
        self.number = number
        self.amount = amount
        self.equipment = equipment
        self.total = total

def toAmount(val):
    if val.strip() == '-':
        return 0.0
    return float(val.lstrip('$'))

def parseBill(fileName):
    table = tabula.read_pdf(fileName, pages=2)
    ds = table[0]

    entries = []
    row = 0
    perLine = 0
    planAmount = 0
    finalAmount = 0
    for val in ds.values:

        # -----------------------row 0 -------------------------
        # Line Type Plans Equipment Services Total
        # -----------------------row 1-------------------------
        # Totals $233.22 $29.17 $0.00 $262.39
        # -----------------------row 2 onwards -------------------------
        # (xxx) xxx-xxxx Voice $4.28 - - $4.28
        if row == 0:
            finalAmount = toAmount(val[5])
            planAmount = toAmount(val[2])
            perLine = planAmount/numberOfLines
        if row >= 2:
            equipment = toAmount(val[3])
            total = perLine + equipment
            entries.append(Entry(val[0], perLine, equipment, total))
        row = row+1

    return planAmount, finalAmount, entries

def validate(file, billAmount, entires):
    entriesTotal = 0
    for entry in entries:
        print(f"{entry.number} | {entry.amount}| {entry.equipment}| {entry.total}")
        entriesTotal += entry.amount
        entriesTotal += entry.equipment
    
    if(abs(billAmount - entriesTotal) > 1.0):
        print('-------------- NO MATCH -----------------')
        raise ValueError(f"Not matched: {billAmount} with {entriesTotal} in {file}")
    else:
        print('-------------- MATCH -----------------')
        print('________________________________________')
        print(f'Bill Total: {billAmount}')
        print(f'Total: from entries:{entriesTotal}')


for file in glob.glob('c:\\sai\\dev\\temp\\pdf\\tmobile\\*.pdf'):
    print(f' validating : {file}')
    entries = parseBill(file)
    total, billAmount, entries = parseBill(file)
    validate(file, billAmount, entries)


