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
import { useStudy } from '@/hooks/useStudy';
import '@/styles/globals.css';
import '@/styles/components.css';

type Page = 'study' | 'vocabulary' | 'progress' | 'workspace' | 'tts';

export function App() {
  const [currentPage, setCurrentPage] = useState<Page>('study');
  const study = useStudy(10);

  const handleStudyFeedback = async (correct: boolean, confidence: number, timeSpent: number) => {
    const success = await study.submitFeedback(correct, confidence, timeSpent);
    if (success) {
      const moved = await study.moveNext();
      if (!moved) {
        // Lesson complete, could show a celebration or reset
        console.log('Lesson completed!');
      }
    }
  };

  return (
    <div className="app">
      <Header currentPage={currentPage} onNavigate={setCurrentPage} />

      <main className="app-container">
        {currentPage === 'study' && (
          <div className="study-section">
            <ProgressIndicator
              current={study.progress.current}
              total={study.progress.total}
              isComplete={study.isComplete}
            />

            {study.isLoading && <div className="loading">Loading lesson...</div>}
            {study.error && <div className="error-message">{study.error}</div>}

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
