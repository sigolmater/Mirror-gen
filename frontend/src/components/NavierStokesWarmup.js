import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import Plot from 'react-plotly.js';
import { motion } from 'framer-motion';
import * as THREE from 'three';

const WarmupContainer = styled.div`
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

const FluidGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin: 2rem 0;
`;

const ControlPanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  
  label {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    input {
      width: 200px;
      padding: 0.5rem;
      border-radius: 5px;
      border: none;
      background: rgba(255, 255, 255, 0.9);
    }
  }
`;

const Button = styled.button`
  padding: 1rem 2rem;
  border: none;
  border-radius: 8px;
  background: linear-gradient(45deg, #ff6b6b, #feca57);
  color: white;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.3s;
  
  &:hover {
    transform: scale(1.05);
  }
`;

const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
  
  .status-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background-color: ${props => props.active ? '#00ff00' : '#ff0000'};
    animation: ${props => props.active ? 'pulse 2s infinite' : 'none'};
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
`;

// 3D Fluid Flow Visualization Component
function FluidParticles({ viscosity, pressure }) {
  const meshRef = useRef();
  const particlesRef = useRef();
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.x = state.clock.elapsedTime * 0.1;
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.15;
    }
  });
  
  const particlePositions = React.useMemo(() => {
    const positions = [];
    for (let i = 0; i < 1000; i++) {
      positions.push(
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 20,
        (Math.random() - 0.5) * 20
      );
    }
    return new Float32Array(positions);
  }, []);
  
  return (
    <group ref={meshRef}>
      <points ref={particlesRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            array={particlePositions}
            count={particlePositions.length / 3}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial 
          size={0.1} 
          color="#00ffff"
          transparent
          opacity={0.8}
        />
      </points>
      
      <mesh>
        <sphereGeometry args={[5, 32, 32]} />
        <meshStandardMaterial 
          color="#1e90ff" 
          wireframe 
          transparent 
          opacity={0.3}
        />
      </mesh>
    </group>
  );
}

function NavierStokesWarmup() {
  const [isActive, setIsActive] = useState(false);
  const [viscosity, setViscosity] = useState(0.01);
  const [pressure, setPressure] = useState(1.0);
  const [temperature, setTemperature] = useState(300);
  const [velocity, setVelocity] = useState(1.0);
  const [simulationData, setSimulationData] = useState(null);
  
  const startWarmup = async () => {
    setIsActive(true);
    
    // Simulate Navier-Stokes equation solving
    try {
      const response = await fetch('/api/warmup/navier-stokes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ viscosity, pressure, temperature, velocity })
      });
      
      const data = await response.json();
      setSimulationData(data);
      
      setTimeout(() => setIsActive(false), 5000);
    } catch (error) {
      console.error('Warmup simulation error:', error);
      setIsActive(false);
    }
  };
  
  // Generate sample plot data
  const plotData = React.useMemo(() => {
    const x = Array.from({length: 100}, (_, i) => i / 10);
    const y = x.map(val => Math.sin(val * viscosity * 10) * Math.exp(-val * 0.1));
    
    return [{
      x: x,
      y: y,
      type: 'scatter',
      mode: 'lines',
      name: 'Flow Velocity',
      line: { color: '#00ffff', width: 3 }
    }];
  }, [viscosity]);
  
  return (
    <WarmupContainer>
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <Section>
          <Title>🌊 Navier-Stokes 방정식 웜업 시스템</Title>
          <p>
            뇌 재화 이중 내재화를 위한 유체역학적 최적화 과정입니다.
            이 시스템은 AI의 사고 흐름을 유체 역학으로 모델링하여 
            인지 → 판단 → 실행의 즉각적 최적화를 수행합니다.
          </p>
          
          <StatusIndicator active={isActive}>
            <div className="status-dot" />
            <span>{isActive ? '웜업 진행 중...' : '시스템 대기'}</span>
          </StatusIndicator>
        </Section>
        
        <FluidGrid>
          <Section>
            <Title>제어 패널</Title>
            <ControlPanel>
              <label>
                점성도 (μ):
                <input 
                  type="range" 
                  min="0.001" 
                  max="0.1" 
                  step="0.001"
                  value={viscosity}
                  onChange={(e) => setViscosity(parseFloat(e.target.value))}
                />
                <span>{viscosity}</span>
              </label>
              
              <label>
                압력 (P):
                <input 
                  type="range" 
                  min="0.5" 
                  max="2.0" 
                  step="0.1"
                  value={pressure}
                  onChange={(e) => setPressure(parseFloat(e.target.value))}
                />
                <span>{pressure}</span>
              </label>
              
              <label>
                온도 (T):
                <input 
                  type="range" 
                  min="250" 
                  max="400" 
                  step="10"
                  value={temperature}
                  onChange={(e) => setTemperature(parseInt(e.target.value))}
                />
                <span>{temperature}K</span>
              </label>
              
              <label>
                유속 (v):
                <input 
                  type="range" 
                  min="0.1" 
                  max="3.0" 
                  step="0.1"
                  value={velocity}
                  onChange={(e) => setVelocity(parseFloat(e.target.value))}
                />
                <span>{velocity} m/s</span>
              </label>
              
              <Button onClick={startWarmup} disabled={isActive}>
                {isActive ? '웜업 진행 중...' : '🚀 웜업 시작'}
              </Button>
            </ControlPanel>
          </Section>
          
          <Section>
            <Title>3D 유체 시뮬레이션</Title>
            <div style={{ height: '400px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
              <Canvas camera={{ position: [10, 10, 10] }}>
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} />
                <FluidParticles viscosity={viscosity} pressure={pressure} />
                <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
              </Canvas>
            </div>
          </Section>
        </FluidGrid>
        
        <Section>
          <Title>실시간 유체 역학 분석</Title>
          <Plot
            data={plotData}
            layout={{
              width: '100%',
              height: 300,
              title: 'AI 사고 흐름 속도 분포',
              xaxis: { title: '시간 (s)', color: 'white' },
              yaxis: { title: '인지 속도 (normalized)', color: 'white' },
              paper_bgcolor: 'rgba(0,0,0,0)',
              plot_bgcolor: 'rgba(0,0,0,0.3)',
              font: { color: 'white' }
            }}
            style={{ width: '100%' }}
          />
        </Section>
        
        <Section>
          <Title>🧠 인지 최적화 결과</Title>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div style={{ background: 'rgba(0,255,0,0.2)', padding: '1rem', borderRadius: '8px' }}>
              <h4>처리 속도</h4>
              <p style={{ fontSize: '2rem', margin: 0 }}>{(velocity * 100).toFixed(0)}%</p>
            </div>
            <div style={{ background: 'rgba(255,255,0,0.2)', padding: '1rem', borderRadius: '8px' }}>
              <h4>효율성</h4>
              <p style={{ fontSize: '2rem', margin: 0 }}>{(95 + viscosity * 50).toFixed(1)}%</p>
            </div>
            <div style={{ background: 'rgba(255,0,255,0.2)', padding: '1rem', borderRadius: '8px' }}>
              <h4>안정성</h4>
              <p style={{ fontSize: '2rem', margin: 0 }}>{(pressure * 85).toFixed(1)}%</p>
            </div>
            <div style={{ background: 'rgba(0,255,255,0.2)', padding: '1rem', borderRadius: '8px' }}>
              <h4>온도 균형</h4>
              <p style={{ fontSize: '2rem', margin: 0 }}>{((400 - temperature) / 1.5).toFixed(0)}%</p>
            </div>
          </div>
        </Section>
      </motion.div>
    </WarmupContainer>
  );
}

export default NavierStokesWarmup;