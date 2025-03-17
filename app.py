from flask import Flask, render_template, request, send_file
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, ListFlowable, ListItem

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/create_cv')
def create_cv():
    return render_template('form.html')

@app.route('/generate_cv', methods=['POST'])
def generate_cv():
    user_data = request.form.to_dict(flat=False)  # Collect all inputs with the same name
    
    # Create a PDF using ReportLab
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=inch, leftMargin=inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    # Define styles
    styles = getSampleStyleSheet()
    name_style = ParagraphStyle('NameStyle', parent=styles['Normal'], fontSize=24, alignment=1, spaceAfter=12, leading=28)
    contact_style = ParagraphStyle('ContactStyle', parent=styles['Normal'], fontSize=12, alignment=1, spaceAfter=24)
    section_heading_style = ParagraphStyle('SectionHeadingStyle', parent=styles['Normal'], fontSize=14, spaceBefore=12, spaceAfter=12, leading=16, fontName='Helvetica-Bold')
    body_style = ParagraphStyle('BodyStyle', parent=styles['Normal'], fontSize=12, leading=14)
    bullet_style = ParagraphStyle('BulletStyle', parent=styles['Normal'], fontSize=12, leftIndent=20, leading=14)
    
    # Build the document
    elements = []
    
    # Candidate's Name
    elements.append(Paragraph(user_data.get('name', [''])[0], name_style))
    
    # Contact Details
    contact_details = f"{user_data.get('email', [''])[0]}<br/>{user_data.get('phone', [''])[0]}<br/>{user_data.get('location', [''])[0]}"
    elements.append(Paragraph(contact_details, contact_style))
    
    # New Fields
    elements.append(Paragraph(f"Nationality: {user_data.get('nationality', [''])[0]}", body_style))
    elements.append(Paragraph(f"Languages Spoken: {user_data.get('languages', [''])[0]}", body_style))
    elements.append(Paragraph(f"Marital Status: {user_data.get('marital_status', [''])[0]}", body_style))
    
    # Professional Summary
    elements.append(Paragraph('PROFESSIONAL SUMMARY', section_heading_style))
    elements.append(Paragraph(user_data.get('summary', [''])[0], body_style))
    
    # Work Experience
    elements.append(Paragraph('WORK EXPERIENCE', section_heading_style))
    workplaces = user_data.get('workplace_name', [])
    durations = user_data.get('work_duration', [])
    duties_list = user_data.get('work_duties', [])
    duty_index = 0
    for i in range(len(workplaces)):
        elements.append(Paragraph(f"<b>{workplaces[i]}</b> ({durations[i]})", body_style))
        duties = []
        while duty_index < len(duties_list) and duties_list[duty_index].strip():
            duties.append(duties_list[duty_index].strip())
            duty_index += 1
        duty_index += 1  # Skip the empty entry between different work experiences
        duty_list = ListFlowable([ListItem(Paragraph(duty, bullet_style)) for duty in duties], bulletType='bullet')
        elements.append(duty_list)
        elements.append(Spacer(1, 18))  # Increased space after each work experience
    
    # Education
    elements.append(Paragraph('EDUCATION', section_heading_style))
    education_names = user_data.get('education_name', [])
    education_durations = user_data.get('education_duration', [])
    education_courses = user_data.get('education_course', [])
    education_qualifications = user_data.get('education_qualification', [])
    for i in range(min(len(education_names), len(education_durations), len(education_courses), len(education_qualifications))):
        elements.append(Paragraph(f"<b>{education_names[i]}</b> ({education_durations[i]})<br/>Course/Programme: {education_courses[i]}<br/>{education_qualifications[i]}", body_style))
        elements.append(Spacer(1, 18))  # Increased space after each education entry
    
    # Skills
    elements.append(Paragraph('SKILLS', section_heading_style))
    skills = user_data.get('skills', [])
    skill_list = ListFlowable([ListItem(Paragraph(skill.strip(), bullet_style)) for skill in skills], bulletType='bullet')
    elements.append(skill_list)
    
    # Interests
    elements.append(Paragraph('INTERESTS', section_heading_style))
    interests = user_data.get('interests', [])
    interest_list = ListFlowable([ListItem(Paragraph(interest.strip(), bullet_style)) for interest in interests], bulletType='bullet')
    elements.append(interest_list)
    
    # References
    elements.append(Paragraph('REFERENCES', section_heading_style))
    reference_names = user_data.get('reference_name', [])
    reference_workplaces = user_data.get('reference_workplace', [])
    reference_phones = user_data.get('reference_phone', [])
    for i in range(min(len(reference_names), len(reference_workplaces), len(reference_phones))):
        elements.append(Paragraph(f"{reference_names[i]}<br/>Place of Work: {reference_workplaces[i]}<br/>Telephone: {reference_phones[i]}", body_style))
        elements.append(Spacer(1, 18))  # Increased space after each reference entry
    
    # Build PDF
    doc.build(elements)
    
    pdf_buffer.seek(0)
    # Use the user's full name as the file name
    full_name = user_data.get('name', [''])[0].replace(' ', '_')  # Replace spaces with underscores
    return send_file(pdf_buffer, as_attachment=True, download_name=f'{full_name}_CV.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)