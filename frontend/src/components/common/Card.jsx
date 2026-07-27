/**
 * Reusable Card component with optional hover effects, icon, and title.
 * 
 * @param {object} props
 * @param {string} [props.variant='default'] - Card variant: 'default', 'hover', 'feature'
 * @param {React.ReactNode} [props.icon] - Icon element to display
 * @param {string} [props.title] - Card title
 * @param {string} [props.className=''] - Additional CSS classes
 * @param {React.ReactNode} props.children - Card content
 */
function Card({ variant = 'default', icon, title, className = '', children }) {
  const variantClass = `card card--${variant}`;

  return (
    <div className={`${variantClass} ${className}`}>
      {icon && <div className="card__icon">{icon}</div>}
      {title && <h3 className="card__title">{title}</h3>}
      <div className="card__content">{children}</div>
    </div>
  );
}

export default Card;

