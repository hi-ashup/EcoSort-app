
export interface WasteAnalysis {
  itemName: string;
  category: string;
  materialComposition: string;
  detailedMaterials: string[];
  disposalInstructions: string[];
  recyclability: string;
  environmentalImpact: string;
  ecoTips: string[];
  upcyclingIdeas: string[];
  dustbinColor: 'Green' | 'Blue' | 'Yellow' | 'Red' | 'Black';
}

export type AppTab = 'home' | 'classification' | 'material' | 'instructions' | 'sustainability' | 'innovative';
