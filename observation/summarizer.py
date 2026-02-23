def summarize_observations(face_data, eye_data):
    observations = []

    # ---- Guard: missing face scan ----
    if not face_data or "landmarks" not in face_data:
        observations.append("insufficient_facial_data")
        return observations

    landmarks = face_data["landmarks"]

    # =========================
    # 1. Eye fatigue (eye openness)
    # =========================
    try:
        left_eye = landmarks["left_eye"]
        right_eye = landmarks["right_eye"]

        # vertical eye opening (normalized space)
        left_eye_open = abs(left_eye[2][1] - left_eye[3][1])
        right_eye_open = abs(right_eye[2][1] - right_eye[3][1])

        avg_eye_open = (left_eye_open + right_eye_open) / 2

        if avg_eye_open < 0.015:
            observations.append("facial_fatigue_detected")
    except KeyError:
        pass

    # =========================
    # 2. Nasal irritation proxy (nose movement / instability)
    # =========================
    try:
        nose = landmarks["nose"]

        nose_motion = abs(nose[0][1] - nose[-1][1])
        if nose_motion > 0.02:
            observations.append("nasal_irritation_detected")
    except KeyError:
        pass

    # =========================
    # 3. Fever-like pattern (reduced facial activity)
    # =========================
    try:
        mouth = landmarks["mouth"]
        mouth_open = abs(mouth[0][1] - mouth[1][1])

        if mouth_open < 0.01:
            observations.append("fever_like_pattern")
    except KeyError:
        pass

    # =========================
    # 4. Eye scan fusion (if available)
    # =========================
    if eye_data and eye_data.get("eye_redness") == 1:
        observations.append("eye_redness_detected")

    # ---- Fallback ----
    if not observations:
        observations.append("no_visible_facial_anomalies")

    return observations
