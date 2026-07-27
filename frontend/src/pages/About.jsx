/**
 * About page explaining the project purpose and vision.
 */
function About() {
  return (
    <div className="about-page">
      <section className="section">
        <div className="container">
          <div className="page-header">
            <h1 className="page-title">About Our Platform</h1>
            <p className="page-subtitle">
              Empowering enterprises with intelligent document management and knowledge discovery.
            </p>
          </div>

          <div className="about-page__content">
            <div className="about-page__section">
              <h2 className="about-page__heading">Our Mission</h2>
              <p className="about-page__text">
                The Enterprise Knowledge Intelligence Platform is designed to revolutionize how
                organizations manage, search, and leverage their document repositories. We believe
                that enterprise knowledge should be accessible, searchable, and actionable — not
                locked away in silos or buried in folders.
              </p>
            </div>

            <div className="about-page__section">
              <h2 className="about-page__heading">What We Offer</h2>
              <p className="about-page__text">
                Our platform provides a secure, scalable foundation for document management with
                intelligent search capabilities. Upload PDF documents, organize your knowledge base,
                and discover insights through advanced search technology.
              </p>
            </div>

            <div className="about-page__section">
              <h2 className="about-page__heading">Built for the Future</h2>
              <p className="about-page__text">
                While currently focused on robust document upload and management, the platform is
                architecturally designed to seamlessly integrate AI-powered features including
                semantic search, intelligent chat, and automated knowledge extraction in future
                phases.
              </p>
            </div>

            <div className="about-page__stats">
              <div className="about-page__stat">
                <span className="about-page__stat-number">100%</span>
                <span className="about-page__stat-label">Secure Uploads</span>
              </div>
              <div className="about-page__stat">
                <span className="about-page__stat-number">PDF</span>
                <span className="about-page__stat-label">Format Support</span>
              </div>
              <div className="about-page__stat">
                <span className="about-page__stat-number">24/7</span>
                <span className="about-page__stat-label">Enterprise Ready</span>
              </div>
              <div className="about-page__stat">
                <span className="about-page__stat-number">50MB</span>
                <span className="about-page__stat-label">Max File Size</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default About;

