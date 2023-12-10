

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# Constants
STYLES = getSampleStyleSheet()
TITLE_STYLE = STYLES["Heading1"]
TEXT_STYLE = STYLES["BodyText"]
TITLE_COLOR = "#333333"
TEXT_COLOR = "#666666"
LIGHT_TEXT_COLOR = "#999999"
DARK_TEXT_COLOR = "#333333"
PAGE_WIDTH, PAGE_HEIGHT = 610, 1000

def initialize_pdf(output_file):
    pdf_canvas = canvas.Canvas(output_file, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    return pdf_canvas, PAGE_WIDTH, PAGE_HEIGHT

def add_logo_and_company_info(pdf_canvas, page_height):
    # Add company logo
    logo_path = "CRMapp/static/img/logo-PhotoRoom.png-PhotoRoom.png"
    pdf_canvas.drawInlineImage(logo_path, 0.4 * inch, page_height - 1.25 * inch, width=75, height=75)

    # Add company name and information
    company_name = "Atlas Elevators Factory L.L.C"
    pdf_canvas.setFont(TITLE_STYLE.fontName, TITLE_STYLE.fontSize)
    pdf_canvas.setFillColor(TITLE_COLOR)
    pdf_canvas.drawString(1.2 * inch, page_height - 0.75 * inch, company_name)

    additional_info = "Manufacturing, Installation & Maintenance"
    pdf_canvas.setFont(TEXT_STYLE.fontName, TEXT_STYLE.fontSize)
    pdf_canvas.setFillColor(TEXT_COLOR)
    pdf_canvas.drawString(1.2 * inch, page_height - 0.95 * inch, additional_info)

    company_info = {
        "Dubai Tel.": "+971 4 3469311",
        "Maintenance - Tel.": "+971 55 7204884 ",
        "Emergency - Tel.": "+971 55 4110653 ",
        "Email": "info@atlaselevators.org",
        "Web": "www.atlaselevators.org",
    }

    info_y_position = page_height - 0.6 * inch
    for key, value in company_info.items():
        pdf_canvas.setFont(TEXT_STYLE.fontName, TEXT_STYLE.fontSize)
        pdf_canvas.setFillColor(TEXT_COLOR)
        pdf_canvas.drawString(PAGE_WIDTH - 2.5 * inch, info_y_position, f"{key}: {value}")
        info_y_position -= TEXT_STYLE.leading

    return info_y_position

def draw_horizontal_line(pdf_canvas, y_position):
    pdf_canvas.line(inch, y_position, letter[0] - inch, y_position)

def draw_title(pdf_canvas, title_text, TITLE_STYLE, title_color, line_y_position):
    title_width = pdf_canvas.stringWidth(title_text, TITLE_STYLE.fontName, TITLE_STYLE.fontSize)
    title_x_position = (PAGE_WIDTH - title_width) / 2
    title_y_position = line_y_position - 0.4 * inch

    pdf_canvas.setFont(TITLE_STYLE.fontName, TITLE_STYLE.fontSize)
    pdf_canvas.setFillColor(title_color)
    pdf_canvas.drawString(title_x_position, title_y_position, title_text)

    return title_y_position

def draw_information(pdf_canvas, date, report_number, line_y_position):
    pdf_canvas.setFont(TEXT_STYLE.fontName, 14)
    pdf_canvas.setFillColor(DARK_TEXT_COLOR)
    pdf_canvas.drawString(inch + 5 * inch, line_y_position - 25, "Date:")

    pdf_canvas.setFillColor(LIGHT_TEXT_COLOR)
    pdf_canvas.drawString(letter[0] - 2 * inch, line_y_position - 25, date)

    pdf_canvas.setFillColor(DARK_TEXT_COLOR)
    pdf_canvas.drawString(inch, line_y_position - 25, "NO:")

    pdf_canvas.setFillColor("#FF0000")
    pdf_canvas.drawString(inch + 0.5 * inch, line_y_position - 25, report_number)

def draw_city_project_name(pdf_canvas,city,project_id,name,mobile_phone, line_y_position):
    

    pdf_canvas.setFont(TEXT_STYLE.fontName, 15)
    pdf_canvas.setFillColor(DARK_TEXT_COLOR)

    pdf_canvas.drawString(inch, line_y_position - TEXT_STYLE.leading - 35, f"City: {city}")
    pdf_canvas.drawString(inch + 5 * inch, line_y_position - TEXT_STYLE.leading - 35, f"Project ID: {project_id}")

    pdf_canvas.drawString(inch, line_y_position - TEXT_STYLE.leading - 60, f"Name: {name}")

    pdf_canvas.drawString(inch, line_y_position - TEXT_STYLE.leading - 85, f"Mobile Phone: {mobile_phone}")

def draw_sections_data(pdf_canvas, y_position, data):
    sections = list(data.keys())

    draw_horizontal_line(pdf_canvas, y_position + 0.01 * TITLE_STYLE.leading)
    y_position -= 2 * TITLE_STYLE.leading

    check_list_title = "Check List For Service Visit"
    title_width = pdf_canvas.stringWidth(check_list_title, TITLE_STYLE.fontName, TITLE_STYLE.fontSize)
    title_x_position = (letter[0] - title_width) / 2
    pdf_canvas.setFont(TITLE_STYLE.fontName, TITLE_STYLE.fontSize)
    pdf_canvas.setFillColor(TITLE_COLOR)
    pdf_canvas.drawString(title_x_position, y_position, check_list_title)
    y_position -= 1.5 * TITLE_STYLE.leading

    for i in range(0, len(sections), 2):
        section1 = sections[i]
        section2 = sections[i + 1] if i + 1 < len(sections) else None

        pdf_canvas.setFont(TITLE_STYLE.fontName, TITLE_STYLE.fontSize - 5)
        pdf_canvas.setFillColor(TITLE_COLOR)
        pdf_canvas.drawString(0.5 * inch, y_position, section1)

        if section2:
            pdf_canvas.drawString(5 * inch, y_position, section2)

        y_position -= TITLE_STYLE.leading

        attributes1 = data[section1]
        attributes2 = data[section2] if section2 else {}

        max_attributes = max(len(attributes1), len(attributes2))

        for j in range(max_attributes):
            if j < len(attributes1):
                attribute, value = list(attributes1.items())[j]
                symbol = "✔" if value else "✘"
                color = "#008000" if value else "#FF0000"
                pdf_canvas.setFont(TEXT_STYLE.fontName, TEXT_STYLE.fontSize + 1)
                pdf_canvas.setFillColor(color)
                pdf_canvas.drawString(inch, y_position, f"{attribute}: {symbol}")

            if section2 and j < len(attributes2):
                attribute, value = list(attributes2.items())[j]
                symbol = "✔" if value else "✘"
                color = "#008000" if value else "#FF0000"
                pdf_canvas.setFont(TEXT_STYLE.fontName, TEXT_STYLE.fontSize + 1)
                pdf_canvas.setFillColor(color)
                pdf_canvas.drawString(5.5 * inch, y_position, f"{attribute}: {symbol}")

            y_position -= TEXT_STYLE.leading

        y_position -= TITLE_STYLE.leading

    draw_horizontal_line(pdf_canvas, y_position + 0.5 * TITLE_STYLE.leading)
    return y_position

def draw_remarks(pdf_canvas, remarks_content, y_position):
    pdf_canvas.setFont(TITLE_STYLE.fontName, TITLE_STYLE.fontSize - 5)
    pdf_canvas.setFillColor(TITLE_COLOR)
    pdf_canvas.drawString(0.5 * inch, y_position, "Remarks : ")
    y_position -= 0.1 * TITLE_STYLE.leading

    pdf_canvas.setFont(TEXT_STYLE.fontName, TITLE_STYLE.fontSize - 5)
    pdf_canvas.setFillColor(TEXT_COLOR)

    remarks_lines = remarks_content.split("\n")
    for line in remarks_lines:
        pdf_canvas.drawString(0.5 * inch, y_position, line)
        y_position -= 1.2 * TEXT_STYLE.leading

    y_position -= 0.2 * TITLE_STYLE.leading

def draw_signatures(pdf_canvas,signatures):
    signature_positions = [
        {"name": "TECHNICIAN", "x": inch, "y": 0.1 * inch},
        {"name": "CLIENT", "x": 3.5 * inch, "y": 0.1 * inch},
        {"name": "SUPERVISOR", "x": 6 * inch, "y": 0.1 * inch},
    ]

    for index, signature_position in enumerate(signature_positions):
        signature_label = f"{signature_position['name']} Signature"
        pdf_canvas.setFont(TEXT_STYLE.fontName, TITLE_STYLE.fontSize - 5)
        pdf_canvas.setFillColor(TITLE_COLOR)
        pdf_canvas.drawString(signature_position['x'] - 10, signature_position['y'] + 0.2 * inch, signature_label)

        signature_path = signatures[index]
        pdf_canvas.drawImage(signature_path, signature_position['x'], signature_position['y'] + 0.5 * inch, width=100, height=50)

def create_report(data,
                date,
                report_number,
                city,
                project_id,
                name,
                mobile_phone,
                remarks_content,
                signatures,
                output_file="maintenance_report.pdf"):
    pdf_canvas, PAGE_WIDTH, page_height = initialize_pdf(output_file)

    info_y_position = add_logo_and_company_info(pdf_canvas, page_height)

    draw_horizontal_line(pdf_canvas, info_y_position + 0.08 * inch)



    title_y_position = draw_title(pdf_canvas, "Maintenance Report", TITLE_STYLE, TITLE_COLOR, info_y_position)

    draw_information(pdf_canvas, date, report_number, title_y_position - 7)

    draw_city_project_name(pdf_canvas,city,project_id,name,mobile_phone, title_y_position - 7)

    y_position = draw_sections_data(pdf_canvas, title_y_position - 5.5 * TITLE_STYLE.leading, data)

    draw_remarks(pdf_canvas, remarks_content, y_position - 10)

    draw_signatures(pdf_canvas,signatures)

    return pdf_canvas

if __name__ == "__main__":
    data = {
        "Machine Room Maintenance:": {
            "Hoist Ropes": False,
            "Coupling": True,
            "Points of Lubrication": True,
            "Control Board": True,
            "Fuses": True,
            "Motor Protection": True,
        },
        "Traction Room Maintenance:": {
            "Governor Rope": True,
            "Is Break": True,
            "Gear Bearing": True,
        },
        "Hydraulic Room Maintenance:": {
            "Piston Units": True,
            "Oil Change": True,
            "Pump": True,
            "Valve": True,
        },
        "Pit Maintenance:": {
            "Cleanliness": True,
            "Buffers": True,
            "Limit Switch": True,
            "Safety Link": True,
            "Under Drive": True,
            "Points of Lubrication": True,
        },
        "Run The Lift Maintenance:": {
            "Landing Calls Signals": True,
            "Door Outside Hangers": True,
            "Door Close Photocell": True,
            "Leveling": True,
            "C.O.P Lights": True,
            "Condition of Car": True,
            "Smooth and Soundless Run": True,
            "Start Stop Process": True,
            "Door Switch Looking Device": True,
        },
        "Shaft and Car Maintenance:": {
            "Clean Lines": True,
            "Final Limits": True,
            "Car Switch": True,
            "Car Insulation": True,
            "Safety Device Link Age": False,
            "Operation of Safety Device": True,
            "Door Operation": True,
            "Door Locks": True,
            "Door Inside": True,
            "Shaft Switches": True,
            "Guide Rails Car": True,
            "Guide Rails Shoes Car": True,
            "Door Inside": True,
            "Traveling Cable": True,
        },
    }

    create_report(data)
    print("Report generated successfully.")
