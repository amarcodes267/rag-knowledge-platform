import { Link } from 'react-router-dom';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import '../styles/Home.css';

/**
 * Home page with hero section and feature highlights.
 */
function Home() {
  const features = [
    {
      title: 'Secure PDF Upload',
      description: 'Upload PDF documents securely with our enterprise-grade encryption and validation. Drag-and-drop support for seamless file management.',
      icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
          <polyline points="17 8 12 3 7 8" />
          <line x1="12" y1="3" x2="12" y2="15" />
        </svg>
      ),
    },
    {
      title: 'AI Knowledge Search',
      description: 'Intelligent semantic search across your document repository. Find relevant information instantly with context-aware results.',
      icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      ),
    },
    {
      title: 'Enterprise Intelligence',
      description: 'Transform documents into actionable knowledge. Leverage cutting-edge AI to extract insights and drive informed decision-making.',
      icon: (
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
        </svg>
      ),
    },
  ];

  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero__bg">
          <div className="hero__gradient"></div>
        </div>
        <div className="container">
          <div className="hero__content">
            <div className="hero__badge">
              <span className="hero__badge-dot"></span>
              Enterprise Knowledge Platform
            </div>
            <h1 className="hero__title">
              Transform Your Documents Into{' '}
              <span className="hero__title-highlight">Intelligent Knowledge</span>
            </h1>
            <p className="hero__subtitle">
              Upload, manage, and search enterprise documents with AI-powered intelligence.
              Streamline your knowledge management workflow with our cutting-edge platform.
            </p>
            <div className="hero__actions">
              <Link to="/upload">
                <Button variant="primary" size="lg">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
                    <polyline points="17 8 12 3 7 8" />
                    <line x1="12" y1="3" x2="12" y2="15" />
                  </svg>
                  Upload PDF
                </Button>
              </Link>
              <Link to="/about">
                <Button variant="outline" size="lg">
                  Learn More
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <div className="features-section__header">
            <h2 className="features-section__title">Why Choose Our Platform</h2>
            <p className="features-section__subtitle">
              Built for enterprises that demand security, scalability, and intelligence
              in their knowledge management systems.
            </p>
          </div>
          <div className="features-section__grid">
            {features.map((feature, index) => (
              <Card
                key={index}
                variant="feature"
                icon={feature.icon}
                title={feature.title}
              >
                <p>{feature.description}</p>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-section__content">
            <h2 className="cta-section__title">Ready to Get Started?</h2>
            <p className="cta-section__subtitle">
              Upload your first document and experience the future of enterprise knowledge management.
            </p>
            <Link to="/upload">
              <Button variant="primary" size="lg">
                Get Started Now
              </Button>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;

