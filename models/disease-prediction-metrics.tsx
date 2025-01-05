import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const DiseasePredictionDashboard = () => {
  const predictionData = [
    {
      disease: "Parkinson's Disease",
      accuracy: 94.2,
      samples: 1196,
      features: 22,
      model: "Random Forest",
      color: "#4C51BF"
    },
    {
      disease: "Pneumonia",
      accuracy: 92.8,
      samples: 700,
      model: "XGBoost",
      color: "#48BB78"
    },
    {
      disease: "COPD",
      accuracy: 89.5,
      samples: 1500,
      model: "GRU",
      color: "#ED8936"
    },
    {
      disease: "URTI",
      accuracy: 88.7,
      samples: 1000,
      model: "GRU",
      color: "#9F7AEA"
    },
    {
      disease: "Bronchitis",
      accuracy: 91.3,
      samples: 892,
      model: "CNN",
      color: "#F56565"
    }
  ];

  return (
    <Card className="w-full p-4">
      <CardHeader>
        <CardTitle>Disease Prediction Performance Metrics</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="mb-8">
          <ResponsiveContainer width="100%" height={400}>
            <BarChart
              data={predictionData}
              margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="disease" angle={-45} textAnchor="end" height={80} />
              <YAxis 
                yAxisId="left" 
                label={{ value: 'Accuracy (%)', angle: -90, position: 'insideLeft' }}
                domain={[80, 100]}  // Adjusted to better show accuracy differences
              />
              <YAxis 
                yAxisId="right" 
                orientation="right" 
                label={{ value: 'Dataset Samples', angle: 90, position: 'insideRight' }}
                domain={[0, 1600]}  // Adjusted for actual sample sizes
              />
              <Tooltip />
              <Legend />
              <Bar 
                yAxisId="left"
                dataKey="accuracy" 
                fill="#4C51BF" 
                name="Accuracy (%)"
              />
              <Bar 
                yAxisId="right"
                dataKey="samples" 
                fill="#48BB78" 
                name="Dataset Samples"
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {predictionData.map((item) => (
            <Card key={item.disease} className="p-4">
              <h3 className="font-bold mb-2">{item.disease}</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span>Accuracy:</span>
                  <span className="font-medium">{item.accuracy}%</span>
                </div>
                <div className="flex justify-between">
                  <span>Samples:</span>
                  <span className="font-medium">{item.samples}</span>
                </div>
                <div className="flex justify-between">
                  <span>Model:</span>
                  <span className="font-medium">{item.model}</span>
                </div>
                {item.features && (
                  <div className="flex justify-between">
                    <span>Features:</span>
                    <span className="font-medium">{item.features}</span>
                  </div>
                )}
              </div>
            </Card>
          ))}
        </div>
      </CardContent>
    </Card>
  );
};

export default DiseasePredictionDashboard;
