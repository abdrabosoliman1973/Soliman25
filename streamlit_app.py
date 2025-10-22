import re

def paraphrase_with_mistral(text, max_tokens=2000, temperature=0.7):
    """
    Paraphrase text using the Paraphrase-Mistral7B model.
    
    Parameters:
    - text: The text to paraphrase
    - max_tokens: Maximum tokens to generate
    - temperature: Sampling temperature (0.0-1.0)
    
    Returns:
    - Cleaned paraphrased text
    """
    prompt = f"""<s>[INST] You are an expert academic writer. Paraphrase the following text while:\n- Preserving all citations (e.g., Author et al., Year)\n- Maintaining all numerical values and statistics\n- Keeping technical terminology intact\n- Enhancing clarity and readability\n- Using varied sentence structures\n- Maintaining the original meaning and tone\n\nText to paraphrase:\n{text}\n\nProvide only the paraphrased text without any introductory phrases. [/INST]</s>\n"""
    response = paraphrase_model(
        prompt,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=0.9,
        repeat_penalty=1.1,
        stop=["\n<", "</s>", "[INST]", "Section::", "UL::", "UL", "BLETER", "Prov by", "BERER", "LETER"],
        echo=False
    )
    txt = response['choices'][0]['text'].replace("[/INST]", "").strip()
    # Clean artifacts - aggressively filter as in app
    for stop_token in ["Section::", "UL::", "UL-", "BLETER", 'Prov by', 'LETER', 'BERER']:
        idx = txt.find(stop_token)
        if idx != -1:
            txt = txt[:idx]
    lines = txt.split('\n')
    cleaned = []
    for line in lines:
        if (
            not line.strip() or
            re.match(r'^[^a-zA-Z]*$', line) or
            'UL::' in line or 'Section::' in line or 'Prov by' in line or 'BLETER' in line or 'LETER' in line or 'BERER' in line
        ):
            continue
        if re.match(r'^(?:\s*[A-Z]\s*){5,}$', line.strip()):
            continue
        cleaned.append(line)
    txt = ' '.join(cleaned).strip()
    sentences = re.findall(r'([A-Z][^.!?\n]{7,}[.!?])', txt)
    if sentences:
        return ' '.join(sentences)
    return txt if txt else '(No meaningful content returned, try a shorter or different input prompt.)'

print("✅ Paraphrasing function updated for strict artifact cleanup!")
print("\nUsage: paraphrase_with_mistral(your_text)")