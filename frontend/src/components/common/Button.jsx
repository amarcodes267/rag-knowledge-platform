/**
 * Reusable Button component with multiple variants and sizes.
 * 
 * @param {object} props
 * @param {string} [props.variant='primary'] - Button variant: 'primary', 'secondary', 'outline', 'ghost'
 * @param {string} [props.size='md'] - Button size: 'sm', 'md', 'lg'
 * @param {boolean} [props.loading=false] - Show loading spinner
 * @param {boolean} [props.disabled=false] - Disable button
 * @param {string} [props.className=''] - Additional CSS classes
 * @param {React.ReactNode} props.children - Button content
 * @param {function} props.onClick - Click handler
 */
function Button({
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  className = '',
  children,
  onClick,
  ...rest
}) {
  const baseClass = 'btn';
  const variantClass = `btn--${variant}`;
  const sizeClass = `btn--${size}`;
  const loadingClass = loading ? 'btn--loading' : '';

  return (
    <button
      className={`${baseClass} ${variantClass} ${sizeClass} ${loadingClass} ${className}`}
      onClick={onClick}
      disabled={disabled || loading}
      {...rest}
    >
      {loading && <span className="btn__spinner" aria-hidden="true"></span>}
      <span className={loading ? 'btn__text' : ''}>{children}</span>
    </button>
  );
}

export default Button;

