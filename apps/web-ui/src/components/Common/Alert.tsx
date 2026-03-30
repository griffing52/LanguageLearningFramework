/**
 * Alert component for displaying messages, errors, warnings, and info
 */

import React, { useEffect } from 'react';
import '@/styles/components.css';

export type AlertType = 'success' | 'error' | 'warning' | 'info';

interface AlertProps {
  type: AlertType;
  message: string;
  title?: string;
  onDismiss?: () => void;
  dismissible?: boolean;
  autoClose?: boolean;
  autoCloseDuration?: number; // ms
}

const getAlertIcon = (type: AlertType): string => {
  switch (type) {
    case 'success': return '✓';
    case 'error': return '!';
    case 'warning': return '⚠';
    case 'info': return 'i';
  }
};

export const Alert: React.FC<AlertProps> = ({
  type,
  message,
  title,
  onDismiss,
  dismissible = true,
  autoClose = type !== 'error',
  autoCloseDuration = 5000
}) => {
  useEffect(() => {
    if (autoClose && onDismiss) {
      const timer = setTimeout(onDismiss, autoCloseDuration);
      return () => clearTimeout(timer);
    }
  }, [autoClose, autoCloseDuration, onDismiss]);

  const icon = getAlertIcon(type);

  return (
    <div className={`alert alert-${type}`} role="alert">
      <div className="alert-content">
        <div className="alert-icon">{icon}</div>
        <div className="alert-message">
          {title && <div className="alert-title">{title}</div>}
          <div className="alert-text">{message}</div>
        </div>
      </div>
      {dismissible && onDismiss && (
        <button 
          className="alert-close"
          onClick={onDismiss}
          aria-label="Close alert"
        >
          ×
        </button>
      )}
    </div>
  );
};

/**
 * Container for displaying multiple alerts
 */
interface AlertContainerProps {
  alerts: Array<AlertProps & { id: string }>;
  onDismiss: (id: string) => void;
}

export const AlertContainer: React.FC<AlertContainerProps> = ({ alerts, onDismiss }) => {
  return (
    <div className="alert-container">
      {alerts.map(alert => (
        <Alert
          key={alert.id}
          {...alert}
          onDismiss={() => onDismiss(alert.id)}
        />
      ))}
    </div>
  );
};
