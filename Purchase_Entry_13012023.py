import tkinter as tk
import configparser

from PIL import Image, ImageTk
from tkcalendar import DateEntry
import json
import multiprocessing
import queue
import threading
import os
import shutil
import re
from openpyxl import load_workbook
from datetime import datetime
from win32com import client
import num2words
import tkinter.messagebox as messagebox
import logging
import babel.numbers
#new comment
# Configure logging to write to a file
logging.basicConfig(filename=r"C:\Users\AMARJEET\Desktop\python_bill\Log\log.Purchase_Entry", level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


Save_Party_button = 0
message_queue = queue.Queue()


class PurchaseBillApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.initialize_gui()

    def handle_arrow_keys(self, event):
        widget = event.widget  # Get the widget where the event occurred

        # Determine the direction based on the arrow key pressed
        new_row = 0
        new_col = 0
        if event.keysym == 'Up':
            new_row = widget.grid_info()["row"] - 1
            new_col = widget.grid_info()["column"]
        elif event.keysym == 'Down':
            new_row = widget.grid_info()["row"] + 1
            new_col = widget.grid_info()["column"]
        elif event.keysym == 'Left':
            new_row = widget.grid_info()["row"]
            new_col = widget.grid_info()["column"] - 1
        elif event.keysym == 'Right':
            new_row = widget.grid_info()["row"]
            new_col = widget.grid_info()["column"] + 1

        # Check if the new row and column are within the valid range
        if 0 <= new_row < self.rows and 0 <= new_col < len(
                ["Sl", "Description", "HSN", "QTY", "UNIT", "Rate", "Dis", "GST", "Total"]):
            # Iterate over all widgets inside the scrollable_frame to find the widget at the new position
            for child in self.scrollable_frame.winfo_children():
                if int(child.grid_info()["row"]) == new_row and int(child.grid_info()["column"]) == new_col:
                    child.focus_set()  # Set focus to the widget at the new position
                    break

    def initialize_gui(self):
        base_width, base_height = 1536, 864
        self.screen_width, self.screen_height = self.winfo_screenwidth(), self.winfo_screenheight()
        width_ratio, height_ratio = self.screen_width / base_width, self.screen_height / base_height

        self.geometry(f"{self.screen_width}x{self.screen_height}")
        self.create_navigation_frame(width_ratio, height_ratio)
        self.create_main_canvas(width_ratio, height_ratio)
        self.create_party_canvas(width_ratio, height_ratio)
        self.create_custom_frame(width_ratio, height_ratio)
        self.create_order_entry_panel(width_ratio, height_ratio)
        self.create_submit_button()

    def create_navigation_frame(self, width_ratio, height_ratio):
        frame_width = (265 / 1536) * self.winfo_screenwidth()
        frame_height = self.winfo_screenheight()
        frame_bg_color = "#9FA375"

        frame_nav = tk.Frame(self, width=frame_width, height=frame_height, bg=frame_bg_color)
        frame_nav.place(x=0, y=0)

        image_path = r"C:\Users\AMARJEET\Desktop\python_bill\Front_end_config\background_image.jpg"
        original_image = Image.open(image_path)
        resized_image = original_image.resize((int(frame_width), int((149 / 200) * frame_width)), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_image)

        image_label = tk.Label(frame_nav, image=tk_image, bg=frame_bg_color)
        image_label.image = tk_image
        image_label.place(x=0, y=0)

    def create_main_canvas(self, width_ratio, height_ratio):
        canvas = tk.Canvas(self, bg="#B9D0A1", highlightthickness=1)
        canvas.place(x=(265 / 1536) * self.winfo_screenwidth(), y=0,
                     width=(self.winfo_screenwidth() - (265 / 1536) * self.winfo_screenwidth()),
                     height=(86 / 864) * self.winfo_screenheight())

        canvas.create_text(
            (638 / 1536) * (self.winfo_screenwidth() - (265 / 1536) * self.winfo_screenwidth()),
            int((40.0 / 864) * self.winfo_screenheight()),
            text="PURCHASE BILL ENTRY",
            font=("Inter", int((32.0 / 864) * self.winfo_screenheight()), "bold"),
            fill="#000000"
        )

    def create_party_canvas(self, width_ratio, height_ratio):
        self.party_frame = tk.Frame(self, width=(self.winfo_screenwidth() - 265),
                                    height=(self.winfo_screenheight() - 87),
                                    bg="White")
        self.party_frame.place(x=(265 * width_ratio), y=((280) * height_ratio))

        self.Entry_Grid_frame = tk.Frame(self, width=(self.winfo_screenwidth() - 265),
                                         height=(self.winfo_screenheight() - 500),
                                         bg="White")
        self.Entry_Grid_frame.place(x=(265 * width_ratio), y=((330) * height_ratio))

        party_canvas = tk.Canvas(self, width=(1073 - 265), height=193, highlightthickness=0)
        self.round_rectangle(party_canvas, 0, 0, (1073 - 265), (280 - 87), radius=(150 * width_ratio), outline="",
                             fill="#E6E6DA")
        party_canvas.place(x=(265 * width_ratio), y=(87 * height_ratio), width=(1073 - 265), height=(280 - 87))
        party_canvas.configure(bg="white")

        party_canvas.create_text(
            (1073 - 265) * width_ratio / 2,
            20 * height_ratio,
            text="Party Details",
            font=("Amstelvar Alpha", int(18 * height_ratio)),
            fill="#F61616"
        )

        tk.Label(party_canvas, text="Select Party:").place(x=15, y=30 * height_ratio)
        party_options = ["Party A", "Party B", "Party C"]
        self.party_dropdown = tk.StringVar(party_canvas)
        self.party_dropdown.set(party_options[0])
        tk.OptionMenu(party_canvas, self.party_dropdown, *party_options).place(x=150 * width_ratio, y=30 * height_ratio)

        tk.Label(party_canvas, text="Party Name:").place(x=15, y=60 * height_ratio)
        self.party_name_entry = tk.Entry(party_canvas, width=80)
        self.party_name_entry.place(x=150 * width_ratio, y=60 * height_ratio)

        tk.Label(party_canvas, text="Party Address:").place(x=15, y=100 * height_ratio)
        self.party_address_entry = tk.Text(party_canvas, width=60, height=2)
        self.party_address_entry.place(x=150 * width_ratio, y=90 * height_ratio)

        tk.Label(party_canvas, text="Mobile No.:").place(x=15, y=130 * height_ratio)
        self.mob_no_entry = tk.Entry(party_canvas, width=30)
        self.mob_no_entry.place(x=150 * width_ratio, y=130 * height_ratio)

        tk.Label(party_canvas, text="Email_Id.:").place(x=350, y=135 * height_ratio)
        self.email_entry = tk.Entry(party_canvas, width=38)
        self.email_entry.place(x=400 * width_ratio, y=135 * height_ratio)

        tk.Label(party_canvas, text="GSTIN:", fg='Red').place(x=20, y=160 * height_ratio)
        self.gstin_entry = tk.Entry(party_canvas, width=30)
        self.gstin_entry.place(x=150 * width_ratio, y=160 * height_ratio)

        # Button for saving party details
        save_button_canvas = tk.Canvas(party_canvas, width=100 * width_ratio, height=30 * height_ratio,
                                       highlightthickness=0)
        self.round_rectangle(save_button_canvas, 0, 0, 100 * width_ratio, 30 * height_ratio, radius=20, outline="",
                             fill="#6FA1EC", tags="save_button")
        save_button_canvas.place(x=450 * width_ratio, y=160 * height_ratio)
        save_button_canvas.create_text(50 * width_ratio, 15 * height_ratio, text="Save Party",
                                       font=("Iris Grover", int(14 * height_ratio)), fill="black")
        save_button_canvas.bind("<Button-1>", self.button_pressed)
        save_button_canvas.bind("<ButtonRelease-1>", self.button_released)

    def round_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1 + radius, y1,
            x1 + radius, y1,
            x2 - radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1 + radius,
            x1, y1
        ]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def create_custom_frame(self, width_ratio, height_ratio):
        custom_frame = tk.Frame(self, width=(463 * width_ratio), height=(280 - 87), bg="white")
        custom_frame.place(x=(1074 * width_ratio), y=(87 * height_ratio))
        tk.Label(custom_frame, text="Invoice Details", fg='Red', bg='White',
                 font=("Amstelvar Alpha", int(18 * height_ratio))).place(
            x=(150 * width_ratio), y=10 * height_ratio)

        tk.Label(custom_frame, text="Invoice_No.:", fg='Blue', bg='White',
                 font=('AmstelvarAlpha', int(14 * height_ratio))).place(x=40, y=50 * height_ratio)
        self.Invoice_no = tk.Entry(custom_frame, width=30, bg='#D9D9D9')
        self.Invoice_no.place(x=200 * width_ratio, y=50 * height_ratio)

        tk.Label(custom_frame, text="Invoice_date.:", fg='Blue', bg='White',
                 font=('AmstelvarAlpha', int(14 * height_ratio))).place(x=40, y=100 * height_ratio)

        # Integrate Date Picker
        date_picker = DateEntry(custom_frame, width=30, background='darkblue', foreground='white', borderwidth=2,
                                date_pattern='dd-mm-yyyy')

        date_picker.place(x=200 * width_ratio, y=100 * height_ratio)
        selected_date = date_picker.get_date()
        self.Invoice_date = selected_date.strftime('%d-%m-%Y')  # Convert to dd-mm-yyyy format
        # logging.info(f"Selected Date: {formatted_date}")

    def adjust_entry_width(self, entry, col):
        """Adjust the width of the entry based on the column."""
        if col == 0:
            entry.config(width=10)
        elif col == 1:
            entry.config(width=70)
        elif col == 2:
            entry.config(width=20)
        elif col in (3, 4, 5):
            entry.config(width=20)
        elif col == 6:
            entry.config(width=15)
        elif col == 7:
            entry.config(width=10)
        elif col == 8:
            entry.config(width=18)

    def create_order_entry_panel(self, width_ratio, height_ratio):
        # Item entry canvas
        item_entry_canvas = tk.Canvas(self.party_frame, width=(self.screen_width - 265), height=51,
                                      highlightthickness=0)
        self.round_rectangle(item_entry_canvas, 1, 1, (self.screen_width - 265), 61, radius=1, outline="",
                             fill="#D9D9D9")
        item_entry_canvas.place(x=(1 * width_ratio), y=(1 * height_ratio), width=(self.screen_width - 265), height=51)
        item_entry_canvas.create_text(
            140 * width_ratio,
            30 * height_ratio,
            text="ITEMS ENTRY PANEL",
            font=("Amstelvar Alpha", int(18 * height_ratio)),
            fill="Black"
        )

        # Frame for the grid headers (fixed headers)
        header_frame = tk.Frame(self, bg="white")
        header_frame.place(x=(265 * width_ratio), y=((330) * height_ratio), width=(self.screen_width - 265), height=50)

        # Adjusted the widths of headers based on the adjust_entry_width function
        header_widths = [int(10 / 2.20), int(77 / 2.20), int(20 / 2.20), int(20 / 2.20), int(20 / 2.20), int(20 / 2.20),
                         int(18 / 2.20), int(10 / 2.20), int(20 / 2.20)]
        headers = ["Sl", "Description", "HSN", "QTY", "UNIT", "Rate", "Dis%", "GST%", "Total"]

        for col, (header, width) in enumerate(zip(headers, header_widths)):
            tk.Label(header_frame, text=header, bg="White", font=("Amstelvar Alpha", int(14 * height_ratio)), padx=10,
                     pady=10, width=width).grid(row=0, column=col, sticky="nsew")

        # Entry Grid Frame
        self.Entry_Grid_frame = tk.Frame(self, bg="white")
        self.Entry_Grid_frame.place(x=(265 * width_ratio), y=((380) * height_ratio), width=(self.screen_width - 265),
                                    height=(self.screen_height - 530))

        # Create a canvas within the Entry_Grid_frame
        self.canvas = tk.Canvas(self.Entry_Grid_frame, bg="white", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar
        scrollbar = tk.Scrollbar(self.Entry_Grid_frame, orient=tk.VERTICAL, command=self.canvas.yview, width=23)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create another frame inside the canvas to hold grid entries
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        # Your code for the grid entries will go here, inside self.scrollable_frame
        self.min_no_of_rows = 17
        self.initialize_grid_entry(headers)

    def initialize_grid_entry(self, headers):
        self.rows = self.min_no_of_rows
        for row in range(1, self.rows + 1):
            for col, header in enumerate(headers):
                self.entry = tk.Entry(self.scrollable_frame, bg="white")
                # self.entry.insert(0, header)  # Insert the header as a placeholder
                self.entry.grid(row=row, column=col, padx=0, pady=0, sticky="nsew")
                self.adjust_entry_width(self.entry, col)

                # Bind arrow keys to handle movement
                self.entry.bind("<Up>", self.handle_arrow_keys)
                self.entry.bind("<Down>", self.handle_arrow_keys)
                self.entry.bind("<Left>", self.handle_arrow_keys)
                self.entry.bind("<Right>", self.handle_arrow_keys)

                if row == self.rows and col == len(headers) - 1:
                    self.entry.bind("<Tab>", self.add_new_row)
                else:
                    self.entry.bind("<Tab>", lambda e, entry=self.entry: self.entry.tk_focusNext().focus())

        self.scrollable_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def add_new_row(self, event):
        # Increment the number of rows
        if event.widget.grid_info()["row"] == self.entry.grid_info()["row"]:
            self.rows += 1
            self.min_no_of_rows = self.min_no_of_rows + 1

            # Retrieve the total number of columns
            total_cols = len(["Sl", "Description", "HSN", "QTY", "UNIT", "Rate", "Dis", "GST", "Total"])

            # Create an empty row in the grid
            for col in range(total_cols):
                self.entry = tk.Entry(self.scrollable_frame, bg="white")
                self.entry.grid(row=self.rows, column=col, padx=0, pady=0, sticky="nsew")
                self.adjust_entry_width(self.entry, col)

                # Bind arrow keys to handle movement
                self.entry.bind("<Up>", self.handle_arrow_keys)
                self.entry.bind("<Down>", self.handle_arrow_keys)
                self.entry.bind("<Left>", self.handle_arrow_keys)
                self.entry.bind("<Right>", self.handle_arrow_keys)

                if col == total_cols - 1:  # Check if it's the last column in the row
                    self.entry.bind("<Tab>", self.add_new_row)  # Bind the Tab key to add a new row when pressed
                else:
                    self.entry.bind("<Tab>", lambda e, entry=self.entry: entry.tk_focusNext().focus())

            # After adding a new row, update the scroll region again
            self.scrollable_frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            # Return 'break' to prevent default tab behavior (e.g., moving to the next widget)
            return 'break'

    def create_submit_button(self):
        submit_button_canvas = tk.Canvas(self.party_frame, width=161, height=60, highlightthickness=0, bg='White')
        self.round_rectangle(submit_button_canvas, 0, 0, 150, 50, radius=60, outline="", fill="#9983D5",
                             tags="submit_button")
        # Position the Submit button below the Entry_Grid_frame
        submit_button_canvas.place(x=1100, y=440)  # Adjust the 'y' value based on your requirements
        submit_button_canvas.create_text(75, 25, text="Submit", font=("Sansita One", 24), fill="black")
        submit_button_canvas.bind("<Button-1>", self.submit_pressed)
        submit_button_canvas.bind("<ButtonRelease-1>", self.submit_released)

    def submit_pressed(self, event):
        logging.info("Submit Button Pressed")
        event.widget.itemconfig("submit_button", fill="#D3D3D3")
        # logging.info ("sl no =",len(self.scrollable_frame.grid_slaves(row=1, column=0)[0].get()))
        # logging.info ("Desc = ",len(self.scrollable_frame.grid_slaves(row=1, column=2)[0].get()))
        # Serialize the user input data to JSON

        user_data = {
            "party_details": {
                "party_name": self.party_name_entry.get(),
                "party_address": self.party_address_entry.get("1.0", tk.END),
                "mobile_no": self.mob_no_entry.get(),
                "email": self.email_entry.get(),
                "gstin": self.gstin_entry.get(),
            },
            "invoice_details": {
                "invoice_number": self.Invoice_no.get(),
                "Invoice_date": self.Invoice_date,
                # Add other fields for invoice details
            },
            "item_details": [],
        }

        # Add item details to the user_data
        for row in range(1, self.rows + 1):
            if len(self.scrollable_frame.grid_slaves(row=row, column=0)[0].get()) == 0:
                break
            item = {
                "sl_no": self.scrollable_frame.grid_slaves(row=row, column=0)[0].get(),
                "description": self.scrollable_frame.grid_slaves(row=row, column=1)[0].get(),
                "hsn": self.scrollable_frame.grid_slaves(row=row, column=2)[0].get(),
                "quantity": self.scrollable_frame.grid_slaves(row=row, column=3)[0].get(),
                "unit": self.scrollable_frame.grid_slaves(row=row, column=4)[0].get(),
                "rate": self.scrollable_frame.grid_slaves(row=row, column=5)[0].get(),
                "dis": self.scrollable_frame.grid_slaves(row=row, column=6)[0].get(),
                "gst": self.scrollable_frame.grid_slaves(row=row, column=7)[0].get(),
                "total": self.scrollable_frame.grid_slaves(row=row, column=8)[0].get()

                # Add other fields for item details
            }
            user_data["item_details"].append(item)

        serialized_data = json.dumps(user_data)
        # logging.info(user_data)

        # Add serialized data to the message queue
        # message_queue.put(serialized_data)
        res = backend(serialized_data)
        if res < 0:
            messagebox.showerror("Error", "Error Encountered in saving data")
        else:
            messagebox.showinfo("Success", "Data saved successfully")

    def submit_released(self, event):
        logging.info("Submit Button Released")
        event.widget.itemconfig("submit_button", fill="#6FA1EC")
        self.initialize_gui()

    def button_pressed(self, event):
        global Save_Party_button
        logging.info("Button Pressed")
        event.widget.itemconfig("save_button", fill="#D3D3D3")
        Save_Party_button = 1

    def button_released(self, event):
        global Save_Party_button
        logging.info("Button Released")
        event.widget.itemconfig("save_button", fill="#6FA1EC")
        Save_Party_button = 0

    def send_to_ipc_queue():
        # Your data collection logic remains the same
        data = {
            "invoice_no": invoice_no_entry.get(),
            "vendor": vendor_entry.get(),
            # ... capture other inputs similarly ...
        }

        # Convert dictionary to JSON string
        json_data = json.dumps(data)

        # Create an IPC queue and put the JSON data into it
        ipc_queue.put(json_data)


def backend(message):
    """Process the JSON message and populate an Excel sheet with the extracted details."""
    logging.info("Backend thread is working...")

    try:
        data = json.loads(message)
        logging.info(f"message = {message}")

        # Extracting party details
        vendor = data['party_details']['party_name']

        # Extracting invoice details
        invoice_no = data['invoice_details']['invoice_number']
        date = data['invoice_details']['Invoice_date']

        # Validate date format
        format = "%d-%m-%Y"
        try:
            datetime.strptime(date, format)
        except ValueError:
            logging.info("Incorrect date format, should be dd-mm-yyyy")
            return -1

        # Copy the audit file to a new location

        config = configparser.ConfigParser()

        # Path to the configuration file
        config_file_path = r"C:\Users\AMARJEET\Desktop\python_bill\Config\config.ini.txt"

        # Read the configuration file
        config.read(config_file_path)

        # Get the paths from the configuration file
        source = config.get('PATHS', 'SOURCE_PATH')
        destination = config.get('PATHS', 'DESTINATION_PATH')+"Audit" + invoice_no + ".xlsx"
        logging.info(f"foramate path {source}")
        logging.info(f"destination path: {destination}")
        shutil.copyfile(source, destination)

        # Load the workbook and access the active sheet
        workbook = load_workbook(filename=destination)
        sheet = workbook.active

        # Populate vendor and invoice details in the Excel sheet
        sheet["C2"] = vendor
        sheet["M2"] = vendor
        sheet["U2"] = vendor
        sheet["I3"] = invoice_no
        sheet["M3"] = invoice_no
        sheet["U3"] = invoice_no
        sheet["C3"] = date

        # Extract and populate item details from the JSON
        total_item = len(data['item_details'])
        for i in range(total_item):
            slno = int(data['item_details'][i]['sl_no'])
            description = data['item_details'][i]['description']
            HSN = int(data['item_details'][i]['hsn'])
            D_P = data['item_details'][i]['unit']
            qty_purchased = int(data['item_details'][i]['quantity'])
            rate_purchased = round(float(data['item_details'][i]['rate']), 2)
            disc = round(float(data['item_details'][i]['dis']), 2)
            GST_RATE = round(float(data['item_details'][i]['gst']), 2)
            total_amount = round(float(data['item_details'][i]['total']), 2)

            cell_str_base = str(5 + slno)
            sheet[f"A{cell_str_base}"] = slno
            sheet[f"K{cell_str_base}"] = slno
            sheet[f"R{cell_str_base}"] = slno

            sheet[f"B{cell_str_base}"] = description
            sheet[f"G{cell_str_base}"] = HSN
            sheet[f"H{cell_str_base}"] = qty_purchased
            sheet[f"T{cell_str_base}"] = qty_purchased
            sheet[f"V{cell_str_base}"] = qty_purchased
            sheet[f"I{cell_str_base}"] = rate_purchased
            sheet[f"J{cell_str_base}"] = disc
            sheet[f"S{cell_str_base}"] = GST_RATE
            sheet[f"W{cell_str_base}"] = total_amount
            sheet[f"Y{cell_str_base}"] = round(float(total_amount * GST_RATE / 100), 2)
            sheet[f"U{cell_str_base}"] = 0

        # Save the workbook with populated details
        workbook.save(filename=destination)

    except json.JSONDecodeError as e:
        logging.info(f"Error decoding JSON: {e}")
        return -1
    except Exception as ex:
        logging.info(f"An error occurred: {ex}")
        return -1
    return 1


# Ensure to define and use the message queue in your main program.


if __name__ == "__main__":
    app = PurchaseBillApp()
    app.title("Purchase Bill Entry")
    '''
    producer_thread = threading.Thread(target=app.mainloop())
    consumer_thread = threading.Thread(target=consumer)

    # Start both threads
    consumer_thread.start()
    producer_thread.start()
    consumer_thread.start()

    # Wait for both threads to finish
    producer_thread.join()
    consumer_thread.join()
    '''
    app.mainloop()
    logging.info("Main thread exiting.")

    # app.mainloop()