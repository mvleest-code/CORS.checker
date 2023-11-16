from flask import Flask, request, jsonify, render_template_string
import requests
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/check_cors', methods=['POST'])
def check_cors():
    data = request.get_json()
    url = data['url']
    domains = data['domain'].split(',')

    parsed_url = urlparse(url)
    mediaBaseUrl = parsed_url.netloc

    results = {}

    for domain in domains:
        domain = domain.strip()  # Remove leading/trailing whitespace

        headers = {
            'authority': mediaBaseUrl,
            'accept': '/',
            'accept-language': 'en',
            'access-control-request-headers': 'authorization',
            'access-control-request-method': 'GET',
            'origin': domain,
            'referer': domain,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
        }

        try:
            response = requests.options(url, headers=headers)
        except requests.exceptions.RequestException as e:
            results[domain] = {'error': str(e)}
            continue

        if ('access-control-allow-origin' in response.headers and 
            response.headers['access-control-allow-origin'] == domain and 
            'access-control-allow-credentials' in response.headers and 
            response.headers['access-control-allow-credentials'] == 'true'):
            results[domain] = {'result': 'CORS WHITELIST CHECK SUCCESS'}
        else:
            results[domain] = {'result': 'CORS WHITELIST CHECK FAILED'}

    return jsonify(results)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>CORS whitelist checker</title>
          <style>
        body {
            font-family: Roboto, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #F7F8FC;
        }
        .container {
            text-align: center;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            width: 450px;
        }
        input[type="text"] {
            margin: 10px 0;
            padding: 10px;
            width: 250px;
            background-color: #F7F8FC;
        }
        button {
            padding: 10px 20px;
            background-color: #0082C3;
            color: #fff;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #0082C3;
            color: #E3E9EF;
        }
    </style>
        <script>
            function checkCORS() {
                const url = document.getElementById('url').value;
                const domain = document.getElementById('domain').value;

                fetch('/check_cors', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({url: url, domain: domain}),
                })
                .then(response => response.json())
                .then(data => {
                    let message = '';
                    for (const [domain, result] of Object.entries(data)) {
                        message += domain + ': ' + (result.error || result.result) + '\\n';
                    }
                    alert(message);
                })
                .catch(error => {
                    alert('Error: ' + error.message);
                });
            }
        </script>
    </head>
    <body>
        <div class="container">
        <h1>CORS Checker v1.2</h1>
        <label for="url">Enter MEDIA URL:</label><br>
        <input type="text" id="url" value="https://media.c000.eagleeyenetworks.com"><br>
        <label for="domain">Enter CORS Domain(s):</label><br>
        <input type="text" id="domain" placeholder="Enter domains separated by commas"><br>
        <button onclick="checkCORS()">Check CORS</button>
    </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=5000)
