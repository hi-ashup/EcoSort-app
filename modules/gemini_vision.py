import google.generativeai as genai
import json
from PIL import Image

def analyze_image(image_file, api_key):
    """
    Analyzes the image using Gemini 1.5 Flash.
    """
    if not api_key:
        return {"error": "API Key Required"}

    try:
        genai.configure(api_key=api_key)
        
        # We use a broader configuration to allow the model to detect which version 
        # is available or fall back. "gemini-1.5-flash" is standard now.
        model_name = "gemini-1.5-flash" 
        
        generation_config = {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096,
            "response_mime_type": "application/json",
        }

        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=generation_config,
        )

        img = Image.open(image_file)

        # REFINED PROMPT to ensure perfect JSON
        prompt = """
        Analyze this waste item. Return JSON only:
        {
            "itemName": "Brief Name",
            "category": "Plastic/Metal/Paper/Organic/E-Waste/Glass",
            "recyclabilityScore": Integer 0-100,
            "dustbinColor": "Green (Organic)/Blue (Recyclable)/Red (Hazard)/Yellow (Metal/Plastic)",
            "materialComposition": [{"material": "name", "percentage": int}],
            "disposalInstructions": ["Step 1", "Step 2"],
            "environmentalImpact": "Short description",
            "upcyclingIdeas": [{"title": "Name", "description": "Short Desc", "difficulty": "Easy/Medium"}]
        }
        """

        response = model.generate_content([prompt, img])
        
        # Cleaning response text just in case
        text_response = response.text.strip()
        if text_response.startswith("```json"):
            text_response = text_response[7:-3]
            
        return json.loads(text_response)

    except Exception as e:
        # Better error visibility
        return {"error": f"AI Processing Failed: {str(e)}"}