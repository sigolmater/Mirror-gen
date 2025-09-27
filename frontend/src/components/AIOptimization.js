import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Plot from 'react-plotly.js';

const OptimizationContainer = styled.div`
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const Section = styled(motion.section)`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 15px;
  padding: 2rem;
  margin: 2rem 0;
`;

const Title = styled.h2`
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #ffd700;
`;

const PersonaGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
`;

const PersonaCard = styled(motion.div)`
  background: ${props => props.active ? 
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' : 
    'rgba(255, 255, 255, 0.1)'
  };
  border-radius: 10px;
  padding: 1.5rem;
  border: 2px solid ${props => props.active ? '#ffd700' : 'transparent'};
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
  }
`;

const PersonaIcon = styled.div`
  font-size: 2.5rem;
  margin-bottom: 1rem;
`;

const PersonaName = styled.h3`
  margin: 0 0 0.5rem 0;
  color: ${props => props.active ? '#ffd700' : '#fff'};
`;

const PersonaDescription = styled.p`
  font-size: 0.9rem;
  opacity: 0.8;
  margin: 0;
`;

const ControlPanel = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
`;

const ControlGroup = styled.div`
  background: rgba(0, 0, 0, 0.3);
  padding: 1.5rem;
  border-radius: 10px;
  
  h4 {
    margin-top: 0;
    color: #ffd700;
  }
  
  label {
    display: block;
    margin: 1rem 0;
    
    input, select {
      width: 100%;
      padding: 0.5rem;
      margin-top: 0.5rem;
      border-radius: 5px;
      border: none;
      background: rgba(255, 255, 255, 0.9);
    }
  }
`;

const OptimizationButton = styled.button`
  width: 100%;
  padding: 1.5rem;
  border: none;
  border-radius: 10px;
  background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
  background-size: 400% 400%;
  color: white;
  font-size: 1.3rem;
  font-weight: bold;
  cursor: pointer;
  margin: 2rem 0;
  animation: gradientShift 3s ease infinite;
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  @keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
  }
`;

const ResultsPanel = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
`;

const MetricCard = styled.div`
  background: rgba(0, 0, 0, 0.3);
  padding: 1.5rem;
  border-radius: 10px;
  text-align: center;
  
  h4 {
    margin-top: 0;
    color: #ffd700;
  }
  
  .metric-value {
    font-size: 2.5rem;
    font-weight: bold;
    margin: 0.5rem 0;
    color: ${props => {
      if (props.value >= 90) return '#00ff00';
      if (props.value >= 70) return '#ffff00';
      return '#ff6b6b';
    }};
  }
`;

const personas = [
  {
    id: 'sun-shin',
    name: '불멸의 이순신',
    icon: '⚓',
    description: '전략 총괄과 위기 관리 (거북선 인텔리전스 활용)',
    specialty: 'strategy'
  },
  {
    id: 'know-enemy',
    name: '지피지기',
    icon: '🔍',
    description: '환경 분석과 전술 지원 (진리의 만리경으로 통찰)',
    specialty: 'analysis'
  },
  {
    id: 'rainbow',
    name: '레인보우',
    icon: '🌈',
    description: '감성 이해와 창의적 발상 (오로라 팔레트로 색칠)',
    specialty: 'creativity'
  },
  {
    id: 'hwata',
    name: '화타',
    icon: '💉',
    description: '문제 진단과 치유 방안 제시 (현자의 침으로 치료)',
    specialty: 'healing'
  },
  {
    id: 'einstein',
    name: '아인슈타인',
    icon: '⚛️',
    description: '신기술 개발과 혁신 실험 (호구와트 연구소 운영)',
    specialty: 'innovation'
  },
  {
    id: 'omniscient',
    name: '만물박사',
    icon: '📚',
    description: '지식 통합과 데이터 해석 (도깨비 방망이로 해결)',
    specialty: 'knowledge'
  },
  {
    id: 'omega',
    name: '오메가',
    icon: '✅',
    description: '품질 검증과 업무 완결 (시골인지로 최종 확인)',
    specialty: 'quality'
  },
  {
    id: 'echo',
    name: '에코',
    icon: '🔄',
    description: '목표 정렬과 페르소나 동기화 (공명 메신저로 연결)',
    specialty: 'synchronization'
  }
];

