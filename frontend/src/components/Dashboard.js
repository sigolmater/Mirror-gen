import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import Plot from 'react-plotly.js';

const DashboardContainer = styled.div`
  padding: 2rem;
  max-width: 1400px;
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

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
`;

const StatCard = styled(motion.div)`
  background: linear-gradient(135deg, ${props => props.color || '#667eea'} 0%, ${props => props.color2 || '#764ba2'} 100%);
  border-radius: 15px;
  padding: 1.5rem;
  text-align: center;
  color: white;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
`;

const StatIcon = styled.div`
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: bold;
  margin: 0.5rem 0;
`;

const StatLabel = styled.div`
  font-size: 0.9rem;
  opacity: 0.8;
`;

const SystemStatus = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
`;

const StatusCard = styled.div`
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 1.5rem;
  border-left: 4px solid ${props => {
    if (props.status === 'active') return '#00ff00';
    if (props.status === 'warning') return '#ffff00';
    return '#ff0000';
  }};
  
  h4 {
    margin-top: 0;
    color: ${props => {
      if (props.status === 'active') return '#00ff00';
      if (props.status === 'warning') return '#ffff00';
      return '#ff0000';
    }};
  }
`;

const ActivityFeed = styled.div`
  max-height: 400px;
  overflow-y: auto;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  padding: 1rem;
  
  .activity-item {
    padding: 0.5rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    
    &:last-child {
      border-bottom: none;
    }
    
    .timestamp {
      font-size: 0.8rem;
      color: #888;
    }
    
    .message {
      margin-top: 0.25rem;
    }
  }
`;

const QuickActions = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin: 2rem 0;
`;

