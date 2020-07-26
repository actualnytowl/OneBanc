import pandas as pd
import re
output = pd.DataFrame(columns=['Date', 'Transaction Description', 'Debit', 'Credit', 'Currency', 'CardName', 'Transaction', 'Location'])


def axis(df):
    i = cnt = name = 0
    while i < len(df):
        temp = [df.iloc[i, y].lower() if isinstance(df.iloc[i, y], str) else 0 for y in range(3)]
        if 'domestic transaction' in temp or 'domestic transactions' in temp:
            currency = "INR"
            dom_or_int = 'domestic'
        elif 'international transaction' in temp or 'international transactions' in temp:
            currency = None
            dom_or_int = 'international'
        while True:
            date, debit, credit, trans = list(df.iloc[i])
            if not re.match("[0-3][0-9]-[0-1][0-9]-[0-9][0-9][0-9][0-9]", str(date)):
                if isinstance(credit, str): name = credit
                break
            location = trans.split()[-1] if currency == 'INR' else trans.split()[-2]
            currency = trans.split()[-1] if currency != "INR" else 'INR'
            trans = trans.split()
            output.loc[cnt] = [date, " ".join(trans if currency == "INR" else trans[:len(trans)-1]), debit, credit, currency, name, dom_or_int, location]
            cnt += 1
            i += 1
            if i == len(df): break
        i += 1


def hdfc(df):
    i = cnt = name = 0

    while i < len(df):
        temp = [df.iloc[i, y].lower() if isinstance(df.iloc[i, y], str) else 0 for y in range(2)]
        if 'domestic transaction' in temp or 'domestic transactions' in temp:
            currency = "INR"
            dom_or_int = 'domestic'
        elif 'international transaction' in temp or 'international transactions' in temp:
            currency = None
            dom_or_int = 'international'
        while True:
            date, trans, amt = list(df.iloc[i])
            if 'cr' in (amt.lower() if isinstance(amt, str) else ""):
                credit = amt.split()[0]
                debit = 0
            else:
                debit = amt
                credit = 0
            if not re.match("[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]", str(date)):
                if isinstance(trans, str): name = trans
                break
            location = trans.split()[-1] if currency == 'INR' else trans.split()[-2]
            currency = trans.split()[-1] if currency != "INR" else 'INR'
            trans = trans.split()
            output.loc[cnt] = [date, " ".join(trans if currency == "INR" else trans[:len(trans)-1]), debit, credit, currency, name, dom_or_int, location]
            cnt += 1
            i += 1
            if i == len(df): break
        i += 1


def icici(df):
    i = cnt = name = 0

    while i < len(df):
        temp = [df.iloc[i, y].lower() if isinstance(df.iloc[i, y], str) else 0 for y in range(4)]
        if 'domestic transaction' in temp or 'domestic transactions' in temp:
            currency = "INR"
            dom_or_int = 'domestic'
        elif 'international transaction' in temp or 'international transactions' in temp:
            currency = None
            dom_or_int = 'international'
        while True:
            date, *trans, debit, credit, _ = list(df.iloc[i])
            trans = (" ".join(map(lambda m: "" if pd.isnull(m) else m,trans))).strip()
            if not re.match("[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]", str(date)):
                if isinstance(debit, str): name = debit
                break
            # this try block is for handling the "Airtel payment, mumbai" transaction in line 9 of ICICI-Input-Case2.csv
            try: debit = int(debit.strip()) if isinstance(debit, str) else 0
            except: trans += " "+debit.strip() if isinstance(debit, str) else ""; debit = credit; credit = _
            location = trans.split()[-1] if currency == 'INR' else trans.split()[-2]
            currency = trans.split()[-1] if currency != "INR" else 'INR'
            trans = trans.split()
            try: location = int(location); location = "not given"
            except: pass
            output.loc[cnt] = [date, " ".join(trans if currency == "INR" else trans[:len(trans)-1]), debit, credit, currency, name, dom_or_int, location]
            # print(date,", ", " ".join(trans if currency == "INR" else trans[:len(trans)-1]),", ", debit,", ", credit)
            cnt += 1
            i += 1
            if i == len(df): break
        i += 1


def idfc(df):
    i = cnt = name = 0

    while i < len(df):
        temp = [df.iloc[i, y].lower() if isinstance(df.iloc[i, y], str) else 0 for y in range(5)]
        if 'domestic transaction' in temp or 'domestic transactions' in temp:
            currency = "INR"
            dom_or_int = 'domestic'
        elif 'international transaction' in temp or 'international transactions' in temp:
            currency = None
            dom_or_int = 'international'
        while True:
            trans, date, amt, *_ = list(df.iloc[i])
            if 'cr' in (amt.lower() if isinstance(amt, str) else ""):
                credit = amt.split()[0]
                debit = 0
            else:
                debit = amt
                credit = 0
            if not re.match("[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]", str(date)):
                if isinstance(date, str):
                    name = date
                break
            location = trans.split()[-1] if currency == 'INR' else trans.split()[-2]
            currency = trans.split()[-1] if currency != "INR" else 'INR'
            trans = trans.split()
            output.loc[cnt] = [date, " ".join(trans if currency == "INR" else trans[:len(trans)-1]), debit, credit, currency, name, dom_or_int, location]
            cnt += 1
            i += 1
            if i == len(df): break
        i += 1


def StandardizeStatement( inputFile, outputFile):
    import_file_path = r"C:\Users\Sagar Annaji\Desktop\Interview_Fresher_Any_Language"
    read_file = pd.read_csv(import_file_path+"\\"+inputFile, delimiter=",", header=None)
    if 'axis' in inputFile.lower():
        axis(read_file)
    elif 'hdfc' in inputFile.lower():
        hdfc(read_file)
    elif 'icici' in inputFile.lower():
        icici(read_file)
    elif 'idfc' in inputFile.lower():
        idfc(read_file)
    output.fillna(0, inplace=True)
    output.to_csv(r"C:\Users\Sagar Annaji\Desktop\Interview_Fresher_Any_Language"+"\\"+outputFile, index=False)

    
StandardizeStatement('ICICI-Input-Case2.csv','ICICI-Output-Case2.csv')
