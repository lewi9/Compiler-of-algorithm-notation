import pandas as pd
 
def save(name, grade, comment):
    try:
        df = pd.read_excel('oceny.xlsx')
        student = list(df.loc[df['Imie i nazwisko'] == name]['Imie i nazwisko'])
        if len(student):
            df.loc[df['Imie i nazwisko'] == name, 'Ocena'] = grade
            df.loc[df['Imie i nazwisko'] == name, 'Komentarz'] = comment
        else:
            data = {
                'Imie i nazwisko': [name],
                'Ocena': [grade],
                'Komentarz': [comment]
            }
            df2 = pd.DataFrame(data)
            df = df.append(df2)
        df.to_excel('oceny.xlsx', index=False)
    except FileNotFoundError:
        data = {
            'Imie i nazwisko': [name],
            'Ocena': [grade],
            'Komentarz': [comment]
        }
        df = pd.DataFrame(data)
        df.to_excel('oceny.xlsx', index=False)
 
