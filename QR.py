import io
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import barcode
from barcode.writer import ImageWriter
import qrcode


class CodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR & Barcode Generator")
        self.root.geometry("420x520")
        self.root.resizable(False, False)

        self.generated_image = None

        # Title Label
        title_lbl = tk.Label(
            root, text="Code Generator", font=("Helvetica", 16, "bold")
        )
        title_lbl.pack(pady=10)

        # Input Field Section
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10, fill="x", padx=20)

        lbl_input = tk.Label(
            input_frame,
            text="Enter Text / Link / Numbers:",
            font=("Helvetica", 10),
        )
        lbl_input.pack(anchor="w")

        self.entry_data = tk.Entry(input_frame, font=("Helvetica", 11), width=40)
        self.entry_data.pack(fill="x", pady=5)
        self.entry_data.focus()

        # Code Type Selection
        type_frame = tk.LabelFrame(
            root, text=" Select Code Type ", font=("Helvetica", 10, "bold"), padx=10, pady=10
        )
        type_frame.pack(pady=10, fill="x", padx=20)

        self.code_type = tk.StringVar(value="QR Code")

        rb_qr = tk.Radiobutton(
            type_frame,
            text="QR Code",
            variable=self.code_type,
            value="QR Code",
            font=("Helvetica", 10),
        )
        rb_qr.pack(anchor="w", side="left", expand=True)

        rb_barcode = tk.Radiobutton(
            type_frame,
            text="Barcode (Code128)",
            variable=self.code_type,
            value="Barcode",
            font=("Helvetica", 10),
        )
        rb_barcode.pack(anchor="w", side="left", expand=True)

        # Generate Button
        btn_generate = tk.Button(
            root,
            text="Generate Code",
            font=("Helvetica", 11, "bold"),
            bg="#007ACC",
            fg="white",
            activebackground="#005999",
            activeforeground="white",
            command=self.generate_code,
        )
        btn_generate.pack(pady=10, fill="x", padx=20)

        # Preview Display Area
        self.preview_frame = tk.Frame(
            root, width=250, height=200, bg="#F0F0F0", relief="groove", bd=2
        )
        self.preview_frame.pack(pady=10)
        self.preview_frame.pack_propagate(False)

        self.lbl_preview = tk.Label(
            self.preview_frame,
            text="Preview will appear here",
            bg="#F0F0F0",
            fg="#888888",
        )
        self.lbl_preview.pack(expand=True)

        # Save Button
        self.btn_save = tk.Button(
            root,
            text="Save Image",
            font=("Helvetica", 10),
            state=tk.DISABLED,
            command=self.save_code,
        )
        self.btn_save.pack(pady=5)

    def generate_code(self):
        data = self.entry_data.get().strip()

        if not data:
            messagebox.showwarning(
                "Input Error", "Please enter a link, text, or set of numbers."
            )
            return

        selected_type = self.code_type.get()

        try:
            if selected_type == "QR Code":
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=2,
                )
                qr.add_data(data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white").convert(
                    "RGB"
                )
            else:
                code128 = barcode.get_barcode_class("code128")
                barcode_obj = code128(data, writer=ImageWriter())

                buffer = io.BytesIO()
                barcode_obj.write(buffer)
                buffer.seek(0)
                img = Image.open(buffer)

            self.generated_image = img

            preview_img = img.copy()
            preview_img.thumbnail((230, 180))

            tk_img = ImageTk.PhotoImage(preview_img)
            self.lbl_preview.config(image=tk_img, text="")
            self.lbl_preview.image = tk_img

            self.btn_save.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror(
                "Generation Error",
                f"Could not generate {selected_type}:\n{e}\n\nNote: Barcodes have strict character limitations depending on input format.",
            )

    def save_code(self):
        if self.generated_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[
                    ("PNG Image", "*.png"),
                    ("JPEG Image", "*.jpg"),
                    ("All Files", "*.*"),
                ],
            )
            if file_path:
                self.generated_image.save(file_path)
                messagebox.showinfo("Success", f"File saved successfully to:\n{file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorApp(root)
    root.mainloop()