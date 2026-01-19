
import React, { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  Button, 
  IconButton, 
  Drawer, 
  List, 
  ListItem, 
  ListItemButton, 
  ListItemIcon, 
  ListItemText, 
  ThemeProvider, 
  createTheme, 
  CssBaseline,
  CircularProgress,
  LinearProgress,
  Paper,
  Alert,
  Stack
} from '@mui/material';
import { 
  Camera, 
  RefreshCw, 
  Trash2, 
  BookOpen, 
  Leaf, 
  Lightbulb, 
  Upload, 
  Microscope, 
  ChevronRight, 
  Zap,
  LayoutDashboard
} from 'lucide-react';
import { AppTab, WasteAnalysis } from './types';
import { analyzeWasteImage } from './geminiService';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#10b981' },
    secondary: { main: '#1976d2' },
    background: { default: '#05080d', paper: '#0a1018' },
    text: { primary: '#f8fafc', secondary: '#94a3b8' },
  },
  typography: {
    fontFamily: '"Outfit", "Roboto", "Helvetica", "Arial", sans-serif',
    h4: { fontWeight: 700, letterSpacing: '-0.02em' },
    h5: { fontWeight: 700 },
    overline: { letterSpacing: '0.3em', fontWeight: 900, fontSize: '0.65rem' },
    body2: { lineHeight: 1.6 },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: 'rgba(255, 255, 255, 0.02)',
          backdropFilter: 'blur(16px)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          borderRadius: 24,
          transition: 'all 0.3s ease',
        }
      }
    },
    MuiButton: {
      styleOverrides: {
        root: { borderRadius: 12, textTransform: 'none', fontWeight: 600 }
      }
    }
  }
});

