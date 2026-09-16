import analyze
import pdf
import ui
import fitz
import os
import threading


REPORT_CSS = """
body { font-family: sans-serif; color: #20252b; font-size: 10pt; }
h1 { color: #173f5f; font-size: 22pt; margin-bottom: 4pt; }
h2 { color: #20639b; font-size: 13pt; border-bottom: 1pt solid #b8c7d1; padding-bottom: 3pt; margin-top: 14pt; }
p { line-height: 1.35; }
table { width: 100%; border-collapse: collapse; margin-top: 6pt; }
th { background-color: #173f5f; color: white; text-align: left; padding: 5pt; }
td { border-bottom: 0.6pt solid #cbd5da; padding: 5pt; vertical-align: top; }
tr:nth-child(even) { background-color: #f1f5f7; }
.summary { background-color: #e8f1f5; border-left: 4pt solid #20639b; padding: 8pt; }
.warning { color: #8a5a00; }
.bad { color: #9b2c2c; }
.good { color: #226b3b; }
.muted { color: #68757d; }
"""

def write_review_pdf(html, output_path):
    document = fitz.open()
    page = document.new_page()
    page.insert_htmlbox(page.rect, f"<style>{REPORT_CSS}</style>{html}")
    document.save(output_path)
    document.close()

def analyze_file(file_path, loading_window):
    images = pdf.pdf_to_images(file_path)
    text = pdf.image_to_text(images)
    review = analyze.generate_ai_review(text)

    write_review_pdf(review, "review.pdf")
    finish_analysis()

def finish_analysis():
    root.destroy()

def main():
    global root
    root = None

    def start_analysis(file_path):
        loading_window = ui.show_loading_dots(root)
        threading.Thread(
            target=analyze_file,
            args=(file_path, loading_window),
            daemon=True
        ).start()

    root = ui.init_window(start_analysis)
    root.mainloop()


if __name__ == "__main__":
    main()
    os.startfile(os.path.abspath("review.pdf"))