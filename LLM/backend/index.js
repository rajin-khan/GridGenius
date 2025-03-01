const express = require('express');
const { exec } = require('child_process');
const cors = require('cors');

const app = express();
const PORT = 5001;

app.use(cors());  // Enable CORS for all routes

// API endpoint to run the Python script and return analysis
app.get('/api/energy-analysis', (req, res) => {
    exec('python3 /Users/rajin/Developer/UNI/SEM10-MACHINE-LEARNING-PROJECT/LLM/energy_analysis.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).json({ error: error.message });
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return res.status(500).json({ error: stderr });
        }
        console.log(`Stdout: ${stdout}`);
        res.json({ analysis: stdout });
    });
});

app.listen(PORT, () => console.log(`Backend running on http://localhost:${PORT}`));