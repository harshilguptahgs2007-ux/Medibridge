import os
import json
import logging
from dotenv import load_dotenv
import requests
import base64

# Load .env
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))
load_dotenv(os.path.join(os.path.dirname(BASE_DIR), ".env"))

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    import docx
except ImportError:
    docx = None

logger = logging.getLogger("medibridge.briefer")

# ============================================================
# EMPTY RESULT HELPER
# ============================================================

def empty_result():
    return {
        "summary": "",
        "duration": "",
        "purpose": "",
        "instruction": "",
        "precaution": "",
        "medicines": "",
        "languages": {
            "english": {
                "summary": "",
                "duration": "",
                "purpose": "",
                "instruction": "",
                "precaution": "",
                "medicines": ""
            },
            "hindi": {
                "summary": "",
                "duration": "",
                "purpose": "",
                "instruction": "",
                "precaution": "",
                "medicines": ""
            }
        }
    }


def _get_client():
    if genai is None:
        raise RuntimeError("google-genai is not installed in the active virtual environment")

    api_key = os.getenv("KIMI_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("KIMI_API_KEY is not configured")

    return genai.Client(api_key=api_key)


# ============================================================
# HEALTH REPORT SUMMARY (KIMI POWERED)
# ============================================================

def summarize_health_report(
    report_text="",
    file_paths=None,
    patient_id=None
):
    report_text = report_text or ""
    file_paths = file_paths or []

    # 1. Attempt generation via NVIDIA API Kimi Model
    try:
        api_key = os.getenv("NVIDIA_API_KEY") or os.getenv("KIMI_API_KEY")
        if not api_key:
            raise RuntimeError("API key is not configured")

        contents_list = []
        docx_texts = []
        pdf_texts = []

        for file_path in file_paths:
            if not os.path.isfile(file_path):
                continue

            lower_path = file_path.lower()

            if lower_path.endswith(".docx") and docx is not None:
                try:
                    doc = docx.Document(file_path)
                    full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
                    if full_text:
                        docx_texts.append(f"--- WORD DOCUMENT CONTENT ({os.path.basename(file_path)}) ---\n{full_text}")
                except Exception as e:
                    logger.warning(f"Error reading docx {file_path}: {e}")
                continue

            if lower_path.endswith(".pdf"):
                try:
                    import pymupdf
                    doc = pymupdf.open(file_path)
                    full_text = ""
                    print(f"PDF has {len(doc)} page(s): {os.path.basename(file_path)}")
                    for page_num, page in enumerate(doc):
                        t = page.get_text() or ""
                        print(f"  Page {page_num}: get_text() returned {len(t.strip())} chars")
                        if t.strip():
                            full_text += "\n" + t
                        else:
                            # OCR the page if no text
                            print(f"  Page {page_num}: no text, sending to NVIDIA OCR...")
                            pix = page.get_pixmap()
                            encoded_string = base64.b64encode(pix.tobytes("jpeg")).decode('utf-8')
                            ocr_payload = {
                                "input": [{"type": "image_url", "url": f"data:image/jpeg;base64,{encoded_string}"}]
                            }
                            ocr_resp = requests.post(
                                os.getenv("NVIDIA_OCR_URL", "https://ai.api.nvidia.com/v1/cv/nvidia/nemotron-ocr-v2"),
                                headers={"Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY')}", "Accept": "application/json"},
                                json=ocr_payload,
                                timeout=30
                            )
                            print(f"  OCR status: {ocr_resp.status_code}")
                            if ocr_resp.status_code == 200:
                                ocr_data = ocr_resp.json()
                                # Correct structure: data[0]['text_detections'][i]['text_prediction']['text']
                                for image_result in ocr_data.get("data", []):
                                    for detection in image_result.get("text_detections", []):
                                        txt = detection.get("text_prediction", {}).get("text", "")
                                        if txt:
                                            full_text += txt + "\n"
                                print(f"  OCR extracted {len(full_text)} chars so far")
                            else:
                                print(f"  OCR error body: {ocr_resp.text[:200]}")
                    if full_text.strip():
                        pdf_texts.append(f"--- PDF DOCUMENT CONTENT ({os.path.basename(file_path)}) ---\n{full_text.strip()}")
                        print(f"  Added PDF text: {len(full_text.strip())} chars")
                    else:
                        print(f"  WARNING: no text extracted from PDF!")
                except Exception as e:
                    print(f"Error reading pdf {file_path}: {e}")
                    logger.warning(f"Error reading pdf {file_path}: {e}")
                continue

            if lower_path.endswith((".png", ".jpg", ".jpeg")):
                try:
                    with open(file_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                        ext = "jpeg" if lower_path.endswith(".jpg") else lower_path.split(".")[-1]
                        
                        ocr_payload = {
                            "input": [{"type": "image_url", "url": f"data:image/{ext};base64,{encoded_string}"}]
                        }
                        ocr_resp = requests.post(
                            os.getenv("NVIDIA_OCR_URL", "https://ai.api.nvidia.com/v1/cv/nvidia/nemotron-ocr-v2"),
                            headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
                            json=ocr_payload,
                            timeout=30
                        )
                        if ocr_resp.status_code == 200:
                            ocr_data = ocr_resp.json()
                            extracted_text = ""
                            for image_result in ocr_data.get("data", []):
                                for detection in image_result.get("text_detections", []):
                                    txt = detection.get("text_prediction", {}).get("text", "")
                                    if txt:
                                        extracted_text += txt + "\n"
                            if extracted_text.strip():
                                pdf_texts.append(f"--- IMAGE OCR CONTENT ({os.path.basename(file_path)}) ---\n{extracted_text.strip()}")
                except Exception as e:
                    logger.warning(f"Error reading image {file_path}: {e}")
                continue

        combined_text = report_text
        if docx_texts:
            combined_text = (combined_text + "\n\n" + "\n\n".join(docx_texts)).strip()
        if pdf_texts:
            combined_text = (combined_text + "\n\n" + "\n\n".join(pdf_texts)).strip()

        print(f"Combined document text: {len(combined_text)} chars")

        prompt = """You are an expert medical assistant for MediBridge.
Analyze the provided medical prescription, doctor note, or clinical document in detail.

TASK:
Extract and simplify the medical information in BOTH simple English and natural Hindi (Devanagari script).

IMPORTANT RULES:
1. Do NOT invent medical information. Extract actual medicines, diagnoses, durations, and instructions present in the document.
2. If multiple medicines are listed, include all of them in the 'medicines' field.
3. Return ONLY valid JSON with no markdown formatting.
4. The JSON must have EXACTLY this structure:
{
    "summary": {
        "english": "<Concise 2-3 sentence overview of patient condition, diagnosis, and care plan>",
        "hindi": "<रोगी की स्थिति, निदान और देखभाल योजना का सरल 2-3 वाक्यों में सारांश>"
    },
    "duration": {
        "english": "<Prescribed duration e.g. 5 days, 2 weeks, or As directed>",
        "hindi": "<उपचार की अवधि e.g. 5 दिन, 2 सप्ताह, या चिकित्सक के निर्देशानुसार>"
    },
    "purpose": {
        "english": "<Medical purpose and recommended specialist>",
        "hindi": "<चिकित्सीय उद्देश्य और अनुशंसित विशेषज्ञ>"
    },
    "instruction": {
        "english": "<Specific dosage and timing instructions for each medicine>",
        "hindi": "<प्रत्येक दवा के लिए खुराक और लेने का समय>"
    },
    "precaution": {
        "english": "<Key precautions, dietary advice, warnings>",
        "hindi": "<प्रमुख सावधानियां, खानपान की सलाह और चेतावनियां>"
    },
    "medicines": {
        "english": "<List of medicines with dosage/strength>",
        "hindi": "<दवाइयों के नाम और खुराक>"
    }
}"""

        text_content = prompt + "\n\n"
        if combined_text:
            text_content += f"PATIENT / DOCUMENT TEXT:\n{combined_text}"

        logger.info(f"Sending {len(text_content)} chars to Groq for patient {patient_id}")

        invoke_url = "https://api.groq.com/openai/v1/chat/completions"
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            raise RuntimeError("GROQ_API_KEY not set")

        headers = {
            "Authorization": f"Bearer {groq_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": text_content
                }
            ],
            "model": "qwen/qwen3.8-27b",
            "max_tokens": 4096,
            "temperature": 0.3,
            "stream": False
        }

        response = requests.post(invoke_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        text = data["choices"][0]["message"]["content"].strip()
        print(f"Groq raw response ({len(text)} chars): {text[:200]}")
        if text.startswith("```"):
            lines = text.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            text = "\n".join(lines).strip()
            
        if text.startswith("json"):
            text = text[4:].strip()

        result = json.loads(text)
        final_result = empty_result()
        for field in ["summary", "duration", "purpose", "instruction", "precaution", "medicines"]:
            val = result.get(field, {})
            if isinstance(val, dict):
                eng = str(val.get("english", "") or "")
                hin = str(val.get("hindi", "") or "")
                final_result[field] = eng
                final_result["languages"]["english"][field] = eng
                final_result["languages"]["hindi"][field] = hin
            elif isinstance(val, str):
                final_result[field] = val
                final_result["languages"]["english"][field] = val
                final_result["languages"]["hindi"][field] = val

        if final_result["summary"]:
            return final_result

    except Exception as e:
        print(f"Groq API ERROR: {e}")

    # 2. Local Fallback if Kimi is unavailable
    return _generate_local_brief(report_text, file_paths, patient_id)


def _generate_local_brief(report_text, file_paths, patient_id=None):
    """Build a structured clinical summary from local documents and prescriptions."""
    extracted_text = report_text or ""
    detected_medicines = []
    diagnoses = []
    instructions = []
    precautions = ["Take prescribed doses at scheduled times with water.", "Consult your doctor if you experience adverse symptoms."]

    # Read extracted text from PDF files if available
    if file_paths and PdfReader is not None:
        for fp in file_paths:
            if fp.lower().endswith(".pdf") and os.path.exists(fp):
                try:
                    reader = PdfReader(fp)
                    for page in reader.pages:
                        t = page.extract_text() or ""
                        if t.strip():
                            extracted_text += "\n" + t
                except Exception:
                    pass

    # Search existing patient prescriptions from local database
    if patient_id:
        try:
            rx_path = os.path.join(BASE_DIR, "data", "prescriptions.json")
            if os.path.exists(rx_path):
                with open(rx_path, "r", encoding="utf-8") as f:
                    all_rx = json.load(f)
                p_rx = [r for r in all_rx if r.get("patient_id") == patient_id]
                for r in p_rx:
                    diag = r.get("diagnosis")
                    if diag and diag not in diagnoses:
                        diagnoses.append(diag)
                    for m in r.get("medicines", []):
                        if isinstance(m, dict):
                            name = m.get("name", "Medication")
                            dosage = m.get("dosage", "")
                            freq = m.get("frequency", "")
                            dur = m.get("duration", "")
                            detected_medicines.append(name)
                            instructions.append(f"{name}: {dosage} {freq} ({dur})")
                        else:
                            detected_medicines.append(str(m))
                            instructions.append(str(m))
                    if r.get("advice"):
                        precautions.append(r["advice"])
        except Exception:
            pass

    diag_str = ", ".join(diagnoses) if diagnoses else "General health checkup and symptom evaluation"
    meds_str = ", ".join(list(dict.fromkeys(detected_medicines))) if detected_medicines else "Prescription review on file"
    inst_str = "; ".join(instructions) if instructions else "Follow physician prescribed dosage instructions"
    prec_str = "; ".join(precautions)

    summary_eng = f"Your health records have been reviewed. Record indicates diagnosis of {diag_str}. Follow prescribed treatment guidelines."
    summary_hin = f"आपके स्वास्थ्य रिकॉर्ड की समीक्षा की गई है। रिकॉर्ड के अनुसार स्थिति: {diag_str}। निर्धारित उपचार दिशानिर्देशों का पालन करें।"

    result = empty_result()
    result["summary"] = summary_eng
    result["duration"] = "As advised by consulting physician"
    result["purpose"] = f"Treatment and medical care for {diag_str}"
    result["instruction"] = inst_str
    result["precaution"] = prec_str
    result["medicines"] = meds_str

    result["languages"]["english"] = {
        "summary": summary_eng,
        "duration": "As advised by consulting physician (typically 5-7 days)",
        "purpose": f"Treatment and medical care for {diag_str}",
        "instruction": inst_str,
        "precaution": prec_str,
        "medicines": meds_str
    }

    result["languages"]["hindi"] = {
        "summary": summary_hin,
        "duration": "चिकित्सक के निर्देशानुसार (आमतौर पर 5-7 दिन)",
        "purpose": f"{diag_str} के लिए उपचार एवं चिकित्सकीय परामर्श",
        "instruction": "चिकित्सक द्वारा बताए अनुसार दवा लें।",
        "precaution": "समय पर दवाइयाँ लें एवं लक्षण बढ़ने पर तुरंत डॉक्टर से संपर्क करें।",
        "medicines": meds_str
    }

    return result