from vision.face_scan import face_scan
from vision.eye_scan import eye_scan
from observation.summarizer import summarize_observations
from questionnaire.questions import questionnaire
from decision.health_assessment import assess_health
from decision.otc_advice import otc_advice



def run_cli_pipeline():
    print("\n=== HEALTH AI CLI MODE ===\n")

    print("Step 1: Face Scan")
    face_data = face_scan()
    print("Face Scan Result:", face_data)

    print("\nStep 2: Eye Scan")
    eye_data = eye_scan()
    print("Eye Scan Result:", eye_data)

    print("\nStep 3: Observation Summary")
    observations = summarize_observations(face_data, eye_data)
    print("Observations:", observations)

    print("\nStep 4: Questionnaire")
    question_score = questionnaire(observations)
    print("Questionnaire Score:", question_score)

    status, severity = assess_health(face_data, eye_data, question_score)
    recommendations = otc_advice(severity)

    result = {
        "mode": "cli",
        "face": face_data,
        "eye": eye_data,
        "observations": observations,
        "questionnaire_score": question_score,
        "health_status": status,
        "severity": severity,
        "recommendations": recommendations
    }

    return result


def run_api_pipeline():
    """
    NON-BLOCKING, API-SAFE PIPELINE
    No webcam, no input(), no BLE pairing
    """
    face_data = {"source": "api", "status": "skipped"}
    eye_data = {"source": "api", "status": "skipped"}

    observations = summarize_observations(face_data, eye_data)

    question_score = 5  # default / frontend-driven later

    status, severity = assess_health(face_data, eye_data, question_score)
    recommendations = otc_advice(severity)

    result = {
        "mode": "api",
        "face": face_data,
        "eye": eye_data,
        "observations": observations,
        "questionnaire_score": question_score,
        "health_status": status,
        "severity": severity,
        "recommendations": recommendations
    }

    return result


def main(mode="api"):
    if mode == "cli":
        return run_cli_pipeline()
    else:
        return run_api_pipeline()


if __name__ == "__main__":
    output = main(mode="cli")

    print("\n===== FINAL HEALTH REPORT =====")
    print("Health Status:", output["health_status"])
    print("Severity Level:", output["severity"])
    print("Detected Observations:", output["observations"])

    print("\nRecommendations:")
    for rec in output["recommendations"]:
        print("-", rec)

    print("\nDisclaimer: This system is NOT a medical diagnostic tool.")
