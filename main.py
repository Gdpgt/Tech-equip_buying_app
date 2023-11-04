# An app that lets you choose and buy available tech equipments,
# then lets you download the receipt as a pdf

import pandas as pd
from fpdf import FPDF
import time

df = pd.read_csv('articles.csv', dtype={'ID': str})


class Equipment:
    def __init__(self, local_article_id):
        self.id = local_article_id
        self.name = df.loc[df['ID'] == self.id, 'NAME'].squeeze()
        self.price = df.loc[df['ID'] == self.id, 'PRICE'].squeeze()

    def is_available(self):
        if df.loc[df['ID'] == self.id, 'IN STOCK'].squeeze() > 0:
            return True
        else:
            return False

    def book(self):
        # Diminishes the stock of the item by 1
        df.loc[df['ID'] == self.id, 'IN STOCK'] -= 1
        # Writes the updated df back to the csv, without the index
        df.to_csv('articles.csv', index=False)


class Receipts:
    def __init__(self, equip_instance):
        # This allows to use the Equipment class's attributes like "id"
        # by using an Equipment instance as a Receipts class attribute
        self.equip = equip_instance

    def create_pdf(self):
        pdf = FPDF('P', 'mm', 'A4')
        pdf.add_page()

        # RECEIPT LINE
        pdf.set_font('Times', style='B', size=18)
        # Automatically found width so that the next cell appears correctly
        pdf.cell(w=pdf.get_string_width('Receipt: #'), h=12, txt='Receipt: #')
        # Changing the font x times so that the output is more visible unbolded
        pdf.set_font('Times', size=16)
        pdf.cell(w=0, h=12, txt=self.equip.id, ln=1)

        # ARTICLE LINE
        pdf.set_font('Times', style='B', size=18)
        pdf.cell(w=pdf.get_string_width('Article:  '), h=12,
                 txt='Article:  ')
        pdf.set_font('Times', size=16)
        pdf.cell(w=0, h=12, txt=self.equip.name, ln=1)

        # PRICE LINE
        pdf.set_font('Times', style='B', size=18)
        pdf.cell(w=pdf.get_string_width('Price:     '), h=12,
                 txt='Price:     ')
        pdf.set_font('Times', size=16)
        pdf.cell(w=0, h=12, txt=str(self.equip.price))
        pdf.output('Receipt.pdf')

    def send_message(self):
        message = f"""
Your purchase has been successful, PLEASE DOWNLOAD your receipt.pdf

Receipt # : {self.equip.id}
Article : {self.equip.name}
Price : {self.equip.price}             
"""
        return print(message)


while True:
    print(df.to_string(index=False))
    print('-' * len(df.columns) * 12 + '\n')

    article_id = input('Enter the ID of the article you want to purchase: ')

    equipment = Equipment(article_id)

    if equipment.is_available():
        equipment.book()

        receipts = Receipts(equipment)
        receipts.create_pdf()
        receipts.send_message()

        time.sleep(10)
        print("\n" * 4)

    else:
        print("\nThis article is OUT OF STOCK, please choose another one")

        time.sleep(4)
        print("\n" * 4)
