from flask import Flask, request, jsonify, render_template_string
import requests
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/check_cors', methods=['POST'])
def check_cors():
    data = request.get_json()
    domains = data['domain'].split(',')

    urls = [
        'https://media.c000.eagleeyenetworks.com',
        'https://media.c001.eagleeyenetworks.com',
        'https://media.c003.eagleeyenetworks.com',
        'https://media.c004.eagleeyenetworks.com',
        'https://media.c005.eagleeyenetworks.com',
        'https://media.c006.eagleeyenetworks.com',
        'https://media.c007.eagleeyenetworks.com',
        'https://media.c012.eagleeyenetworks.com',
        'https://media.c013.eagleeyenetworks.com',
        'https://media.c014.eagleeyenetworks.com',
        'https://media.c015.eagleeyenetworks.com',
        'https://media.c016.eagleeyenetworks.com',
        'https://media.c017.eagleeyenetworks.com',
        'https://media.c018.eagleeyenetworks.com',
        'https://media.c019.eagleeyenetworks.com',
        'https://media.c020.eagleeyenetworks.com',
        'https://media.c021.eagleeyenetworks.com',
        'https://media.c022.eagleeyenetworks.com',
        'https://media.c023.eagleeyenetworks.com',
        'https://media.c024.eagleeyenetworks.com',
        'https://media.c025.eagleeyenetworks.com',
        'https://media.c026.eagleeyenetworks.com',
        'https://media.c027.eagleeyenetworks.com'
    ]

    all_results = []

    for url in urls:
        parsed_url = urlparse(url)
        mediaBaseUrl = url

        domain_results = {}

        for domain in domains:
            domain = domain.strip()
            domain = domain.rstrip('/')

            if not domain.startswith('http://') and not domain.startswith('https://'):
                domain = 'https://' + domain

            headers = {
                'authority': parsed_url.netloc,
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
                print(f"Check for {domain} on {url}: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Error for {domain} on {url}: {e}")
                domain_results[domain] = {'error': str(e)}
                continue

            if ('access-control-allow-origin' in response.headers and
                    response.headers['access-control-allow-origin'] == domain and
                    'access-control-allow-credentials' in response.headers and
                    response.headers['access-control-allow-credentials'] == 'true'):
                domain_results[domain] = {'result': 'CORS WHITELIST CHECK SUCCESS'}
            else:
                domain_results[domain] = {'result': 'CORS WHITELIST CHECK FAILED'}

        all_results.append({url: domain_results})

    return jsonify(all_results)

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>CORS whitelist checker</title>
    <link rel="icon" href="https://www.m-cloud.nl/favicon.ico">
    <style>
        body {
            font-family: Roboto, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #F7F8FC;
        }
        .container {
            text-align: center;
            background-color: #fff;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            width: 450px;
            min-height: 215px;
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
        button:disabled {
            background-color: #ccc;
            cursor: not-allowed;
        }
        button:hover:enabled {
            background-color: #0082C3;
            color: #E3E9EF;
        }
        #results-container {
            margin-left: 10px;
            margin-top: 10px;
            margin-bottom: 10px;
            width: 800px;
            min-height: 215px;
            max-height: 800px;
            overflow-y: scroll;
            background-color: #fff;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            position: relative;
        }
        .result {
            margin-bottom: 1px;
        }
    </style>
<script>
async function checkCORS() {
    const domain = document.getElementById('domain').value;
    let resultsContainer = document.getElementById('results-container');
    let checkCORSButton = document.getElementById('check-cors-button');

    checkCORSButton.disabled = true;

    try {
        const response = await fetch('/check_cors', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ domain: domain }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseBody = await response.text();

        const data = JSON.parse(responseBody);

        resultsContainer.innerHTML = '';

        for (const resultItem of data) {
            const url = Object.keys(resultItem)[0];
            const domains = resultItem[url];

            let labelDiv = document.createElement('div');
            labelDiv.textContent = `Results for ${url}:`;
            labelDiv.style.fontWeight = 'bold';
            resultsContainer.appendChild(labelDiv);

            for (const [domain, result] of Object.entries(domains)) {
                let resultDiv = document.createElement('div');
                resultDiv.className = 'result';

                const resultText = result.error
                    ? `Error: ${result.error}`
                    : `Result: ${result.result.trim()}`;

                resultDiv.textContent = `${domain}: ${resultText}`;
                resultDiv.style.color = result.result && result.result.trim() === 'CORS WHITELIST CHECK SUCCESS' ? 'green' : 'red';
                resultsContainer.appendChild(resultDiv);
            }
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        checkCORSButton.disabled = false;
    }
}
</script>
</head>
<body>
    <div class="container">
        <h1>CORS Checker v1.4</h1>
        <label for="domain">Enter CORS Domain(s):</label><br>
        <input type="text" id="domain" placeholder="Enter domains separated by commas"><br>
        <button id="check-cors-button" onclick="checkCORS()">Check CORS</button>
    </div><br>
    
    <div id="results-container">
        <label for="results-container">Press "Check CORS" to show the results here.</label>
    </div>
</body>
</html>

    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
