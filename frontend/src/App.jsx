import { Routes, Route } from 'react-router-dom';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import PageContainer from './components/layout/PageContainer';
import Home from './pages/Home';
import About from './pages/About';
import Features from './pages/Features';
import Upload from './pages/Upload';
import Chat from './pages/Chat';
import Contact from './pages/Contact';
import NotFound from './pages/NotFound';

/**
 * Main application component with routing configuration.
 * All routes are wrapped in PageContainer for consistent layout.
 */
function App() {
  return (
    <div className="app">
      <Navbar />
      <PageContainer>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/features" element={<Features />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </PageContainer>
      <Footer />
    </div>
  );
}

export default App;

