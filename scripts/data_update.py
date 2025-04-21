# scripts/data_update.py
import os
import subprocess
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define paths
REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
NOTEBOOKS_DIR = os.path.join(REPO_ROOT, "notebooks")
DATA_DIR = os.path.join(REPO_ROOT, "app", "data")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def run_notebook(notebook_path):
    """Execute a notebook via nbconvert and collect output."""
    logger.info(f"Running notebook: {os.path.basename(notebook_path)}")
    
    try:
        # Execute the notebook
        subprocess.run([
            "jupyter", "nbconvert", 
            "--to", "notebook", 
            "--execute",
            "--output", os.path.basename(notebook_path),
            notebook_path
        ], check=True)
        
        logger.info(f"Successfully executed: {os.path.basename(notebook_path)}")
        return True
    
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing notebook {os.path.basename(notebook_path)}: {e}")
        return False

def main():
    """Run all notebooks in sequence."""
    logger.info("Starting data update process...")
    
    # List of notebooks to run in order
    notebooks = [
        "01_data_collection.ipynb",
        "02_fundamental_analysis.ipynb",
        "03_technical_analysis.ipynb",
        "04_news_sentiment.ipynb",
        "05_social_sentiment.ipynb",
        "06_composite_score.ipynb"
    ]
    
    # Run each notebook in sequence
    for notebook in notebooks:
        notebook_path = os.path.join(NOTEBOOKS_DIR, notebook)
        if os.path.exists(notebook_path):
            success = run_notebook(notebook_path)
            if not success:
                logger.warning(f"Failed to run {notebook}. Continuing with next notebook.")
        else:
            logger.warning(f"Notebook not found: {notebook}")
    
    logger.info("Data update process completed")

if __name__ == "__main__":
    main()