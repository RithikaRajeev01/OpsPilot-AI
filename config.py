import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "catboost_model_final.pkl"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

# ==========================================================
# MODEL SETTINGS
# ==========================================================

THRESHOLD = 0.40

# ==========================================================
# APPLICATION SETTINGS
# ==========================================================

MAX_UPLOAD_SIZE = 20 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    "csv"
}

# ==========================================================
# GEMINI SETTINGS
# ==========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"

# ==========================================================
# APPLICATION DETAILS
# ==========================================================

APP_NAME = "OpsPilot AI"

APP_VERSION = "1.0"

COMPANY_NAME = "OpsPilot AI Enterprise Platform"