const DRAWER_WIDTH = 280;

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<AppTab>('classification');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [image, setImage] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<WasteAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      setError("Optic sensor offline. Camera access denied.");
    }
  };

  const captureImage = () => {
    if (videoRef.current && canvasRef.current) {
      const context = canvasRef.current.getContext('2d');
      if (context) {
        canvasRef.current.width = videoRef.current.videoWidth;
        canvasRef.current.height = videoRef.current.videoHeight;
        context.drawImage(videoRef.current, 0, 0);
        const dataUrl = canvasRef.current.toDataURL('image/jpeg');
        setImage(dataUrl);
        handleAnalysis(dataUrl);
      }
    }
  };

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        const dataUrl = event.target?.result as string;
        setImage(dataUrl);
        handleAnalysis(dataUrl);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleAnalysis = async (base64: string) => {
    setIsAnalyzing(true);
    setError(null);
    try {
      const result = await analyzeWasteImage(base64);
      setAnalysis(result);
    } catch (err) {
      setError("AI core initialization failed. Verify network connection.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const resetScanner = () => {
    setImage(null);
    setAnalysis(null);
    setActiveTab('classification');
    startCamera();
  };

  useEffect(() => {
    startCamera();
  }, []);

  const navItems = [
    { id: 'classification', label: 'Classification', icon: <Trash2 size={20} /> },
    { id: 'material', label: 'Material Composition', icon: <Microscope size={20} /> },
    { id: 'instructions', label: 'Disposal Protocol', icon: <BookOpen size={20} /> },
    { id: 'sustainability', label: 'Eco Strategy', icon: <Leaf size={20} /> },
    { id: 'innovative', label: 'Upcycling Lab', icon: <Lightbulb size={20} /> },
  ];

  const renderContent = () => {
    if (isAnalyzing) {
      return (
        <Stack alignItems="center" justifyContent="center" sx={{ height: '100%', py: 8 }}>
          <Box sx={{ position: 'relative', mb: 4 }}>
            <CircularProgress size={80} thickness={2} sx={{ color: 'primary.main' }} />
            <Box sx={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Zap size={30} style={{ color: '#10b981' }} />
            </Box>
          </Box>
          <Typography variant="overline" color="primary" sx={{ mb: 1 }}>Decompiling Molecular Data...</Typography>
          <Typography variant="body2" color="text.secondary" align="center">Parsing high-density image for material signatures</Typography>
        </Stack>
      );
    }

    if (!analysis) {
      return (
        <Stack alignItems="center" justifyContent="center" sx={{ height: '100%', opacity: 0.3 }}>
          <Box sx={{ p: 6, borderRadius: '50%', bgcolor: 'rgba(16, 185, 129, 0.05)', mb: 3 }}>
            <LayoutDashboard size={80} />
          </Box>
          <Typography variant="overline">Select an input source to initiate scan</Typography>
        </Stack>
      );
    }

    switch (activeTab) {
      case 'classification':
        return (
          <Stack spacing={4}>
            <Card sx={{ p: 1, position: 'relative', overflow: 'hidden' }}>
              <Box sx={{ position: 'absolute', top: -20, right: -20, opacity: 0.05 }}>
                <Trash2 size={160} />
              </Box>
              <CardContent>
                {/* Fixed Grid usage from Grid2 to Grid */}
                <Grid container spacing={4} alignItems="center">
                  <Grid item>
                    <Paper 
                      elevation={0}
                      sx={{ 
                        width: 100, 
                        height: 100, 
                        borderRadius: 6, 
                        display: 'flex', 
                        alignItems: 'center', 
                        justifyContent: 'center',
                        bgcolor: analysis.dustbinColor.toLowerCase() === 'black' ? '#111' : analysis.dustbinColor.toLowerCase(),
                        color: 'white',
                        boxShadow: `0 10px 30px -5px ${analysis.dustbinColor.toLowerCase()}`
                      }}
                    >
                      <Trash2 size={48} />
                    </Paper>
                  </Grid>
                  <Grid item xs>
                    <Typography variant="overline" color="primary">Neural ID Success</Typography>
                    <Typography variant="h4" sx={{ mb: 1 }}>{analysis.itemName}</Typography>
                    <Typography variant="body2" color="text.secondary">{analysis.category} Stream Identified</Typography>
                  </Grid>
                </Grid>

                <Grid container spacing={2} sx={{ mt: 5 }}>
                  <Grid item xs={12} sm={6}>
                    <Box sx={{ p: 3, borderRadius: 5, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)' }}>
                      <Typography variant="overline" color="text.secondary" sx={{ display: 'block', mb: 1 }}>Recyclability</Typography>
                      <Typography variant="h6" sx={{ fontSize: '1rem' }}>{analysis.recyclability}</Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <Box sx={{ p: 3, borderRadius: 5, bgcolor: 'rgba(255,255,255,0.03)', border: '1px solid rgba(255,255,255,0.05)' }}>
                      <Typography variant="overline" color="text.secondary" sx={{ display: 'block', mb: 1 }}>Env. Impact</Typography>
                      <Typography variant="h6" sx={{ fontSize: '1rem' }}>{analysis.environmentalImpact}</Typography>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>

            <Box sx={{ p: 4, borderRadius: 8, bgcolor: 'rgba(16, 185, 129, 0.03)', border: '1px solid rgba(16, 185, 129, 0.1)' }}>
               <Typography variant="overline" color="primary" sx={{ mb: 3, display: 'block' }}>Sort Target Mapping</Typography>
               <Stack direction="row" spacing={1.5} sx={{ height: 10 }}>
                {['green', 'blue', 'yellow', 'red', 'black'].map(c => (
                  <Box 
                    key={c} 
                    sx={{ 
                      flex: 1, 
                      borderRadius: 2, 
                      bgcolor: c, 
                      opacity: analysis.dustbinColor.toLowerCase() === c ? 1 : 0.08,
                      transform: analysis.dustbinColor.toLowerCase() === c ? 'scaleY(1.8)' : 'none',
                      transition: 'all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)'
                    }} 
                  />
                ))}
               </Stack>
            </Box>
          </Stack>
        );
      case 'material':
        return (
          <Stack spacing={3}>
            <Alert icon={<Microscope size={20} />} severity="info" sx={{ bgcolor: 'rgba(25, 118, 210, 0.1)', borderRadius: 5, color: 'info.light' }}>
              <Typography variant="body2">{analysis.materialComposition}</Typography>
            </Alert>
            {analysis.detailedMaterials.map((mat, i) => (
              <Card key={i} sx={{ border: 'none', bgcolor: 'rgba(255,255,255,0.01)' }}>
                <CardContent sx={{ py: 3 }}>
                  <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
                    <Typography variant="body1" sx={{ fontWeight: 700 }}>{mat}</Typography>
                    <Typography variant="overline" color="text.secondary">DETECTION STRENGTH</Typography>
                  </Stack>
                  <LinearProgress 
                    variant="determinate" 
                    value={100 - (i * 12)} 
                    sx={{ height: 6, borderRadius: 3, bgcolor: 'rgba(255,255,255,0.05)' }} 
                  />
                </CardContent>
              </Card>
            ))}
          </Stack>
        );
      case 'instructions':
        return (
          <Stack spacing={2.5}>
            {analysis.disposalInstructions.map((step, i) => (
              <Card key={i} sx={{ borderLeft: '4px solid #10b981', bgcolor: 'rgba(16, 185, 129, 0.02)' }}>
                <CardContent sx={{ display: 'flex', gap: 4, alignItems: 'center', py: 3 }}>
                  <Typography variant="h4" color="primary" sx={{ opacity: 0.3, fontStyle: 'italic' }}>0{i+1}</Typography>
                  <Typography variant="body1" sx={{ fontWeight: 500 }}>{step}</Typography>
                </CardContent>
              </Card>
            ))}
          </Stack>
        );
      default:
        return (
          <Stack spacing={2.5}>
            {(activeTab === 'sustainability' ? analysis.ecoTips : analysis.upcyclingIdeas).map((text, i) => (
              <Card key={i} sx={{ '&:hover': { bgcolor: 'rgba(16, 185, 129, 0.08)', transform: 'translateX(8px)' } }}>
                <CardContent sx={{ display: 'flex', gap: 4, alignItems: 'center', py: 3 }}>
                  <Box sx={{ color: activeTab === 'sustainability' ? 'primary.main' : '#facc15' }}>
                    {activeTab === 'sustainability' ? <Leaf size={28} /> : <Lightbulb size={28} />}
                  </Box>
                  <Typography variant="body1" sx={{ flexGrow: 1, fontWeight: 500 }}>{text}</Typography>
                  <ChevronRight size={20} style={{ opacity: 0.3 }} />
                </CardContent>
              </Card>
            ))}
          </Stack>
        );
    }
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
        {/* Permanent Sidebar Drawer */}
        <Drawer
          variant="permanent"
          sx={{
            width: DRAWER_WIDTH,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: DRAWER_WIDTH,
              boxSizing: 'border-box',
              borderRight: '1px solid rgba(255, 255, 255, 0.08)',
              bgcolor: '#080c14',
              p: 4,
              display: 'flex',
              flexDirection: 'column'
            },
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2.5, mb: 8 }}>
            <Box sx={{ p: 1, bgcolor: 'primary.main', borderRadius: 3, boxShadow: '0 0 20px rgba(16, 185, 129, 0.4)' }}>
              <Leaf size={24} color="white" />
            </Box>
            <Typography variant="h5" sx={{ letterSpacing: '-0.05em' }}>EcoScan</Typography>
          </Box>

          <List sx={{ px: 0, flexGrow: 1 }}>
            {navItems.map((item) => (
              <ListItem key={item.id} disablePadding sx={{ mb: 2 }}>
                <ListItemButton 
                  selected={activeTab === item.id}
                  onClick={() => setActiveTab(item.id as AppTab)}
                  sx={{ 
                    borderRadius: 4,
                    px: 3,
                    '&.Mui-selected': { 
                      bgcolor: 'rgba(16, 185, 129, 0.1)', 
                      color: 'primary.main',
                      '&:hover': { bgcolor: 'rgba(16, 185, 129, 0.15)' }
                    },
                    py: 2
                  }}
                >
                  <ListItemIcon sx={{ minWidth: 48, color: activeTab === item.id ? 'inherit' : 'text.secondary' }}>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText 
                    primary={item.label} 
                    primaryTypographyProps={{ variant: 'overline', fontSize: '0.6rem' }} 
                  />
                </ListItemButton>
              </ListItem>
            ))}
          </List>

          <Box sx={{ pt: 4 }}>
            <Button 
              fullWidth 
              variant="outlined" 
              startIcon={<RefreshCw size={18} />}
              onClick={resetScanner}
              sx={{ py: 2, borderColor: 'rgba(255,255,255,0.1)', borderRadius: 4 }}
            >
              Reset Core
            </Button>
          </Box>
        </Drawer>

        {/* Main Dashboard Container */}
        <Box component="main" sx={{ flexGrow: 1, p: 5, height: '100vh', display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          {/* Fixed Grid usage from Grid2 to Grid */}
          <Grid container spacing={5} sx={{ height: '100%' }}>
            
            {/* Input Viewport (Camera/Image) */}
            <Grid item xs={12} md={5} lg={4} sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              <Card sx={{ p: 4, bgcolor: 'rgba(25, 118, 210, 0.05)', borderColor: 'rgba(25, 118, 210, 0.15)' }}>
                <Typography variant="h5" sx={{ mb: 1.5 }}>Neural Scanner</Typography>
                <Typography variant="body2" color="text.secondary">
                  Real-time molecular analysis module. Align item within scan-frame or upload data.
                </Typography>
              </Card>

              <Box 
                className={`pulse-frame ${isAnalyzing ? 'analyzing' : ''}`}
                sx={{ 
                  flex: 1, 
                  position: 'relative', 
                  borderRadius: 10, 
                  overflow: 'hidden', 
                  border: '1px solid rgba(255,255,255,0.1)',
                  bgcolor: 'black',
                  boxShadow: '0 30px 60px rgba(0,0,0,0.6)'
                }}
              >
                {!image ? (
                  <Box sx={{ height: '100%', position: 'relative' }}>
                    <video ref={videoRef} autoPlay playsInline style={{ width: '100%', height: '100%', objectFit: 'cover', opacity: 0.35, filter: 'grayscale(1) contrast(1.2)' }} />
                    <Box className="scan-animation" />
                  </Box>
                ) : (
                  <Box sx={{ height: '100%', position: 'relative' }}>
                    <img src={image} style={{ width: '100%', height: '100%', objectFit: 'cover', filter: isAnalyzing ? 'brightness(0.4) saturate(0.2)' : 'none' }} />
                    {isAnalyzing && <Box className="scan-animation" />}
                  </Box>
                )}

                {/* Scoped Controls */}
                {!isAnalyzing && (
                  <Stack 
                    direction="row" 
                    spacing={2.5} 
                    sx={{ 
                      position: 'absolute', 
                      bottom: 32, 
                      left: '50%', 
                      transform: 'translateX(-50%)',
                      p: 1.5,
                      bgcolor: 'rgba(0,0,0,0.5)',
                      backdropFilter: 'blur(20px)',
                      borderRadius: 6,
                      border: '1px solid rgba(255,255,255,0.1)'
                    }}
                  >
                    <Button
                      component="label"
                      variant="text"
                      sx={{ minWidth: 60, height: 60, borderRadius: 5, color: 'text.secondary', '&:hover': { color: 'white' } }}
                    >
                      <Upload size={28} />
                      <input type="file" hidden accept="image/*" onChange={handleFileUpload} />
                    </Button>
                    <IconButton 
                      onClick={captureImage}
                      sx={{ 
                        width: 76, 
                        height: 76, 
                        bgcolor: 'primary.main', 
                        color: 'white',
                        '&:hover': { bgcolor: '#0ea573', transform: 'scale(1.05)' },
                        boxShadow: '0 0 40px rgba(16, 185, 129, 0.4)',
                        transition: '0.2s'
                      }}
                    >
                      <Camera size={36} />
                    </IconButton>
                  </Stack>
                )}
              </Box>

              {error && <Alert severity="error" variant="filled" sx={{ borderRadius: 5 }}>{error}</Alert>}
            </Grid>

            {/* Analysis Output Viewport */}
            <Grid item xs={12} md={7} lg={8} sx={{ display: 'flex', flexDirection: 'column' }}>
              <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', gap: 2.5 }}>
                <Box sx={{ width: 10, height: 10, borderRadius: '50%', bgcolor: 'primary.main', animation: 'pulse 2s infinite' }} />
                <Typography variant="overline" color="text.secondary">
                   {isAnalyzing ? 'System Parsing...' : activeTab.split(' ').map(w => w.toUpperCase()).join(' ') + ' NODE'}
                </Typography>
              </Box>
              
              <Box sx={{ flex: 1, overflowY: 'auto', pr: 2, pb: 4 }}>
                {renderContent()}
              </Box>
            </Grid>

          </Grid>
        </Box>
      </Box>
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </ThemeProvider>
  );
};

export default App;
