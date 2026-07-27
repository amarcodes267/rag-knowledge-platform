/**
 * Loader component for displaying loading states.
 * 
 * @param {object} props
 * @param {string} [props.size='md'] - Loader size: 'sm', 'md', 'lg'
 * @param {string} [props.label='Loading...'] - Accessible label
 */
function Loader({ size = 'md', label = 'Loading...' }) {
  return (
    <div className="loader" role="status" aria-label={label}>
      <div className={`loader__spinner loader__spinner--${size}`}>
        <div className="loader__ring"></div>
        <div className="loader__ring loader__ring--reverse"></div>
      </div>
      {label && <span className="loader__label">{label}</span>}
    </div>
  );
}

export default Loader;

