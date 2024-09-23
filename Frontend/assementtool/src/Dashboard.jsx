import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { PieComponent } from './components/ui/piechart';
import { BarChartComponent } from './components/ui/barchart';

const Dashboard = () => {
  const location = useLocation();
  const { data } = location.state || {};
  const [listOfQuestions, setListOfQuestions] = useState([[]]);
  const [levelCounts, setLevelCounts] = useState([]);
  const [qualityOfPaper, setQualityOfPaper] = useState('');

  useEffect(() => {
    if (data) {
      setListOfQuestions(data.classified_questions);
      setLevelCounts(data.level_counts);
      setQualityOfPaper(data.quality_of_paper);
    }
  }, [data]);

  const totalQuestions = Object.values(levelCounts).reduce((acc, count) => acc + count, 0);

  return (
    <div className="p-8 bg-gray-900">
      {data ? (
        <div className="space-y-4">
          <h2 className="text-3xl text-cyan-600 font-bold text-center">Dashboard</h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-8">
            {/* Quality of Paper */}
            <div className="bg-slate-700 shadow-md p-2 rounded-lg flex flex-col items-center justify-center h-full ">
            <h1 className="text-3xl text-cyan-600  text-center">Quaility of paper</h1>
              <h1 className="text-6xl text-cyan-600 font-semibold  text-center">{parseFloat(qualityOfPaper).toFixed(2)}%</h1>
            </div>

            {/* Bar Chart */}
            
              <BarChartComponent levelCounts={levelCounts} />
            

            {/* Pie Chart */}
            
              <PieComponent levelCounts={levelCounts} totalQuestions={totalQuestions} />
              
            

            {/* Level Count Summary */}
            <div className="bg-slate-700 shadow-md p-2 rounded-lg flex  flex-col items-center justify-center justify-between h-full text-cyan-600 text-center">
              <h3 className="text-xl text-cyan-600 font-semibold ">Level Counts Summary</h3>
              <ul className="space-y-2">
                <li>ANALYZING: {levelCounts.ANALYZING}</li>
                <li>APPLYING: {levelCounts.APPLYING}</li>
                <li>CREATING: {levelCounts.CREATING}</li>
                <li>EVALUATING: {levelCounts.EVALUATING}</li>
                <li>REMEMBERING: {levelCounts.REMEMBERING}</li>
                <li>UNDERSTANDING: {levelCounts.UNDERSTANDING}</li>
                <li>Total: {totalQuestions}</li>
              </ul>
            </div>
          </div>
        </div>
      ) : (
        <p>No data available</p>
      )}
    </div>
  );
};

export default Dashboard;
