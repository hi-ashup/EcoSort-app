
import { GoogleGenAI, Type } from "@google/genai";
import { WasteAnalysis } from "./types";

// Always initialize with the exact structure required by the SDK
const ai = new GoogleGenAI({ apiKey: process.env.API_KEY || "" });

export async function analyzeWasteImage(base64Image: string): Promise<WasteAnalysis> {
  // Use the specific Gemini 3 Flash preview model as recommended in guidelines for basic text/image tasks
  const modelName = 'gemini-3-flash-preview';
  
  const response = await ai.models.generateContent({
    model: modelName,
    contents: {
      parts: [
        {
          text: `Act as a world-class environmental scientist and waste management expert. 
          Analyze this image to provide a professional-grade waste classification with extreme precision. 
          
          Required JSON output fields:
          1. itemName: Scientific or specific commercial name of the item.
          2. category: General waste stream (Organic, Recyclable, Hazardous, E-waste, Metal, Glass, or Residual).
          3. materialComposition: A brief scientific summary of the primary materials.
          4. detailedMaterials: Array of strings showing estimated percentage breakdown (e.g., "PET Plastic 92%", "Polypropylene Cap 5%", "Paper Label 3%").
          5. disposalInstructions: Professional, step-by-step guide on how to prepare and dispose of the item.
          6. recyclability: Technical rating (e.g., "High - Widely Recycled", "Moderate", or "None").
          7. environmentalImpact: Description of the ecological footprint if improperly disposed of.
          8. ecoTips: Specific 3Rs (Reduce, Reuse, Recycle) advice tailored specifically to this object.
          9. upcyclingIdeas: 3 innovative "best-out-of-waste" project ideas.
          10. dustbinColor: Standard global sorting color (Green, Blue, Yellow, Red, or Black).`
        },
        {
          inlineData: {
            mimeType: "image/jpeg",
            data: base64Image.split(',')[1]
          }
        }
      ]
    },
    config: {
      responseMimeType: "application/json",
      responseSchema: {
        type: Type.OBJECT,
        properties: {
          itemName: { type: Type.STRING },
          category: { type: Type.STRING },
          materialComposition: { type: Type.STRING },
          detailedMaterials: { type: Type.ARRAY, items: { type: Type.STRING } },
          disposalInstructions: { type: Type.ARRAY, items: { type: Type.STRING } },
          recyclability: { type: Type.STRING },
          environmentalImpact: { type: Type.STRING },
          ecoTips: { type: Type.ARRAY, items: { type: Type.STRING } },
          upcyclingIdeas: { type: Type.ARRAY, items: { type: Type.STRING } },
          dustbinColor: { type: Type.STRING, enum: ["Green", "Blue", "Yellow", "Red", "Black"] }
        },
        required: ["itemName", "category", "detailedMaterials", "dustbinColor", "environmentalImpact", "disposalInstructions"]
      }
    }
  });

  // Extract text directly using the .text property as per guidelines
  const text = response.text;
  if (!text) {
    throw new Error("Neural response was empty. The model might have failed to identify the object.");
  }

  try {
    return JSON.parse(text);
  } catch (e) {
    console.error("JSON Parse Error:", text);
    throw new Error("Neural output format was invalid.");
  }
}
