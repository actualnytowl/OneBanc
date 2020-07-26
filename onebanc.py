import pandas as pd
import re
output = pd.DataFrame(columns=['Date', 'Transaction Description', 'Debit', 'Credit', 'Currency', 'CardName', 'Transaction', 'Location'])


def StandardizeStatement( inputFile, outputFile):

    '''change this path
           to the directory of input files'''
    import_file_path = r"C:\Users\Sagar Annaji\Desktop\Interview_Fresher_Any_Language"
    df = pd.read_csv(import_file_path+"\\"+inputFile, delimiter=",", header=None)
    i = cnt = name = 0
    order = {}
    while i < len(df):
        temp = [df.iloc[i, y].lower() if isinstance(df.iloc[i, y], str) else 0 for y in range(len(df.columns))]
        if 'domestic transaction' in temp or 'domestic transactions' in temp or 'domestic' in temp:
            currency = "INR"
            dom_or_int = 'domestic'
        elif 'international transaction' in temp or 'international transactions' in temp or 'international' in temp:
            currency = None
            dom_or_int = 'international'
        while True:
            x = list(df.iloc[i])
            # print(x if cnt==5 else "",end="")
            x3 = list(map(lambda _: str(_) if isinstance(_, str) or not pd.isnull(_) else pd.np.nan, x))
            x3 = list(map(lambda _: _.strip() if isinstance(_, str) else pd.np.nan, x3))
            x = list(map(lambda _: _.lower() if isinstance(_, str) else pd.np.nan, x3))
            # print(x)
            if not order:
                if 'date' in x:
                    order['date'] = x.index('date')
                else:
                    break
                if 'credit' in x:
                    order['credit'] = x.index('credit')
                if 'debit' in x:
                    order['debit'] = x.index('debit')
                gg = lambda x1: 1 if 'transaction' in (x1.lower() if isinstance(x1, str) else "") else 0
                x2 = list(map(gg, x))
                if any(x2):
                    order['transaction description'] = x2.index(1)
                # print(order)
            if order:
                if 'amount' in x:
                    order['amount'] = x.index('amount')
                if order.get('amount'):
                    amt = x3[order['amount']]
                    if 'cr' in (amt.lower() if isinstance(amt, str) else ""):
                        credit = amt.split()[0]
                        debit = 0
                    else:
                        debit = amt
                        credit = 0
                else:
                    credit = x3[order['credit']]
                    debit = x3[order['debit']]
                date = x3[order['date']]
                trans = x3[order['transaction description']]
            else:
                date = pd.np.nan
            if not re.match("[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]", str(date)) or re.match(
                    "[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]", str(date)):
                # if isinstance(trans, str): name = trans
                xx = [df.iloc[i, y] if isinstance(df.iloc[i, y], str) else 0 for y in range(len(df.columns))]
                if xx.count(0) == len(xx) - 1:
                    for j in xx:
                        if j != 0:
                            if 'transaction' not in j.lower(): name = j
                break
            # print(date, trans, debit, credit)
            try:
                debit = int(debit.strip()) if isinstance(debit, str) else 0
            except:
                trans += " " + debit.strip() if isinstance(debit, str) else ""; debit = credit; credit = x3[-1]
            location = trans.split()[-1] if currency == 'INR' else trans.split()[-2]
            currency = trans.split()[-1] if currency != "INR" else 'INR'
            trans = trans.split()
            try:
                location = int(location); location = "not given"
            except:
                pass
            output.loc[cnt] = [date, " ".join(trans if currency == "INR" else trans[:len(trans) - 1]), debit, credit,
                               currency, name, dom_or_int, location]
            cnt += 1
            i += 1
            if i == len(df): break
        i += 1
    output.fillna(0, inplace=True)
    output.to_csv(import_file_path+"\\"+outputFile, index=False)

# z = ['ICICI-Input-Case2.csv', 'Axis-Input-Case3.csv','HDFC-Input-Case1.csv', 'IDFC-Input-Case4.csv']


StandardizeStatement('ICICI-Input-Case2.csv','ICICI-Output-Case2.csv')
