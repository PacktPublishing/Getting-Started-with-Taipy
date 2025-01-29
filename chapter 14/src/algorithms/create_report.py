import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fpdf import FPDF


def create_pdf_report(df, filename="./iframes/report.pdf"):
    """Creates a pdf report from the Andorran hotels DataFrame
    using FPDF
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_fill_color(56, 245, 220)
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, txt="Accommodation Report", ln=True, align="C")

    ##### Convert the DataFrame to a table in the PDF ####
    pdf.ln(10)
    pdf.set_font("Arial", size=10)

    # Table header
    for col in df.columns:
        if col == "parish":
            pdf.cell(40, 10, col, border=3, align="L", fill=True)
        else:
            pdf.cell(25, 10, col, border=3, align="R", fill=True)
    pdf.ln()

    # Table rows
    for i in range(len(df)):
        for col in df.columns:
            if col == "parish":
                pdf.cell(40, 10, str(df[col][i]), border=1, align="L")
            else:
                pdf.cell(25, 10, str(df[col][i]), border=1, align="R")
        pdf.ln()
    #### Table Ends ####

    #### Bart chart with matplotlib ####
    plt.figure(figsize=(6, 4))
    plt.bar(df["parish"], df["total"], color="skyblue")
    plt.xlabel("Parish")
    plt.ylabel("Total Accommodation")
    plt.title("Total Accommodation by Parish")

    # Parish names are a bit long, rotate them a bit:
    plt.xticks(rotation=90)
    plt.tight_layout()

    # Save chart to a file
    chart_filename = "chart.png"

    # dpi 300 is important to have better visuals!
    plt.savefig(chart_filename, dpi=300)
    plt.close()

    # Add the chart image to the PDF
    pdf.ln(10)
    pdf.image(chart_filename, x=10, y=pdf.get_y(), w=180)

    # Output PDF to file
    pdf.output(filename)

    # Once added to pdf, we remove the chart image
    os.remove(chart_filename)
