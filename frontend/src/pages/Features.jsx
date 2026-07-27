import Card from '../components/common/Card';

/**
 * Features page displaying all platform capabilities.
 * UI-only component showcasing feature cards.
 */
function Features() {
  const features = [
    {
      title: 'PDF Upload',
      description: 'Secure drag-and-drop PDF upload with real-time validation. Support for files up to 50MB with automatic virus scanning.',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
          <polyline points="17 8 12 3 7 8" />
          <line x1="12" y1="3" x2="12" y2="15" />
        </svg>
      ),
    },
    {
      title: 'Semantic Search',
      description: 'Advanced search capabilities that understand context and meaning. Find relevant documents quickly with intelligent query matching.',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
      ),
    },
    {
      title: 'AI Chat',
      description: 'Conversational interface for interacting with your documents. Ask questions and get contextual answers from your knowledge base.',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
        </svg>
      ),
    },
    {
      title: 'Fast Processing',
      description: 'Lightning-fast document upload and processing. Optimized backend ensures minimal wait times even for large PDF files.',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
        </svg>
      ),
    },
    {
      title: 'Secure Documents',
      description: 'Enterprise-grade security for your sensitive documents. Encrypted storage and secure transfer protocols protect your data.',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
          <path d="M7 11V7a5 5 0 0110 0v4" />
        </svg>
      ),
    },
    {
      title: 'Enterprise Ready',
      description: 'Built for scale with modular architecture. Easy integration with existing systems and workflows for seamless deployment.',
      icon: (
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
        </svg>
      ),
    },
  ];

  return (
    <div className="features-page">
      <section className="section">
        <div className="container">
          <div className="page-header">
            <h1 className="page-title">Platform Features</h1>
            <p className="page-subtitle">
              Discover the powerful features that make our platform the ideal choice for enterprise knowledge management.
            </p>
          </div>

          <div className="features-page__grid">
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
    </div>
  );
}

export default Features;