function AIOptimization() {
  const [activePersonas, setActivePersonas] = useState([]);
  const [optimizationMode, setOptimizationMode] = useState('balanced');
  const [quantumLevel, setQuantumLevel] = useState(5);
  const [mirrorDepth, setMirrorDepth] = useState(3);
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [results, setResults] = useState(null);
  const [realTimeMetrics, setRealTimeMetrics] = useState({
    efficiency: 85,
    coherence: 92,
    innovation: 78,
    stability: 94
  });

  const togglePersona = (personaId) => {
    setActivePersonas(prev => 
      prev.includes(personaId) 
        ? prev.filter(id => id !== personaId)
        : [...prev, personaId]
    );
  };

  const startOptimization = async () => {
    setIsOptimizing(true);
    
    try {
      const response = await fetch('/api/ai-optimization/start', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          personas: activePersonas,
          mode: optimizationMode,
          quantum_level: quantumLevel,
          mirror_depth: mirrorDepth
        })
      });
      
      const data = await response.json();
      
      // Simulate optimization process
      setTimeout(() => {
        setResults(data);
        setRealTimeMetrics({
          efficiency: Math.min(100, realTimeMetrics.efficiency + Math.random() * 10),
          coherence: Math.min(100, realTimeMetrics.coherence + Math.random() * 8),
          innovation: Math.min(100, realTimeMetrics.innovation + Math.random() * 15),
          stability: Math.min(100, realTimeMetrics.stability + Math.random() * 5)
        });
        setIsOptimizing(false);
      }, 3000);
      
    } catch (error) {
      console.error('Optimization error:', error);
      setIsOptimizing(false);
    }
  };

  // Real-time metrics simulation
  useEffect(() => {
    const interval = setInterval(() => {
      if (isOptimizing) {
        setRealTimeMetrics(prev => ({
          efficiency: Math.max(0, Math.min(100, prev.efficiency + (Math.random() - 0.5) * 5)),
          coherence: Math.max(0, Math.min(100, prev.coherence + (Math.random() - 0.5) * 3)),
          innovation: Math.max(0, Math.min(100, prev.innovation + (Math.random() - 0.5) * 8)),
          stability: Math.max(0, Math.min(100, prev.stability + (Math.random() - 0.5) * 2))
        }));
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [isOptimizing]);

  const performanceData = [
    {
      x: ['효율성', '일관성', '혁신성', '안정성'],
      y: [realTimeMetrics.efficiency, realTimeMetrics.coherence, realTimeMetrics.innovation, realTimeMetrics.stability],
      type: 'bar',
      marker: {
        color: ['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3']
      }
    }
  ];

  return (
    <OptimizationContainer>
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Section>
          <Title>🚀 AI 최적화 시스템</Title>
          <p>
            13면체 정다면체 거울 시스템을 통한 AI 페르소나 최적화입니다.
            각 면이 서로를 비추며 하나의 성장이 13배로 증폭되어 전체로 확산됩니다.
          </p>
        </Section>

        <Section>
          <Title>🎭 페르소나 선택</Title>
          <p>활성화할 AI 페르소나를 선택하세요. 최대 8개까지 동시 활성화 가능합니다.</p>
          <PersonaGrid>
            {personas.map(persona => (
              <PersonaCard
                key={persona.id}
                active={activePersonas.includes(persona.id)}
                onClick={() => togglePersona(persona.id)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <PersonaIcon>{persona.icon}</PersonaIcon>
                <PersonaName active={activePersonas.includes(persona.id)}>
                  {persona.name}
                </PersonaName>
                <PersonaDescription>{persona.description}</PersonaDescription>
              </PersonaCard>
            ))}
          </PersonaGrid>
        </Section>

        <Section>
          <Title>⚙️ 최적화 설정</Title>
          <ControlPanel>
            <ControlGroup>
              <h4>최적화 모드</h4>
              <label>
                모드 선택:
                <select 
                  value={optimizationMode} 
                  onChange={(e) => setOptimizationMode(e.target.value)}
                >
                  <option value="balanced">균형 모드</option>
                  <option value="performance">성능 우선</option>
                  <option value="creativity">창의성 우선</option>
                  <option value="stability">안정성 우선</option>
                </select>
              </label>
            </ControlGroup>

            <ControlGroup>
              <h4>양자 준비 수준</h4>
              <label>
                양자 레벨: {quantumLevel}
                <input
                  type="range"
                  min="1"
                  max="10"
                  value={quantumLevel}
                  onChange={(e) => setQuantumLevel(parseInt(e.target.value))}
                />
              </label>
            </ControlGroup>

            <ControlGroup>
              <h4>거울 반사 깊이</h4>
              <label>
                반사 깊이: {mirrorDepth}
                <input
                  type="range"
                  min="1"
                  max="7"
                  value={mirrorDepth}
                  onChange={(e) => setMirrorDepth(parseInt(e.target.value))}
                />
              </label>
            </ControlGroup>
          </ControlPanel>

          <OptimizationButton 
            onClick={startOptimization} 
            disabled={isOptimizing || activePersonas.length === 0}
          >
            {isOptimizing ? '🔄 최적화 진행 중...' : '✨ AI 최적화 시작'}
          </OptimizationButton>
        </Section>

        <Section>
          <Title>📊 실시간 성능 모니터링</Title>
          <ResultsPanel>
            <div>
              <Plot
                data={performanceData}
                layout={{
                  title: 'AI 성능 지표',
                  width: 400,
                  height: 300,
                  paper_bgcolor: 'rgba(0,0,0,0)',
                  plot_bgcolor: 'rgba(0,0,0,0.3)',
                  font: { color: 'white' },
                  yaxis: { range: [0, 100] }
                }}
              />
            </div>
            
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <MetricCard value={realTimeMetrics.efficiency}>
                <h4>⚡ 효율성</h4>
                <div className="metric-value">{realTimeMetrics.efficiency.toFixed(1)}%</div>
              </MetricCard>
              
              <MetricCard value={realTimeMetrics.coherence}>
                <h4>🎯 일관성</h4>
                <div className="metric-value">{realTimeMetrics.coherence.toFixed(1)}%</div>
              </MetricCard>
              
              <MetricCard value={realTimeMetrics.innovation}>
                <h4>💡 혁신성</h4>
                <div className="metric-value">{realTimeMetrics.innovation.toFixed(1)}%</div>
              </MetricCard>
              
              <MetricCard value={realTimeMetrics.stability}>
                <h4>🛡️ 안정성</h4>
                <div className="metric-value">{realTimeMetrics.stability.toFixed(1)}%</div>
              </MetricCard>
            </div>
          </ResultsPanel>
        </Section>

        {results && (
          <Section>
            <Title>🏆 최적화 결과</Title>
            <div style={{ 
              background: 'rgba(0, 255, 0, 0.1)', 
              padding: '2rem', 
              borderRadius: '10px',
              border: '2px solid #00ff00'
            }}>
              <h3 style={{ color: '#00ff00', margin: 0 }}>
                ✅ 최적화 완료! 품질 등급: EXCELLENT
              </h3>
              <p style={{ margin: '1rem 0 0 0' }}>
                선택된 페르소나들이 성공적으로 동기화되었습니다. 
                {activePersonas.length}개의 페르소나가 {mirrorDepth}단계 거울 반사를 통해 
                최적화되었습니다.
              </p>
            </div>
          </Section>
        )}
      </motion.div>
    </OptimizationContainer>
  );
}

export default AIOptimization;