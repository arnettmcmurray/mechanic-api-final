from flask import Blueprint, jsonify
from app.seed import seed_data

# Match your other blueprints’ pattern
seed_trigger_bp = Blueprint("seed_trigger_bp", __name__, url_prefix="/seed")

@seed_trigger_bp.route("/", methods=["POST"])
def trigger_seed():
    """Run existing seed_data() safely on Render."""
    try:
        seed_data()
        return jsonify({"message": "Seed executed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
