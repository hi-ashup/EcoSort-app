import google.generativeai as genai
import os
import json
from PIL import Image

# Initialize schema structure for robust JSON parsing
SCHEMA_PROMPT = """
You are EcoSort AI. Analyze the image and provide a JSON output. 
STRICTLY follow this JSON structure:
{
  "itemName": "string",
  "category": "string (e.g., Plastic, Metal, Organic, E-Waste)",
  "recyclabilityScore": "integer (0-100)",
  "dustbinColor": "string (Green, Blue, Red, Yellow - based on international standards)",
  "materialComposition": [
      {"material": "string", "percentage": "integer"}
  ],
  "disposalInstructions": ["string", "string"],
  "environmentalImpact": "string (Short impact statement)",
  "upcyclingIdeas": [
      {"title": "string", "description": "string", "difficulty": "Easy/Medium/Hard"}
  ]
}
Return ONLY valid JSON.
"""

def analyze_image(image_file, api_key):
    """
    sends image to Gemini 1.5 Flash for analysis
    """
    if not api_key:
        return {"error": "API Key Missing"}

    try:
        genai.configure(api_key=api_key)
        # Using Gemini 1.5 Flash for speed/vision capabilities
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Load image with PIL
        img = Image.open(image_file)
        
        # Generate Content
        response = model.generate_content([SCHEMA_PROMPT, img])
        
        # Parse JSON strictly
        clean_text = response.text.strip()
        
        # Handle cases where model puts markdown blocks around json
        if clean_text.startswith("```json"):
            clean_text = clean_text.replace("```json", "").replace("```", "")
        
        data = json.loads(clean_text)
        return data

    except Exception as e:
        return {"error": str(e)}