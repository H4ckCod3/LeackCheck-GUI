import sys
import requests
import customtkinter as ctk
from tkinter import messagebox

LEAKCHECK_API_KEY = "YOUR-KEY-HEARE"

def check_leaks(query, query_type):
    url = f'https://leakcheck.io/api/v2/query/{query}?type={query_type}'
    headers = {'Accept': 'application/json', 'X-API-Key': LEAKCHECK_API_KEY}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {'error': f"API Error: {str(e)}"}

def build_leak_details(leak):
    details = {}
    if leak.get('source', {}).get('name') and leak['source']['name'] != 'Not available':
        details['Source'] = leak['source']['name']
    if leak.get('email') and leak['email'] != 'Not available':
        details['Email'] = leak['email']
    if leak.get('username') and leak['username'] != 'Not available':
        details['Username'] = leak['username']
    if leak.get('password') and leak['password'] != 'Not available':
        details['Password'] = leak['password']
    if leak.get('ip') and leak['ip'] != 'Not available':
        details['IP'] = leak['ip']
    if leak.get('mobile') and leak['mobile'] != 'Not available':
        details['Mobile'] = leak['mobile']
    return details

class LeakCheckerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.bg_color = "#1E1E1E"
        self.default_button_color = "#BB86FC" 
        self.initUI()

    def initUI(self):
        self.title("Vanshy")
        self.geometry("930x530")
        self.configure(bg_color=self.bg_color, fg_color="#121212")

        main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#121212")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
    
        title = ctk.CTkLabel(main_frame, text="Vanshy Osint", font=("Arial", 40, "bold"), text_color="#BB86FC")
        title.grid(row=0, column=0, columnspan=2, pady=(20, 40), sticky="n") 

        top_separator = ctk.CTkFrame(main_frame, height=2, fg_color="#BB86FC")
        top_separator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=5)

        sidebar_frame = ctk.CTkFrame(main_frame, width=20, corner_radius=15, fg_color="transparent")
        sidebar_frame.grid(row=2, column=0, sticky="ns", padx=15, pady=10) 

        ctk.CTkLabel(sidebar_frame, text="", height=1).grid(row=0, column=0) 

        button_texts = ["Email", "Phone", "Username", "IP", "Password"]
        self.buttons = {}
        for i, text in enumerate(button_texts):
            button = ctk.CTkButton(sidebar_frame, text=text, command=lambda t=text: self.setQueryType(t), 
                                   width=200, height=45, corner_radius=12, fg_color=self.default_button_color, hover_color="#1E1E1E",
                                   font=("Arial", 14, "bold"))
            button.grid(row=i+1, column=0, pady=10, padx=15, sticky="ew")
            self.buttons[text] = button

        right_panel = ctk.CTkFrame(main_frame, fg_color="#121212", corner_radius=15)
        right_panel.grid(row=2, column=1, padx=20, pady=10, sticky="nsew")

        input_frame = ctk.CTkFrame(right_panel, fg_color="#121212")
        input_frame.grid(row=0, column=0, pady=20)

        self.input_field = ctk.CTkEntry(input_frame, placeholder_text="Enter data to search", width=500, height=45, corner_radius=12, font=("Arial", 16))
        self.input_field.grid(row=0, column=0, padx=10)

        self.check_button = ctk.CTkButton(input_frame, text="🔍", command=self.onCheck, width=45, height=45, corner_radius=12, 
                                          fg_color=self.default_button_color, hover_color="#1E1E1E", font=("Arial", 16, "bold"))
        self.check_button.grid(row=0, column=1, padx=10)

        separator = ctk.CTkFrame(right_panel, height=2, fg_color="#BB86FC")
        separator.grid(row=1, column=0, sticky="ew", pady=5)

        self.result_area = ctk.CTkTextbox(right_panel, height=200, width=600, wrap="word", state="disabled", font=("Arial", 14))
        self.result_area.grid(row=2, column=0, pady=20)

        bottom_separator = ctk.CTkFrame(main_frame, height=2, fg_color="#BB86FC")
        bottom_separator.grid(row=3, column=0, columnspan=2, sticky="ew", padx=15, pady=10)

        self.query_type = "email"

    def setQueryType(self, query_type):
        self.query_type = query_type.lower()
        self.input_field.configure(placeholder_text=f"Enter {query_type} to search")

    def onCheck(self):
        query = self.input_field.get().strip()
        if query:
            data = check_leaks(query, self.query_type)
            if data.get('success'):
                results = ""
                for leak in data.get('result', []):
                    details = build_leak_details(leak)

                    for key, value in details.items():
                        if key == 'Email':
                            results += f"📧 {key}: {value}\n"
                        elif key == 'Password':
                            results += f"🔑 {key}: {value}\n"
                        elif key == 'Username':
                            results += f"👤 {key}: {value}\n"
                        elif key == 'IP':
                            results += f"🌍 {key}: {value}\n"
                        elif key == 'Mobile':
                            results += f"📱 {key}: {value}\n"
                        elif key == 'Source':
                            results += f"💻 {key}: {value}\n"

                    results += "----------------------------------------\n"  

                self.result_area.configure(state="normal")
                self.result_area.delete(1.0, "end")
                self.result_area.insert("insert", results)
                self.result_area.configure(state="disabled")
            else:
                self.result_area.configure(state="normal")
                self.result_area.delete(1.0, "end")
                self.result_area.insert("insert", "❌ Error occurred")
                self.result_area.configure(state="disabled")
        else:
            self.result_area.configure(state="normal")
            self.result_area.delete(1.0, "end")
            self.result_area.insert("insert", "⚠️ Please enter a query")
            self.result_area.configure(state="disabled")



if __name__ == '__main__':
    app = LeakCheckerApp()
    app.mainloop()
