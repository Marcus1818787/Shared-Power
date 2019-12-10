import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from datetime import datetime
from tokenize import Double

from sqlalchemy import DateTime

from app.models import session
from app.models.booking import Booking
from app.models.dispatch import Dispatch
from app.models.returns import Returns
from app.models.tools import Tools
from app.models.users import Users


class Bookings(tk.Frame):


    def __init__(self, root):
        self.FONT = 'Helvetica'
        self.TITLE_SIZE = 24

        # this is for testing purposes only
        # grab the user with the specified id to query for his bookings
        self.CURRENT_USER = session.query(Users).filter_by(id=1).first()

        # create a new frame
        tk.Frame.__init__(self, root)
        label = Label(self, text="Bookings", font=(self.FONT, self.TITLE_SIZE)).pack(side='top')
        return_button = Button(self, text="Return tool").pack(anchor='w')
        report_button = Button(self, text="Report tool").pack(anchor='w')
        self.createTable()
        self.loadTable()



    def createTable(self):
        tv = Treeview(self)
        tv.pack(side='left')
        vsb = Scrollbar(self, orient="vertical", command=tv.yview)
        vsb.pack(side='right', fill='y')

        tv.configure(yscrollcommand=vsb.set)

        tv['columns'] = ('return_date', 'cost', 'delivery')

        tv.heading("#0", text='Booked date', anchor='w')
        tv.column("#0", anchor="w")

        tv.heading('return_date', text='Due return date')
        tv.column('return_date', anchor='center', width=100)

        tv.heading('cost', text='Cost')
        tv.column('cost', anchor='center', width=100)

        tv.heading('delivery', text='Delivery/Collection')
        tv.column('delivery', anchor='center', width=100)

        tv.pack(fill=BOTH, expand=1)
        self.treeview = tv


    def loadTable(self):
        _user_bookings = []
        user_bookings = session.query(Booking).filter(Booking.user_id==self.CURRENT_USER.id)

        # join the tables
        for book in user_bookings:
            tool = session.query(Tools).filter_by(id=book.tool_id).first()

            data = {
                "id": book.id,
                "booked_date": book.booked_date,
                "duration_of_booking": book.duration_of_booking,
                "tool_id": book.tool_id,
                "user_id": book.user_id,
                "tool_name": tool.name,
                "tool_daily_price": tool.daily_price,
                "tool_half_day_price": tool.half_day_price
            }

            # if the customer books a tool for x days + half day we write in in db as x.5
            # here we calculate the price
            if '.' in book.duration_of_booking:
                data['cost'] = (int(book.duration_of_booking[:book.duration_of_booking.find('.')]) *
                                float(tool.daily_price)
                                + float(tool.half_day_price))
            else:
                data['cost'] = (int(book.duration_of_booking) * float(tool.daily_price))

            try:
                return_date = session.query(Returns).filter_by(booking_id=book.id).first()
                if return_date.returned == True:
                    data['return_date'] = "Returned"
            except:
                data['return_date'] = book.return_date

            try:
                dispatch = session.query(Dispatch).filter_by(booking_id=book.id).first()
                data['delivery'] = f"Delivery on {dispatch.dispatch_datetime}"
                print(dispatch.dispatch_datetime)
            except:
                data['delivery'] = "Collect"

            _user_bookings.append(data)
        print(_user_bookings)

        for booking in _user_bookings:
            self.treeview.insert('', 'end', text=booking['booked_date'],
                                 values=(booking['return_date'], booking['cost'], booking['delivery']))