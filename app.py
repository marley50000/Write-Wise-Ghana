from flask import Flask, render_template, request, send_file
from io import BytesIO
from fpdf import FPDF

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
    
    # Create a PDF using FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Candidate's Name
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(200, 10, txt=user_data.get('name', [''])[0], ln=True, align='C')
    
    # Contact Details
    pdf.set_font("Arial", size=12)
    contact_details = f"Email: {user_data.get('email', [''])[0]}\nPhone: {user_data.get('phone', [''])[0]}\nLocation: {user_data.get('location', [''])[0]}"
    pdf.multi_cell(0, 10, txt=contact_details)
    
    # New Fields
    pdf.multi_cell(0, 10, txt=f"Nationality: {user_data.get('nationality', [''])[0]}")
    pdf.multi_cell(0, 10, txt=f"Languages Spoken: {user_data.get('languages', [''])[0]}")
    pdf.multi_cell(0, 10, txt=f"Marital Status: {user_data.get('marital_status', [''])[0]}")
    
    # Professional Summary
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, txt='PROFESSIONAL SUMMARY', ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=user_data.get('summary', [''])[0])
    
    # Work Experience
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, txt='WORK EXPERIENCE', ln=True)
    pdf.set_font("Arial", size=12)
    workplaces = user_data.get('workplace_name', [])
    durations = user_data.get('work_duration', [])
    duties_list = user_data.get('work_duties', [])
    duty_index = 0
    for i in range(len(workplaces)):
        pdf.cell(0, 10, txt=f"{workplaces[i]} ({durations[i]})", ln=True)
        while duty_index < len(duties_list) and duties_list[duty_index].strip():
            pdf.multi_cell(0, 10, txt=f"- {duties_list[duty_index].strip()}")
            duty_index += 1
        duty_index += 1  # Skip the empty entry between different work experiences
    
    # Education
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, txt='EDUCATION', ln=True)
    pdf.set_font("Arial", size=12)
    education_names = user_data.get('education_name', [])
    education_durations = user_data.get('education_duration', [])
    education_courses = user_data.get('education_course', [])
    education_qualifications = user_data.get('education_qualification', [])
    for i in range(min(len(education_names), len(education_durations), len(education_courses), len(education_qualifications))):
        pdf.multi_cell(0, 10, txt=f"{education_names[i]} ({education_durations[i]})\nCourse/Programme: {education_courses[i]}\n{education_qualifications[i]}")
    
    # Skills
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, txt='SKILLS', ln=True)
    pdf.set_font("Arial", size=12)
    skills = user_data.get('skills', [])
    for skill in skills:
        pdf.multi_cell(0, 10, txt=f"- {skill.strip()}")
    
    # Interests
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, txt='INTERESTS', ln=True)
    pdf.set_font("Arial", size=12)
    interests = user_data.get('interests', [])
    for interest in interests:
        pdf.multi_cell(0, 10, txt=f"- {interest.strip()}")
    
    # References
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, txt='REFERENCES', ln=True)
    pdf.set_font("Arial", size=12)
    reference_names = user_data.get('reference_name', [])
    reference_workplaces = user_data.get('reference_workplace', [])
    reference_phones = user_data.get('reference_phone', [])
    for i in range(min(len(reference_names), len(reference_workplaces), len(reference_phones))):
        pdf.multi_cell(0, 10, txt=f"{reference_names[i]}\nPlace of Work: {reference_workplaces[i]}\nTelephone: {reference_phones[i]}")
    
    # Save PDF to buffer
    pdf_buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    pdf_buffer.write(pdf_output)
    pdf_buffer.seek(0)
    
    # Use the user's full name as the file name
    full_name = user_data.get('name', [''])[0].replace(' ', '_')  # Replace spaces with underscores
    return send_file(pdf_buffer, as_attachment=True, download_name=f'{full_name}_CV.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
