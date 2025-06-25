import pikepdf
from PyPDF2 import PdfReader, PdfWriter
import re

# Input PDF
input_pdf = "Global Trends Reader.pdf"

# List of bookmarks and start pages
bookmarks = [
    (1,    "1.01 Pinker - Enlightenment Now"),
    (74,   "2.02 Irwin - Free Trade Under Fire Ch 2"),
    (125,  "3.01 Inglehart and Norris - Trump Brexit and the Rise of Populism"),
    (178,  "4.01 Mankiw - Macroeconomics Ch 4"),
    (198,  "5.01 Brynjolfsson and McAfee - The Second Machine Age Ch 1 and 2"),
    (224,  "5.02 Gordon - Why Has Economic Growth Slowed When Innovation Accelerated"),
    (252,  "6.01 Piketty - Capital in the 21st Century Introduction"),
    (288,  "7.01 National Intelligence Council - Global Trends Paradox of Progress"),
    (493,  "8.01 Baron - Business and Its Environment Ch 6"),
    (524,  "9.01 World Bank - Global Monitoring Report 2015-2016"),
    (575,  "10.01 WMO - Statement on the State of the Global Climate in 2016")
]

# Step 1: Add bookmarks with pikepdf
with pikepdf.open(input_pdf) as pdf:
    outline = pdf.open_outline()
    for page_num, title in bookmarks:
        page = pdf.pages[page_num - 1]  # zero-based index
        outline.root.append(pikepdf.OutlineItem(title, page))
    pdf.save("course_reader_with_bookmarks.pdf")

print("✅ Bookmarks added to course_reader_with_bookmarks.pdf")

# Step 2: Split into chapters using PyPDF2
reader = PdfReader("course_reader_with_bookmarks.pdf")

# Add a dummy end page to simplify split logic
all_bookmarks = bookmarks + [(len(reader.pages) + 1, "END")]

for i in range(len(bookmarks)):
    start_page = all_bookmarks[i][0] - 1  # zero-based
    end_page = all_bookmarks[i + 1][0] - 1
    full_title = all_bookmarks[i][1]
    
    # Remove page number prefix for filename
    # clean_name = re.sub(r"^\d+\.\d+\s+", "", full_title)

    # Use full bookmark name as-is
    clean_name = full_title
    
    # Make it file-safe
    # filename = re.sub(r"[^\w\s-]", "", clean_name).strip().replace(" ", "_") + ".pdf"
    filename = re.sub(r"[^\w\s.-]", "", clean_name).strip() + ".pdf"
    
    # Create PDF writer and add pages
    writer = PdfWriter()
    for j in range(start_page, end_page):
        writer.add_page(reader.pages[j])
    
    # Write the chapter file
    with open(filename, "wb") as f_out:
        writer.write(f_out)

    print(f"✅ Saved: {filename}")