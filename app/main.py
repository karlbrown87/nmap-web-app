from flask import Flask, render_template, request, make_response
import nmap
import socket
import json
from weasyprint import HTML

app = Flask(__name__)
nm = nmap.PortScanner()

@app.route('/', methods=['GET', 'POST'])
def index():
    scan_results = None
    if request.method == 'POST':
        target = request.form['target']
        scan_type = request.form['scan_type']
        try:
            # Resolve domain to IP
            try:
                ip = socket.gethostbyname(target)
            except socket.gaierror:
                return render_template('index.html', scan_results=f"Error: Unable to resolve domain '{target}'")

            # Perform scan
            if scan_type == 'quick':
                nm.scan(ip, arguments='-F')
            elif scan_type == 'full':
                nm.scan(ip)

            # Convert scan results to a serializable JSON string
            scan_results = nm[ip]
            scan_results = json.dumps(scan_results, default=str)
        except Exception as e:
            scan_results = json.dumps({"error": str(e)})
    return render_template('index.html', scan_results=scan_results)

def format_scan_results(scan_results):
    if "error" in scan_results:
        return f"<p>Error: {scan_results['error']}</p>"

    # Get host details
    hostnames = scan_results.get('hostnames', [{'name': 'N/A'}])
    addresses = scan_results.get('addresses', {'ipv4': 'N/A'})
    state = scan_results.get('status', {}).get('state', 'N/A')

    # Build a structured HTML table
    formatted_results = '<h2>Scan Results</h2>'
    formatted_results += f'<p><strong>Host:</strong> {hostnames[0]["name"]}</p>'
    formatted_results += f'<p><strong>IP Address:</strong> {addresses.get("ipv4", "N/A")}</p>'
    formatted_results += f'<p><strong>State:</strong> {state}</p>'
    formatted_results += '<table style="width:100%; border-collapse: collapse;">'
    formatted_results += '<tr><th style="border: 1px solid #ddd; padding: 8px;">Port</th>'
    formatted_results += '<th style="border: 1px solid #ddd; padding: 8px;">State</th>'
    formatted_results += '<th style="border: 1px solid #ddd; padding: 8px;">Service</th>'
    formatted_results += '<th style="border: 1px solid #ddd; padding: 8px;">Details</th></tr>'

    for port, details in scan_results.get('tcp', {}).items():
        formatted_results += '<tr>'
        formatted_results += f'<td style="border: 1px solid #ddd; padding: 8px;">{port}/tcp</td>'
        formatted_results += f'<td style="border: 1px solid #ddd; padding: 8px;">{details["state"]}</td>'
        formatted_results += f'<td style="border: 1px solid #ddd; padding: 8px;">{details["name"]}</td>'
        formatted_results += '<td style="border: 1px solid #ddd; padding: 8px;">'
        formatted_results += f'Product: {details.get("product", "N/A")}<br>'
        formatted_results += f'Version: {details.get("version", "N/A")}<br>'
        formatted_results += f'Extra Info: {details.get("extrainfo", "N/A")}'
        formatted_results += '</td>'
        formatted_results += '</tr>'

    formatted_results += '</table>'
    return formatted_results

@app.route('/export', methods=['POST'])
def export_pdf():
    # Get scan results from the form
    scan_results = request.form.get('scan_results', '{}')

    # Safely parse the scan results as JSON
    try:
        scan_results_dict = json.loads(scan_results)
    except json.JSONDecodeError:
        return render_template(
            'index.html',
            scan_results="Invalid scan results provided. Could not parse as JSON.",
        )

    # Format the scan results
    formatted_results = format_scan_results(scan_results_dict)

    # Render the results in an HTML template
    rendered_html = render_template('export.html', scan_results=formatted_results)

    # Convert rendered HTML to PDF
    pdf = HTML(string=rendered_html).write_pdf(stylesheets=['app/static/pdf_styles.css'])

    # Return the PDF file as a response
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=scan_results.pdf'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
