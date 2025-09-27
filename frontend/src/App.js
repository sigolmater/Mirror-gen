import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled from 'styled-components';
import Dashboard from './components/Dashboard';
import NavierStokesWarmup from './components/NavierStokesWarmup';
import AIOptimization from './components/AIOptimization';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  font-family: 'Arial', sans-serif;
  color: white;
`;

const Header = styled.header`
  text-align: center;
  padding: 2rem;
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
`;

const Title = styled.h1`
  font-size: 2.5rem;
  margin: 0;
  background: linear-gradient(45deg, #fff, #ffd700);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
`;

const Subtitle = styled.p`
  font-size: 1.2rem;
  margin-top: 0.5rem;
  opacity: 0.8;
`;

const Navigation = styled.nav`
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  
  a {
    color: white;
    text-decoration: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    transition: background-color 0.3s;
    
    &:hover {
      background-color: rgba(255, 255, 255, 0.2);
    }
  }
`;

function App() {
  return (
    <AppContainer>
      <Router>
        <Header>
          <Title>시골길 개인 AI 최적화 시스템</Title>
          <Subtitle>Personal AI Optimization System - Mirror Universal</Subtitle>
        </Header>
        
        <Navigation>
          <a href="/">Dashboard</a>
          <a href="/warmup">Navier-Stokes Warmup</a>
          <a href="/optimization">AI Optimization</a>
        </Navigation>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/warmup" element={<NavierStokesWarmup />} />
          <Route path="/optimization" element={<AIOptimization />} />
        </Routes>
      </Router>
    </AppContainer>
  );
}

export default App;