from flask import Flask, render_template_string, send_file
from weasyprint import HTML, CSS
import io

app = Flask(__name__)

@app.route('/generate_pdf')
def generate_pdf():
    # Define the content
    content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resume</title>
        <style>
            body {
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                color: #333;
                background-color: #f9f9f9;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
            }
            .container {
                width: 60%;
                background-color: #fff;
                padding: 40px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
            }
            h1 {
                color: #2E86C1;
                font-size: 36px;
                margin-bottom: 10px;
                text-align: center;
            }
            h2, h3, h4 {
                color: #1F618D;
                border-bottom: 2px solid #2E86C1;
                padding-bottom: 5px;
                margin-top: 30px;
                margin-bottom: 10px;
            }
            .contact-info {
                margin-bottom: 30px;
                font-size: 14px;
                text-align: center;
            }
            .section {
                margin-bottom: 20px;
            }
            .section p {
                margin: 5px 0;
            }
            .section ul {
                margin: 10px 0;
                padding-left: 20px;
            }
            .section ul li {
                margin-bottom: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Akinpelu Adedamola</h1>
            </div>
            <div class="contact-info">
                <p>Lagos, Nigeria</p>
                <p>Phone: +(234)7061774623</p>
                <p>Email: adedamolabasit09@gmail.com</p>
                <p>GitHub: <a href="https://www.github.com/adedamolabasit">www.github.com/adedamolabasit</a></p>
                <p>Personal Site: <a href="https://www.adedamola.site">www.adedamola.site</a></p>
            </div>

            <div class="section">
                <h2>Objective</h2>
                <p>Dynamic and solution-oriented Software Engineer with comprehensive experience in backend engineering, frontend development, and full stack projects. Specializes in developing RESTful APIs, optimizing database performance, and implementing responsive, high-performance interfaces. Seeking to leverage software expertise and keen interest in semiconductor technologies to contribute to ASM's innovation-driven projects as a Software Support Engineer.</p>
            </div>

            <div class="section">
                <h2>Education</h2>
                <p><strong>Bachelor of Science, Surveying and Geoinformatics</strong></p>
                <p>Obafemi Awolowo University, Ile-Ife, Nigeria</p>
                <p>July 2016 - 2021</p>
            </div>

            <div class="section">
                <h2>Experience</h2>
                <p><strong>Blockops Network, Lagos, NG — Backend Engineer</strong></p>
                <p>January 2022 - PRESENT</p>
                <ul>
                    <li>Engineered RESTful APIs integrating third-party services, boosting functionality and user experience.</li>
                    <li>Enhanced database performance through strategic query optimization, achieving a 40% reduction in load times.</li>
                    <li>Advocated for and implemented Test-Driven Development (TDD), improving code quality and maintainability.</li>
                    <li>Participated actively in code reviews, elevating team standards through constructive feedback.</li>
                </ul>

                <p><strong>Stable Borrow, Remote — Senior Frontend Engineer</strong></p>
                <p>September 2021 - June 2022</p>
                <ul>
                    <li>Pioneered frontend codebase establishment, laying the groundwork for project scalability and development.</li>
                    <li>Facilitated advanced integration between frontend applications and blockchain smart contracts.</li>
                    <li>Drove the integration of external APIs, enlarging project scope and functionalities.</li>
                    <li>Translated complex UI/UX designs into responsive interfaces, ensuring high application performance.</li>
                </ul>

                <p><strong>Nautilus Technologies, Lagos, NG — Full Stack Developer</strong></p>
                <p>September 2020 - PRESENT</p>
                <ul>
                    <li>Developed and maintained critical website infrastructure, emphasizing security and efficiency.</li>
                    <li>Collaborated in an agile team, delivering iterative updates and enhancements in a fast-paced environment.</li>
                </ul>
            </div>

            <div class="section">
                <h2>Skills</h2>
                <p><strong>Languages:</strong> JavaScript, Python, Solidity, Rust, C, C++, C#</p>
                <p><strong>Frameworks:</strong> Node.js, Express.js, Flask, FastAPI, Django, React.js, Tailwind, Redux</p>
                <p><strong>Database Management:</strong> MySQL, PostgreSQL, SQLite, MongoDB, Redis</p>
                <p><strong>Tools:</strong> GitHub, GitLab, Bitbucket, Arduino</p>
                <p><strong>Development Practices:</strong> REST API Development, Test-Driven Development (TDD), Continuous Integration</p>
            </div>

            <div class="section">
                <h2>Awards and Recognitions</h2>
                <ul>
                    <li>Second runner-up in XDC category, Web3athon</li>
                    <li>Chainlink Bounty Award, Moonbeam (Polkadot) platform, "Bear Necessities Hackathon"</li>
                    <li>Stellar Swap Bounty in Moonbeam (Polkadot) platform, "Bear Necessities Hackathon"</li>
                    <li>AWS Honorable Mention, Fantom Hackathon Q2 2023</li>
                </ul>
            </div>

            <div class="section">
                <h2>Additional Information</h2>
                <p><strong>Languages:</strong> Fluent in English</p>
                <p><strong>Availability:</strong> Willing to work at and travel to customer sites, committed to minimum 4 days at the field office weekly.</p>
            </div>
        </div>
    </body>
    </html>
    '''

    # Convert HTML to PDF
    html = HTML(string=content)
    css = CSS(string='''
        @page { size: A4; margin: 2cm; }
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    ''')

    pdf_file = html.write_pdf(stylesheets=[css])

    return send_file(
        io.BytesIO(pdf_file),
        attachment_filename="resume.pdf",
        as_attachment=True,
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    app.run(debug=True)