const ActionButton = styled.button`
  padding: 1rem;
  border: none;
  border-radius: 10px;
  background: linear-gradient(135deg, #ff6b6b, #feca57);
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

function Dashboard() {
  const [systemStats, setSystemStats] = useState({
    activePersonas: 5,
    optimizationCycles: 1247,
    quantumLevel: 7,
    mirrorReflections: 13,
    systemUptime: '7d 14h 32m',
    totalOptimizations: 89
  });

  const [realTimeData, setRealTimeData] = useState([]);
  const [activityLog, setActivityLog] = useState([
    { timestamp: '2024-01-15 14:32:18', message: '🚀 AI 최적화 시스템 시작됨', type: 'info' },
    { timestamp: '2024-01-15 14:31:45', message: '⚛️ 양자 준비 완료 (레벨 7)', type: 'success' },
    { timestamp: '2024-01-15 14:31:12', message: '🎭 페르소나 "아인슈타인" 활성화', type: 'info' },
    { timestamp: '2024-01-15 14:30:58', message: '🌊 Navier-Stokes 웜업 완료', type: 'success' },
    { timestamp: '2024-01-15 14:30:21', message: '🔍 지피지기 환경 분석 시작', type: 'info' }
  ]);

  // Simulate real-time data updates
  useEffect(() => {
    const interval = setInterval(() => {
      const now = new Date();
      const newPoint = {
        time: now.toLocaleTimeString(),
        performance: 70 + Math.random() * 25,
        efficiency: 60 + Math.random() * 35,
        coherence: 80 + Math.random() * 15
      };

      setRealTimeData(prev => {
        const updated = [...prev, newPoint];
        return updated.slice(-20); // Keep last 20 points
      });

      // Occasionally add new activity
      if (Math.random() < 0.3) {
        const activities = [
          '🔄 에코가 페르소나 동기화 수행',
          '💡 레인보우가 창의적 해결책 제안',
          '⚓ 이순신이 전략 업데이트 완료',
          '🔬 화타가 시스템 진단 완료',
          '✅ 오메가가 품질 검증 수행'
        ];
        
        const newActivity = {
          timestamp: now.toLocaleString(),
          message: activities[Math.floor(Math.random() * activities.length)],
          type: 'info'
        };

        setActivityLog(prev => [newActivity, ...prev.slice(0, 19)]);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  const performanceChartData = [
    {
      x: realTimeData.map(d => d.time),
      y: realTimeData.map(d => d.performance),
      type: 'scatter',
      mode: 'lines+markers',
      name: '전체 성능',
      line: { color: '#00ff00', width: 2 }
    },
    {
      x: realTimeData.map(d => d.time),
      y: realTimeData.map(d => d.efficiency),
      type: 'scatter',
      mode: 'lines+markers',
      name: '효율성',
      line: { color: '#ff6b6b', width: 2 }
    },
    {
      x: realTimeData.map(d => d.time),
      y: realTimeData.map(d => d.coherence),
      type: 'scatter',
      mode: 'lines+markers',
      name: '일관성',
      line: { color: '#feca57', width: 2 }
    }
  ];

  const quantumDistribution = [
    {
      values: [30, 25, 20, 15, 10],
      labels: ['양자 준비', 'AI 최적화', '거울 반사', '페르소나 동기화', '기타'],
      type: 'pie',
      marker: {
        colors: ['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3', '#6c5ce7']
      }
    }
  ];

  return (
    <DashboardContainer>
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Section>
          <Title>📊 시스템 대시보드</Title>
          <p>
            시골길 개인 AI 최적화 시스템의 실시간 상태와 성능을 모니터링합니다.
            13면체 정다면체 거울 시스템이 모든 페르소나를 동기화하여 최적의 성능을 제공합니다.
          </p>
        </Section>

        <Section>
          <Title>📈 주요 지표</Title>
          <StatsGrid>
            <StatCard
              color="#667eea"
              color2="#764ba2"
              whileHover={{ scale: 1.05 }}
            >
              <StatIcon>🎭</StatIcon>
              <StatValue>{systemStats.activePersonas}</StatValue>
              <StatLabel>활성 페르소나</StatLabel>
            </StatCard>

            <StatCard
              color="#f093fb"
              color2="#f5576c"
              whileHover={{ scale: 1.05 }}
            >
              <StatIcon>🔄</StatIcon>
              <StatValue>{systemStats.optimizationCycles}</StatValue>
              <StatLabel>최적화 사이클</StatLabel>
            </StatCard>

            <StatCard
              color="#4facfe"
              color2="#00f2fe"
              whileHover={{ scale: 1.05 }}
            >
              <StatIcon>⚛️</StatIcon>
              <StatValue>{systemStats.quantumLevel}</StatValue>
              <StatLabel>양자 레벨</StatLabel>
            </StatCard>

            <StatCard
              color="#a8edea"
              color2="#fed6e3"
              whileHover={{ scale: 1.05 }}
            >
              <StatIcon>🪞</StatIcon>
              <StatValue>{systemStats.mirrorReflections}</StatValue>
              <StatLabel>거울 반사</StatLabel>
            </StatCard>

            <StatCard
              color="#ff9a9e"
              color2="#fecfef"
              whileHover={{ scale: 1.05 }}
            >
              <StatIcon>⏱️</StatIcon>
              <StatValue>{systemStats.systemUptime}</StatValue>
              <StatLabel>시스템 가동시간</StatLabel>
            </StatCard>

            <StatCard
              color="#a18cd1"
              color2="#fbc2eb"
              whileHover={{ scale: 1.05 }}
            >
              <StatIcon>🏆</StatIcon>
              <StatValue>{systemStats.totalOptimizations}%</StatValue>
              <StatLabel>최적화 성공률</StatLabel>
            </StatCard>
          </StatsGrid>
        </Section>

        <Section>
          <Title>⚡ 시스템 상태</Title>
          <SystemStatus>
            <StatusCard status="active">
              <h4>🟢 Core AI Engine</h4>
              <p>모든 페르소나가 정상적으로 동작 중입니다.</p>
              <small>마지막 체크: 방금 전</small>
            </StatusCard>

            <StatusCard status="active">
              <h4>🟢 Quantum Prep System</h4>
              <p>양자 준비 시스템이 안정적으로 작동하고 있습니다.</p>
              <small>현재 레벨: {systemStats.quantumLevel}</small>
            </StatusCard>

            <StatusCard status="warning">
              <h4>🟡 Mirror Reflection Network</h4>
              <p>일부 거울 면에서 미세한 지연이 감지되었습니다.</p>
              <small>자동 조정 중...</small>
            </StatusCard>

            <StatusCard status="active">
              <h4>🟢 Navier-Stokes Warmup</h4>
              <p>유체역학적 최적화가 완벽하게 수행되고 있습니다.</p>
              <small>효율성: 94.7%</small>
            </StatusCard>
          </SystemStatus>
        </Section>

        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '2rem' }}>
          <Section>
            <Title>📊 실시간 성능 차트</Title>
            <Plot
              data={performanceChartData}
              layout={{
                width: '100%',
                height: 300,
                title: 'AI 시스템 실시간 성능',
                xaxis: { title: '시간', color: 'white' },
                yaxis: { title: '성능 (%)', color: 'white', range: [0, 100] },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0.3)',
                font: { color: 'white' },
                legend: { orientation: 'h', y: -0.2 }
              }}
              style={{ width: '100%' }}
            />
          </Section>

          <Section>
            <Title>🥧 리소스 분배</Title>
            <Plot
              data={quantumDistribution}
              layout={{
                width: 300,
                height: 300,
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                font: { color: 'white' },
                showlegend: false
              }}
            />
          </Section>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
          <Section>
            <Title>🚀 빠른 작업</Title>
            <QuickActions>
              <ActionButton onClick={() => window.location.href = '/warmup'}>
                🌊 웜업 시작
              </ActionButton>
              <ActionButton onClick={() => window.location.href = '/optimization'}>
                ⚡ AI 최적화
              </ActionButton>
              <ActionButton>
                🔧 시스템 조정
              </ActionButton>
              <ActionButton>
                📊 상세 분석
              </ActionButton>
              <ActionButton>
                🧠 페르소나 관리
              </ActionButton>
              <ActionButton>
                ⚛️ 양자 설정
              </ActionButton>
            </QuickActions>
          </Section>

          <Section>
            <Title>📝 활동 로그</Title>
            <ActivityFeed>
              {activityLog.map((activity, index) => (
                <div key={index} className="activity-item">
                  <div className="timestamp">{activity.timestamp}</div>
                  <div className="message">{activity.message}</div>
                </div>
              ))}
            </ActivityFeed>
          </Section>
        </div>
      </motion.div>
    </DashboardContainer>
  );
}

export default Dashboard;