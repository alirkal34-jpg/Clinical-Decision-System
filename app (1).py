import React, { useState } from 'react';
import { Heart, Activity, AlertCircle, CheckCircle, TrendingUp } from 'lucide-react';

export default function CardioAI() {
  const [age, setAge] = useState(50);
  const [gender, setGender] = useState('male');
  const [height, setHeight] = useState(175);
  const [weight, setWeight] = useState(80);
  const [systolic, setSystolic] = useState(120);
  const [diastolic, setDiastolic] = useState(80);
  const [cholesterol, setCholesterol] = useState('normal');
  const [glucose, setGlucose] = useState('normal');
  const [smoke, setSmoke] = useState(false);
  const [alcohol, setAlcohol] = useState(false);
  const [active, setActive] = useState(true);
  const [result, setResult] = useState(null);

  const calculateRisk = () => {
    const bmi = weight / ((height / 100) ** 2);
    
    // Base risk calculation with improved weighting
    let riskScore = 0;
    const reasons = [];

    // Age factor (strongest predictor)
    if (age > 60) {
      riskScore += 0.25;
      reasons.push('Age >60 (+25%)');
    } else if (age > 50) {
      riskScore += 0.15;
      reasons.push('Age >50 (+15%)');
    } else if (age > 40) {
      riskScore += 0.08;
      reasons.push('Age >40 (+8%)');
    }

    // Blood pressure (critical factor)
    if (systolic >= 140 || diastolic >= 90) {
      riskScore += 0.22;
      reasons.push('Hypertension Stage 2 (+22%)');
    } else if (systolic >= 130 || diastolic >= 85) {
      riskScore += 0.12;
      reasons.push('Elevated BP (+12%)');
    } else if (systolic >= 120 || diastolic >= 80) {
      riskScore += 0.05;
      reasons.push('Prehypertension (+5%)');
    }

    // BMI factor
    if (bmi >= 30) {
      riskScore += 0.15;
      reasons.push('Obesity BMI ≥30 (+15%)');
    } else if (bmi >= 25) {
      riskScore += 0.08;
      reasons.push('Overweight BMI ≥25 (+8%)');
    }

    // Cholesterol (significant metabolic factor)
    if (cholesterol === 'very_high') {
      riskScore += 0.18;
      reasons.push('Very High Cholesterol (+18%)');
    } else if (cholesterol === 'above_normal') {
      riskScore += 0.10;
      reasons.push('Above Normal Cholesterol (+10%)');
    }

    // Glucose (diabetes risk)
    if (glucose === 'very_high') {
      riskScore += 0.16;
      reasons.push('Very High Glucose (+16%)');
    } else if (glucose === 'above_normal') {
      riskScore += 0.09;
      reasons.push('Above Normal Glucose (+9%)');
    }

    // LIFESTYLE FACTORS - Now properly weighted!
    if (smoke) {
      riskScore += 0.20; // Smoking is a MAJOR risk factor
      reasons.push('⚠️ Smoking (+20%)');
    }
    
    if (alcohol) {
      riskScore += 0.10; // Excessive alcohol significantly increases risk
      reasons.push('⚠️ Alcohol Use (+10%)');
    }
    
    if (!active) {
      riskScore += 0.12; // Sedentary lifestyle is dangerous
      reasons.push('⚠️ Physical Inactivity (+12%)');
    }

    // Gender factor (men at slightly higher risk)
    if (gender === 'male') {
      riskScore += 0.05;
      reasons.push('Male Gender (+5%)');
    }

    // Cap the score
    riskScore = Math.min(Math.max(riskScore, 0.01), 0.99);

    setResult({
      score: riskScore,
      percentage: (riskScore * 100).toFixed(1),
      bmi: bmi.toFixed(1),
      reasons: reasons,
      riskLevel: riskScore > 0.60 ? 'critical' : riskScore > 0.40 ? 'high' : riskScore > 0.25 ? 'moderate' : 'low'
    });
  };

  const getRiskColor = (level) => {
    switch(level) {
      case 'critical': return 'from-red-600 to-red-800';
      case 'high': return 'from-orange-500 to-red-600';
      case 'moderate': return 'from-yellow-500 to-orange-500';
      case 'low': return 'from-green-500 to-emerald-600';
      default: return 'from-gray-500 to-gray-600';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 text-white p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 pt-6">
          <div className="flex items-center justify-center gap-3 mb-3">
            <Heart className="w-12 h-12 text-red-500" />
            <h1 className="text-4xl font-bold">Cardio AI</h1>
          </div>
          <p className="text-slate-400">Clinical Decision Support System</p>
          <div className="inline-block mt-2 px-4 py-1 bg-green-900/30 border border-green-500 rounded-full text-green-400 text-sm">
            ● AI Engine Online
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Sidebar - Patient Data Entry */}
          <div className="lg:col-span-1 bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-6 h-fit">
            <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
              <Activity className="w-5 h-5" />
              Patient Data
            </h2>

            {/* Demographics */}
            <div className="space-y-4 mb-6">
              <h3 className="text-sm font-semibold text-slate-400 uppercase">Demographics</h3>
              
              <div>
                <label className="block text-sm mb-2">Age: {age}</label>
                <input 
                  type="range" 
                  min="30" 
                  max="90" 
                  value={age} 
                  onChange={(e) => setAge(Number(e.target.value))}
                  className="w-full accent-red-500"
                />
              </div>

              <div>
                <label className="block text-sm mb-2">Gender</label>
                <div className="flex gap-2">
                  <button 
                    onClick={() => setGender('male')}
                    className={`flex-1 py-2 rounded-lg ${gender === 'male' ? 'bg-red-500' : 'bg-slate-700'}`}
                  >
                    Male
                  </button>
                  <button 
                    onClick={() => setGender('female')}
                    className={`flex-1 py-2 rounded-lg ${gender === 'female' ? 'bg-red-500' : 'bg-slate-700'}`}
                  >
                    Female
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-sm mb-2">Height (cm)</label>
                  <input 
                    type="number" 
                    value={height} 
                    onChange={(e) => setHeight(Number(e.target.value))}
                    className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block text-sm mb-2">Weight (kg)</label>
                  <input 
                    type="number" 
                    value={weight} 
                    onChange={(e) => setWeight(Number(e.target.value))}
                    className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2"
                  />
                </div>
              </div>
            </div>

            {/* Clinical Vitals */}
            <div className="space-y-4 mb-6 pt-4 border-t border-slate-700">
              <h3 className="text-sm font-semibold text-slate-400 uppercase">Clinical Vitals</h3>
              
              <div>
                <label className="block text-sm mb-2">Systolic BP: {systolic}</label>
                <input 
                  type="range" 
                  min="80" 
                  max="240" 
                  value={systolic} 
                  onChange={(e) => setSystolic(Number(e.target.value))}
                  className="w-full accent-red-500"
                />
              </div>

              <div>
                <label className="block text-sm mb-2">Diastolic BP: {diastolic}</label>
                <input 
                  type="range" 
                  min="40" 
                  max="140" 
                  value={diastolic} 
                  onChange={(e) => setDiastolic(Number(e.target.value))}
                  className="w-full accent-red-500"
                />
              </div>

              <div>
                <label className="block text-sm mb-2">Cholesterol</label>
                <select 
                  value={cholesterol} 
                  onChange={(e) => setCholesterol(e.target.value)}
                  className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2"
                >
                  <option value="normal">Normal</option>
                  <option value="above_normal">Above Normal</option>
                  <option value="very_high">Very High</option>
                </select>
              </div>

              <div>
                <label className="block text-sm mb-2">Glucose</label>
                <select 
                  value={glucose} 
                  onChange={(e) => setGlucose(e.target.value)}
                  className="w-full bg-slate-700 border border-slate-600 rounded px-3 py-2"
                >
                  <option value="normal">Normal</option>
                  <option value="above_normal">Above Normal</option>
                  <option value="very_high">Very High</option>
                </select>
              </div>
            </div>

            {/* Lifestyle */}
            <div className="space-y-3 pt-4 border-t border-slate-700">
              <h3 className="text-sm font-semibold text-slate-400 uppercase">Lifestyle</h3>
              
              <label className="flex items-center justify-between cursor-pointer">
                <span>Smoker</span>
                <input 
                  type="checkbox" 
                  checked={smoke} 
                  onChange={(e) => setSmoke(e.target.checked)}
                  className="w-5 h-5 accent-red-500"
                />
              </label>

              <label className="flex items-center justify-between cursor-pointer">
                <span>Alcohol</span>
                <input 
                  type="checkbox" 
                  checked={alcohol} 
                  onChange={(e) => setAlcohol(e.target.checked)}
                  className="w-5 h-5 accent-red-500"
                />
              </label>

              <label className="flex items-center justify-between cursor-pointer">
                <span>Active Sport</span>
                <input 
                  type="checkbox" 
                  checked={active} 
                  onChange={(e) => setActive(e.target.checked)}
                  className="w-5 h-5 accent-green-500"
                />
              </label>
            </div>

            <button 
              onClick={calculateRisk}
              className="w-full mt-6 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 py-3 rounded-lg font-semibold transition-all transform hover:scale-105"
            >
              🚀 START ANALYSIS
            </button>
          </div>

          {/* Main Content - Results */}
          <div className="lg:col-span-2 space-y-6">
            {/* Metrics Row */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white text-slate-900 rounded-lg p-4 shadow-lg">
                <div className="text-sm text-slate-600 mb-1">BMI Score</div>
                <div className="text-2xl font-bold">{result ? result.bmi : '--'}</div>
              </div>
              <div className="bg-white text-slate-900 rounded-lg p-4 shadow-lg">
                <div className="text-sm text-slate-600 mb-1">Blood Pressure</div>
                <div className="text-2xl font-bold">{systolic}/{diastolic}</div>
              </div>
              <div className="bg-white text-slate-900 rounded-lg p-4 shadow-lg">
                <div className="text-sm text-slate-600 mb-1">Patient Age</div>
                <div className="text-2xl font-bold">{age}</div>
              </div>
              <div className="bg-white text-slate-900 rounded-lg p-4 shadow-lg">
                <div className="text-sm text-slate-600 mb-1">Metabolic Risk</div>
                <div className="text-2xl font-bold">
                  {cholesterol !== 'normal' || glucose !== 'normal' ? 'Elevated' : 'Normal'}
                </div>
              </div>
            </div>

            {/* Results Display */}
            {result ? (
              <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-8">
                <h2 className="text-2xl font-bold mb-6">Diagnostic Report</h2>
                
                {/* Risk Gauge */}
                <div className="mb-8">
                  <div className="text-center mb-4">
                    <div className={`inline-block text-6xl font-bold bg-gradient-to-r ${getRiskColor(result.riskLevel)} bg-clip-text text-transparent`}>
                      {result.percentage}%
                    </div>
                    <div className="text-slate-400 mt-2">Cardiovascular Risk Probability</div>
                  </div>
                  
                  <div className="h-8 bg-slate-700 rounded-full overflow-hidden">
                    <div 
                      className={`h-full bg-gradient-to-r ${getRiskColor(result.riskLevel)} transition-all duration-1000`}
                      style={{ width: `${result.percentage}%` }}
                    />
                  </div>
                  <div className="flex justify-between text-xs text-slate-500 mt-1">
                    <span>0%</span>
                    <span>Low</span>
                    <span>Moderate</span>
                    <span>High</span>
                    <span>100%</span>
                  </div>
                </div>

                {/* Clinical Conclusion */}
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    {result.riskLevel === 'critical' || result.riskLevel === 'high' ? (
                      <div className="bg-red-950/50 border border-red-800 rounded-lg p-6">
                        <div className="flex items-center gap-2 text-red-400 mb-3">
                          <AlertCircle className="w-6 h-6" />
                          <h3 className="text-lg font-bold">HIGH RISK DETECTED</h3>
                        </div>
                        <p className="text-red-200 mb-4">
                          The patient shows strong indicators of cardiovascular disease.
                        </p>
                        <div className="space-y-2 text-sm text-red-300">
                          <p><strong>Recommended Action:</strong></p>
                          <p>• Urgent Cardiology Referral</p>
                          <p>• Full Blood Panel Required</p>
                          <p>• Immediate Lifestyle Intervention</p>
                        </div>
                      </div>
                    ) : (
                      <div className="bg-green-950/50 border border-green-800 rounded-lg p-6">
                        <div className="flex items-center gap-2 text-green-400 mb-3">
                          <CheckCircle className="w-6 h-6" />
                          <h3 className="text-lg font-bold">{result.riskLevel === 'moderate' ? 'MODERATE RISK' : 'LOW RISK / HEALTHY'}</h3>
                        </div>
                        <p className="text-green-200 mb-4">
                          {result.riskLevel === 'moderate' 
                            ? 'The patient has some risk factors that should be addressed.'
                            : "The patient's values are within the manageable range."}
                        </p>
                        <div className="space-y-2 text-sm text-green-300">
                          <p><strong>Recommended Action:</strong></p>
                          <p>• {result.riskLevel === 'moderate' ? 'Follow-up in 3-6 months' : 'Routine Annual Check-up'}</p>
                          <p>• Maintain Healthy Diet</p>
                          <p>• Regular Exercise</p>
                        </div>
                      </div>
                    )}
                  </div>

                  <div>
                    <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-6">
                      <div className="flex items-center gap-2 mb-3">
                        <TrendingUp className="w-5 h-5 text-amber-400" />
                        <h3 className="font-bold">Risk Contributors</h3>
                      </div>
                      <div className="space-y-2 text-sm">
                        {result.reasons.length > 0 ? (
                          result.reasons.map((reason, idx) => (
                            <div key={idx} className="flex items-start gap-2">
                              <span className="text-amber-400 mt-0.5">•</span>
                              <span className="text-slate-300">{reason}</span>
                            </div>
                          ))
                        ) : (
                          <p className="text-slate-400">No significant risk factors detected</p>
                        )}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-slate-800/50 backdrop-blur border border-slate-700 rounded-xl p-12 text-center">
                <Heart className="w-16 h-16 text-slate-600 mx-auto mb-4" />
                <p className="text-slate-400 text-lg">
                  Please enter patient data and click <strong>"START ANALYSIS"</strong> to begin assessment
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
