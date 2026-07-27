import { useState } from 'react';
import '../styles/Contact.css';

/**
 * Contact page with form validation.
 * Frontend validation only - no backend submission.
 */
function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: '',
  });
  const [errors, setErrors] = useState({});
  const [isSubmitted, setIsSubmitted] = useState(false);

  /**
   * Validate form fields.
   * @returns {boolean} Whether the form is valid
   */
  const validateForm = () => {
    const newErrors = {};

    if (!formData.name.trim()) {
      newErrors.name = 'Name is required';
    } else if (formData.name.trim().length < 2) {
      newErrors.name = 'Name must be at least 2 characters';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!formData.message.trim()) {
      newErrors.message = 'Message is required';
    } else if (formData.message.trim().length < 10) {
      newErrors.message = 'Message must be at least 10 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  /**
   * Handle input change.
   */
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    // Clear error for the field being edited
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  /**
   * Handle form submission.
   */
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      setIsSubmitted(true);
      // Reset form after successful submission
      setTimeout(() => {
        setFormData({ name: '', email: '', message: '' });
        setIsSubmitted(false);
      }, 3000);
    }
  };

  return (
    <div className="contact-page">
      <section className="section">
        <div className="container">
          <div className="page-header">
            <h1 className="page-title">Contact Us</h1>
            <p className="page-subtitle">
              Have questions or feedback? We'd love to hear from you.
            </p>
          </div>

          <div className="contact-page__content">
            <div className="contact-form">
              {isSubmitted ? (
                <div className="contact-form__success">
                  <div className="contact-form__success-icon">
                    <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M22 11.08V12a10 10 0 11-5.93-9.14" />
                      <polyline points="22 4 12 14.01 9 11.01" />
                    </svg>
                  </div>
                  <h3 className="contact-form__success-title">Message Sent!</h3>
                  <p className="contact-form__success-text">
                    Thank you for reaching out. We'll get back to you shortly.
                  </p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} noValidate>
                  <div className="contact-form__group">
                    <label htmlFor="name" className="contact-form__label">
                      Full Name
                    </label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      className={`contact-form__input ${errors.name ? 'contact-form__input--error' : ''}`}
                      placeholder="John Doe"
                      value={formData.name}
                      onChange={handleChange}
                    />
                    {errors.name && (
                      <span className="contact-form__error">{errors.name}</span>
                    )}
                  </div>

                  <div className="contact-form__group">
                    <label htmlFor="email" className="contact-form__label">
                      Email Address
                    </label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      className={`contact-form__input ${errors.email ? 'contact-form__input--error' : ''}`}
                      placeholder="john@example.com"
                      value={formData.email}
                      onChange={handleChange}
                    />
                    {errors.email && (
                      <span className="contact-form__error">{errors.email}</span>
                    )}
                  </div>

                  <div className="contact-form__group">
                    <label htmlFor="message" className="contact-form__label">
                      Message
                    </label>
                    <textarea
                      id="message"
                      name="message"
                      className={`contact-form__textarea ${errors.message ? 'contact-form__textarea--error' : ''}`}
                      placeholder="Tell us about your inquiry..."
                      rows={6}
                      value={formData.message}
                      onChange={handleChange}
                    />
                    {errors.message && (
                      <span className="contact-form__error">{errors.message}</span>
                    )}
                  </div>

                  <button type="submit" className="contact-form__submit btn btn--primary btn--lg">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <line x1="22" y1="2" x2="11" y2="13" />
                      <polygon points="22 2 15 22 11 13 2 9 22 2" />
                    </svg>
                    Send Message
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Contact;

