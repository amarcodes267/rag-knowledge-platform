import { Link } from 'react-router-dom';
import Button from '../components/common/Button';

/**
 * 404 Not Found page for unmatched routes.
 */
function NotFound() {
  return (
    <div className="not-found-page">
      <div className="not-found-page__content">
        <div className="not-found-page__code">404</div>
        <h1 className="not-found-page__title">Page Not Found</h1>
        <p className="not-found-page__text">
          The page you are looking for does not exist or has been moved. 
          Please check the URL or navigate back to the homepage.
        </p>
        <Link to="/">
          <Button variant="primary" size="lg">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
              <polyline points="9 22 9 12 15 12 15 22" />
            </svg>
            Go Home
          </Button>
        </Link>
      </div>
    </div>
  );
}

export default NotFound;

