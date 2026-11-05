# run_sample.ps1 - Run the sample input automatically
# Usage: First set your key: $env:GROQ_API_KEY="your_key_here"
# Then run: .\run_sample.ps1

$input = "Priya`nPython, HTML, basic SQL`nMachine learning, statistics`nData Scientist"
$input | python app.py

