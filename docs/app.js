let pyodide = null;
let isInitialized = false;

// Initialize Pyodide when the page loads
async function initPyodide() {
    updateStatus('Loading Python environment...', 'loading');
    
    try {
        pyodide = await loadPyodide();
        
        // Load required packages
        await pyodide.loadPackage(['micropip']);
        
        // Install the aicad package dependencies
        await pyodide.runPythonAsync(`
            import micropip
            await micropip.install('typing-extensions')
            await micropip.install('dataclasses-json')
        `);
        
        // Load the aicad package code directly
        const moduleFiles = [
            '__init__.py',
            'ir.py',
            'compose.py',
            'dsl_parse.py',
            'refine.py',
            'validate.py',
            'compile_fs.py',
            'compile_cadquery.py',
            'verify.py',
            'init.py'
        ];
        
        // Fetch all module files from GitHub
        // Note: This URL points to the main branch. For testing with forks/branches, update this URL.
        const baseUrl = 'https://raw.githubusercontent.com/yossideutsch1973/ai-cad-compiler/main/src/aicad/';
        
        for (const file of moduleFiles) {
            try {
                const response = await fetch(baseUrl + file);
                if (!response.ok) {
                    throw new Error(`Failed to fetch ${file}: ${response.status}`);
                }
                const content = await response.text();
                pyodide.FS.writeFile(`/home/pyodide/aicad/${file}`, content);
            } catch (error) {
                console.error(`Error loading ${file}:`, error);
                throw error;
            }
        }
        
        // Create the aicad package directory
        pyodide.FS.mkdir('/home/pyodide/aicad', { recursive: true });
        
        // Set up the Python path
        await pyodide.runPythonAsync(`
            import sys
            sys.path.insert(0, '/home/pyodide')
        `);
        
        isInitialized = true;
        updateStatus('Ready! Enter a design intent and click Compile.', 'success');
        enableCompileButton();
    } catch (error) {
        console.error('Error initializing Pyodide:', error);
        updateStatus(`Error initializing: ${error.message}. Please refresh the page.`, 'error');
    }
}

function updateStatus(message, type) {
    const status = document.getElementById('status');
    status.textContent = message;
    status.className = `status ${type}`;
}

function enableCompileButton() {
    const btn = document.getElementById('compile-btn');
    btn.disabled = false;
}

function disableCompileButton() {
    const btn = document.getElementById('compile-btn');
    btn.disabled = true;
    document.getElementById('btn-text').style.display = 'none';
    document.getElementById('btn-spinner').style.display = 'block';
}

function enableCompileButtonAfterRun() {
    const btn = document.getElementById('compile-btn');
    btn.disabled = false;
    document.getElementById('btn-text').style.display = 'block';
    document.getElementById('btn-spinner').style.display = 'none';
}

async function compileIntent() {
    if (!isInitialized) {
        updateStatus('Still initializing... Please wait.', 'loading');
        return;
    }
    
    const intent = document.getElementById('intent').value.trim();
    
    if (!intent) {
        updateStatus('Please enter a design intent.', 'error');
        return;
    }
    
    disableCompileButton();
    updateStatus('Compiling design...', 'loading');
    
    try {
        // Pass the intent as a Python variable to avoid injection issues
        pyodide.globals.set('user_intent', intent);
        
        // Run the compilation
        const result = await pyodide.runPythonAsync(`
from aicad import compile_all
import json

result = compile_all(user_intent)

# Convert result to JSON-friendly format
output = {
    "featurescript": result["featurescript"],
    "cadquery": result["cadquery"],
    "status": "OK" if result["report"].ok else "INVALID",
    "errors": [str(e) for e in result["report"].errors] if hasattr(result["report"], 'errors') else []
}
json.dumps(output)
        `);
        
        const output = JSON.parse(result);
        
        // Display outputs
        document.getElementById('featurescript-output').textContent = output.featurescript;
        document.getElementById('cadquery-output').textContent = output.cadquery;
        
        if (output.status === 'OK') {
            updateStatus('✓ Compilation successful!', 'success');
        } else {
            updateStatus(`⚠ Compilation completed with warnings: ${output.errors.join(', ')}`, 'error');
        }
    } catch (error) {
        console.error('Compilation error:', error);
        updateStatus(`Error: ${error.message}`, 'error');
        document.getElementById('featurescript-output').textContent = '';
        document.getElementById('cadquery-output').textContent = '';
    } finally {
        enableCompileButtonAfterRun();
    }
}

// Initialize when the page loads
window.addEventListener('DOMContentLoaded', () => {
    disableCompileButton();
    initPyodide();
});

// Allow Enter key in textarea to trigger compilation (with Ctrl/Cmd)
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('intent').addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            compileIntent();
        }
    });
});
