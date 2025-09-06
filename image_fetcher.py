import requests
import os
from datetime import datetime
from urllib.parse import urlparse
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import io

class ImageFetcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Ubuntu Image Fetcher")
        self.root.geometry("800x600")
        self.root.configure(bg='#f5f5f5')
        
        # Setup main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Ubuntu Image Fetcher", 
                               font=("Segoe UI", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Description
        desc_label = ttk.Label(main_frame, 
                              text="A tool for effortlessly collecting images from the web",
                              font=("Segoe UI", 10))
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # URL input
        url_label = ttk.Label(main_frame, text="Image URL:", font=("Segoe UI", 10))
        url_label.grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50, font=("Consolas", 9))
        url_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Fetch button
        fetch_btn = ttk.Button(main_frame, text="Fetch Image", command=self.fetch_image)
        fetch_btn.grid(row=3, column=1, padx=(10, 0), pady=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to fetch images")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=("Segoe UI", 9), foreground="gray")
        status_label.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # Image preview
        preview_label = ttk.Label(main_frame, text="Image Preview:", font=("Segoe UI", 10))
        preview_label.grid(row=5, column=0, sticky=tk.W, pady=(0, 5))
        
        self.preview_frame = ttk.Frame(main_frame, relief=tk.SUNKEN, width=400, height=300)
        self.preview_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        self.preview_frame.grid_propagate(False)
        
        self.image_label = ttk.Label(self.preview_frame, text="No image preview available", 
                                    background="white", anchor=tk.CENTER)
        self.image_label.pack(expand=True, fill=tk.BOTH)
        
        # Save options
        save_frame = ttk.Frame(main_frame)
        save_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.filename_var = tk.StringVar(value="downloaded_image.jpg")
        filename_entry = ttk.Entry(save_frame, textvariable=self.filename_var, width=30, font=("Consolas", 9))
        filename_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        browse_btn = ttk.Button(save_frame, text="Browse", command=self.browse_save_location)
        browse_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Save button
        save_btn = ttk.Button(main_frame, text="Save Image", command=self.save_image)
        save_btn.grid(row=8, column=0, columnspan=2, pady=(0, 10))
        
        # Console output
        console_label = ttk.Label(main_frame, text="Console Output:", font=("Segoe UI", 10))
        console_label.grid(row=9, column=0, sticky=tk.W, pady=(0, 5))
        
        # Console text widget
        self.console_text = tk.Text(main_frame, height=8, width=70, font=("Consolas", 9), 
                                   relief=tk.SUNKEN, wrap=tk.WORD)
        self.console_text.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for console
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.console_text.yview)
        scrollbar.grid(row=10, column=2, sticky=(tk.N, tk.S))
        self.console_text.configure(yscrollcommand=scrollbar.set)
        
        # Footer message
        footer_label = ttk.Label(main_frame, text="Connection strengthened. Community enriched.", 
                                font=("Segoe UI", 9, "italic"), foreground="gray")
        footer_label.grid(row=11, column=0, columnspan=2, pady=(20, 0))
        
        # Initialize variables
        self.fetched_image = None
        self.image_data = None
        
        # Configure tags for console text
        self.console_text.tag_configure("success", foreground="green")
        self.console_text.tag_configure("error", foreground="red")
        
    def fetch_image(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter an image URL")
            return
            
        self.log_to_console(f"Fetching image from: {url}", "info")
        self.status_var.set("Fetching image...")
        self.root.update()
        
        try:
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            # Get image data
            self.image_data = response.content
            
            # Create image for preview
            image = Image.open(io.BytesIO(self.image_data))
            image.thumbnail((400, 300))
            photo = ImageTk.PhotoImage(image)
            
            # Update preview
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo  # Keep a reference
            
            # Suggest filename
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            self.filename_var.set(filename)
            
            self.fetched_image = image
            self.log_to_console(f"Successfully fetched: {filename}", "success")
            self.status_var.set("Image fetched successfully")
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error fetching image: {e}"
            self.log_to_console(error_msg, "error")
            self.status_var.set("Error fetching image")
            messagebox.showerror("Error", error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            self.log_to_console(error_msg, "error")
            self.status_var.set("Error processing image")
            messagebox.showerror("Error", error_msg)
            
    def save_image(self):
        if self.image_data is None:
            messagebox.showerror("Error", "No image to save. Please fetch an image first.")
            return
            
        filename = self.filename_var.get().strip()
        if not filename:
            messagebox.showerror("Error", "Please specify a filename")
            return
            
        try:
            # Open file dialog if no path specified
            if not os.path.isabs(filename):
                filepath = filedialog.asksaveasfilename(
                    initialfile=filename,
                    defaultextension=".jpg",
                    filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
                )
                if not filepath:
                    return
            else:
                filepath = filename
                
            # Save the image
            with open(filepath, 'wb') as f:
                f.write(self.image_data)
                
            self.log_to_console(f"Image saved to {filepath}", "success")
            self.status_var.set(f"Image saved to {os.path.basename(filepath)}")
            messagebox.showinfo("Success", f"Image successfully saved to {filepath}")
            
        except Exception as e:
            error_msg = f"Error saving image: {e}"
            self.log_to_console(error_msg, "error")
            self.status_var.set("Error saving image")
            messagebox.showerror("Error", error_msg)
            
    def browse_save_location(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filepath:
            self.filename_var.set(filepath)
            
    def log_to_console(self, message, msg_type="info"):
        tag = msg_type
        if msg_type == "info":
            tag = ""
            
        self.console_text.insert(tk.END, message + "\n", tag)
        self.console_text.see(tk.END)

def main():
    root = tk.Tk()
    app = ImageFetcher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
