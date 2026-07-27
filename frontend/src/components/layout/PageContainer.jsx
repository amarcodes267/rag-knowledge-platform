/**
 * Page Container component.
 * Wraps page content to maintain consistent layout with proper spacing.
 */
function PageContainer({ children }) {
  return <main className="page-wrapper">{children}</main>;
}

export default PageContainer;

