/**
 * Main App component
 */

import { useState } from 'react';
import { Header } from '@/components/Layout/Header';
import { StudyCard } from '@/components/Study/StudyCard';
import { ProgressIndicator } from '@/components/Study/ProgressIndicator';
import { WordList } from '@/components/Vocabulary/WordList';
import { Dashboard } from '@/components/Progress/Dashboard';
import { Workspace } from '@/components/Platform/Workspace';
import { TtsWorkspace } from '@/components/Platform/TtsWorkspace';
import { Alert, AlertType } from '@/components/Common/Alert';
import { useStudy } from '@/hooks/useStudy';
import '@/styles/globals.css';
import '@/styles/components.css';

type Page = 'study' | 'vocabulary' | 'progress' | 'workspace' | 'tts';

interface AppAlert {
  id: string;
  type: AlertType;
  title?: string;
  message: string;
}

export function App() {
  const [currentPage, setCurrentPage] = useState<Page>('study');
  const [alerts, setAlerts] = useState<AppAlert[]>([]);
  const study = useStudy(10);

  const showAlert = (type: AlertType, message: string, title?: string) => {
    const id = `${Date.now()}-${Math.random()}`;
    setAlerts(prev => [...prev, { id, type, message, title }]);
  };

  const dismissAlert = (id: string) => {
    setAlerts(prev => prev.filter(a => a.id !== id));
  };

  const handleStudyFeedback = async (correct: boolean, confidence: number, timeSpent: number) => {
    const success = await study.submitFeedback(correct, confidence, timeSpent);
    if (success) {
      const moved = await study.moveNext();
      if (!moved) {
        showAlert('success', 'Great job! You\'ve completed this lesson.', 'Lesson Complete');
      }
    } else if (study.error) {
      showAlert('error', study.error, 'Oops!');
    }
  };

  return (
    <div className="app">
      <Header currentPage={currentPage} onNavigate={setCurrentPage} />

      {/* Alert Container */}
      {alerts.length > 0 && (
        <div className="alert-container">
          {alerts.map(alert => (
            <Alert
              key={alert.id}
              type={alert.type}
              title={alert.title}
              message={alert.message}
              onDismiss={() => dismissAlert(alert.id)}
              dismissible={true}
              autoClose={alert.type !== 'error'}
            />
          ))}
        </div>
      )}

      <main className="app-container">
        {currentPage === 'study' && (
          <div className="study-section">
            <ProgressIndicator
              current={study.progress.current}
              total={study.progress.total}
              isComplete={study.isComplete}
            />

            {study.isLoading && <div className="loading">Loading lesson...</div>}

            {!study.isLoading && study.getCurrentTarget() && (
              <StudyCard
                target={study.getCurrentTarget()!}
                onFeedback={handleStudyFeedback}
                isLoading={false}
              />
            )}
          </div>
        )}

        {currentPage === 'vocabulary' && (
          <div className="vocabulary-section">
            <WordList limit={50} />
          </div>
        )}

        {currentPage === 'progress' && (
          <div className="progress-section">
            <Dashboard />
          </div>
        )}

        {currentPage === 'workspace' && (
          <div className="workspace-section">
            <Workspace />
          </div>
        )}

        {currentPage === 'tts' && (
          <div className="workspace-section">
            <TtsWorkspace />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
