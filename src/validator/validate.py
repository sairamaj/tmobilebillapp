import glob
import tabula

numberOfLines = 12


class Entry:
    def __init__(self, number, amount, equipment, services, onetime_charge, total):
        self.number = number
        self.amount = amount
        self.equipment = equipment
        self.onetime_charge = onetime_charge
        self.services = services
        self.total = total


def toAmount(val):
    if val.strip() == '-':
        return 0.0
    return float(val.lstrip('$'))


class EntryParser:
    def __init__(self, ds_columns):
        self.phone = 0
        self.equipment = -1
        self.services = -1
        self.onetime_charge = -1
        print(f'type is:{type(ds_columns)}')
        columns = ds_columns.to_list()
        print(columns)
        print(type(columns))
        if "Equipment" in columns:
            self.equipment = columns.index('Equipment')
        if "Services" in columns:
            self.services = columns.index('Services')
        if "One-time charges" in columns:
            self.onetime_charge = columns.index('One-time charges')

    def parse(self, dFrame):
        phone = dFrame[self.phone]
        equipment = 0.0
        services = 0.0
        onetime_charge = 0.0
        if self.equipment > 0:
            equipment = toAmount(dFrame[self.equipment])
        if self.services > 0:
            services = toAmount(dFrame[self.services])
        if self.onetime_charge > 0:
            onetime_charge = toAmount(dFrame[self.onetime_charge])
        total = self.perLine + equipment + services + onetime_charge
        return Entry(phone, self.perLine, equipment, services, onetime_charge, total)


def parseBill(fileName):
    table = tabula.read_pdf(fileName, pages=2)
    ds = table[0]

    entryParser = EntryParser(ds.columns)

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
            finalAmount = toAmount(val[-1])
            planAmount = toAmount(val[2])
            entryParser.perLine = planAmount/numberOfLines

        if row >= 2:
            entries.append(entryParser.parse(val))
        row = row+1

    return planAmount, finalAmount, entries


def display(entries):
    print(f"{'Number':^18}|{'Amount':^12}|{'Equipment':^12}|{'Services':^12}|{'One Time':^12}|{'Total':^12}")
    for entry in entries:
        print(
            f"{entry.number:^18}|{entry.amount:^12.2f}|{entry.equipment:^12}|{entry.services:^12}|{entry.onetime_charge:^12}|{entry.total:^12.2f}")
    print('______________________________________________________')

def validate(file, billAmount, entires):
    entriesTotal = 0
    for entry in entries:
        entriesTotal += entry.total

    if(abs(billAmount - entriesTotal) > 1.0):
        print('-------------- NO MATCH -----------------')
        raise ValueError(
            f"Not matched: {billAmount} with {entriesTotal} in {file}")
    else:
        print('-------------- MATCH -----------------')
        print('________________________________________')
        print(f'Bill Total: {billAmount:.2f}')
        print(f'Total: from entries:{entriesTotal:.2f}')


def save(month, entries):
    file = f'{month}.txt'
    with open(file, 'w') as writer:
        writer.write(f"{'Number':^18}|{'Amount':^12}|{'Equipment':^12}|{'Services':^12}|{'One Time':^12}|{'Total':^12}\n")
        for entry in entries:
            writer.write(f"{entry.number:^18}|{entry.amount:^12.2f}|{entry.equipment:^12}|{entry.services:^12}|{entry.onetime_charge:^12}|{entry.total:^12.2f}\n")
    print(f"{file} saved.")

for file in glob.glob('c:\\sai\\dev\\temp\\pdf\\tmobile\\*.pdf'):
    print(f' validating : {file}')
    planAmount, billAmount, entries = parseBill(file)
    display(entries)
    print(f'final amount:{billAmount:.2f}')
    print(f'plan Amount:{planAmount:.2f}')
    validate(file, billAmount, entries)
    month = file.lstrip('SummaryBill')
    save(month, entries)
