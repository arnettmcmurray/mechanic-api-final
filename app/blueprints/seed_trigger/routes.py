from flask import Blueprint, jsonify
from app.seed import seed_data
import traceback

seed_trigger_bp = Blueprint("seed_trigger_bp", __name__, url_prefix="/seed")

@seed_trigger_bp.route("/", methods=["POST"])
def trigger_seed():
    """Run existing seed_data() safely on Render and print tracebacks."""
    try:
        seed_data()
        return jsonify({"message": "Seed executed successfully"}), 200
    except Exception as e:
        print("❌ Seed failed:", e)
        traceback.print_exc()
        return jsonify({
            "error": str(e),
            "details": traceback.format_exc()
        }), 500
