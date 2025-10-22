def paraphrase_with_mistral(text, model, max_tokens=2000, temperature=0.7):
    """
    Robust paraphrasing function compatible with LM Studio chat-completion API.
    Cleans malformed or truncated responses gracefully.
    """

    import re
    import json
    import html

    system_prompt = (
        "You are an expert academic writer. Paraphrase the following text while:\n"
        "- Preserving all citations (e.g., Author et al., Year)\n"
        "- Maintaining all numerical values and statistics\n"
        "- Keeping technical terminology intact\n"
        "- Enhancing clarity and readability\n"
        "- Using varied sentence structures\n"
        "- Maintaining the original meaning and tone.\n"
        "Return only the paraphrased text. Do not include control symbols, tags, or markers."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text}
    ]

    try:
        # use chat completions endpoint for stable models
        response = requests.post(
            "http://localhost:1234/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": model,
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.95,
                "stream": False
            },
            timeout=180
        )

        response.raise_for_status()
        data = response.json()

        # Try multiple fallback paths depending on model output shape
        raw_text = ""
        if "choices" in data:
            choice = data["choices"][0]
            if "message" in choice and "content" in choice["message"]:
                raw_text = choice["message"]["content"]
            elif "text" in choice:
                raw_text = choice["text"]
        elif "text" in data:
            raw_text = data["text"]

        # --- CLEANUP PHASE ---
        if not raw_text:
            return "⚠️ Model returned no text. Try increasing max_tokens or lowering temperature."

        text_clean = html.unescape(raw_text)

        # remove known junk tokens or pseudo markers
        text_clean = re.sub(r"(?i)(UL|BLET|BLETER|LET|SECTION|LIST|ENDLIST|::|--|###|@@@|\\|\/)+", " ", text_clean)
        text_clean = text_clean.replace("<s>", "").replace("</s>", "")
        text_clean = text_clean.replace("[INST]", "").replace("[/INST]", "")
        text_clean = text_clean.replace("ASSISTANT:", "").replace("USER:", "")
        text_clean = text_clean.replace("```", "").replace("**", "")
        text_clean = text_clean.strip()

        # remove repeating garbage patterns
        text_clean = re.sub(r"([A-Z]{3,}\s*){3,}", "", text_clean)
        text_clean = re.sub(r"([:;.,-])\1{1,}", r"\1", text_clean)

        # collapse multiple spaces
        text_clean = re.sub(r"\s{2,}", " ", text_clean).strip()

        # heuristic fix for truncation (unfinished sentence)
        if not text_clean.endswith(('.', '!', '?', '”', '."')):
            text_clean += "."

        return text_clean

    except requests.exceptions.RequestException as e:
        return f"❌ Connection error: {e}"
    except json.JSONDecodeError:
        return "⚠️ Response was malformed JSON. Try rerunning."
    except Exception as e:
        return f"⚠️ Unexpected error: {str(e)}"
