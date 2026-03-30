/**
 * Workspace component for data and planning operations.
 */

import { FC, useEffect, useState } from 'react';
import { platformApi, LessonDefinition, PlatformStatus, TeachingStatistics } from '@/api/platform';
import '@/styles/components.css';

export const Workspace: FC = () => {
  const [status, setStatus] = useState<PlatformStatus | null>(null);
  const [lessons, setLessons] = useState<LessonDefinition[]>([]);
  const [teachingStats, setTeachingStats] = useState<TeachingStatistics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const [wordForm, setWordForm] = useState({ value: '', translation: '', complexity: 1, frequency: 0, age: 0 });
  const [phraseForm, setPhraseForm] = useState({ value: '', translation: '', complexity: 1, frequency: 0, age: 0 });
  const [lessonForm, setLessonForm] = useState({ lesson_id: '', name: '', description: '', items_raw: '' });
  const [importMode, setImportMode] = useState<'replace' | 'append'>('replace');
  const [wordsFile, setWordsFile] = useState<File | null>(null);
  const [phrasesFile, setPhrasesFile] = useState<File | null>(null);
  const [memoryFile, setMemoryFile] = useState<File | null>(null);
  const [memoryExportName, setMemoryExportName] = useState('');

  const loadAll = async () => {
    try {
      const [statusData, lessonsData, statsData] = await Promise.all([
        platformApi.getStatus(),
        platformApi.listLessons(),
        platformApi.getTeachingStatistics(10)
      ]);
      setStatus(statusData);
      setLessons(lessonsData);
      setTeachingStats(statsData);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load workspace state');
    }
  };

  useEffect(() => {
    void loadAll();
  }, []);

  const submitWord = async () => {
    try {
      await platformApi.addWord(wordForm);
      setWordForm({ value: '', translation: '', complexity: 1, frequency: 0, age: 0 });
      await loadAll();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add word');
      setMessage(null);
    }
  };

  const submitPhrase = async () => {
    try {
      await platformApi.addPhrase(phraseForm);
      setPhraseForm({ value: '', translation: '', complexity: 1, frequency: 0, age: 0 });
      await loadAll();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add phrase');
      setMessage(null);
    }
  };

  const submitLesson = async () => {
    try {
      const items = lessonForm.items_raw
        .split('\n')
        .map(line => line.trim())
        .filter(Boolean)
        .map(line => {
          const [item_type, ...rest] = line.split(':');
          return { item_type: (item_type || 'word') as 'word' | 'phrase', value: rest.join(':').trim() };
        });

      await platformApi.createLesson({
        lesson_id: lessonForm.lesson_id,
        name: lessonForm.name,
        description: lessonForm.description,
        items
      });

      setLessonForm({ lesson_id: '', name: '', description: '', items_raw: '' });
      await loadAll();
      setMessage('Lesson created successfully.');
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create lesson');
      setMessage(null);
    }
  };

  const runImport = async (kind: 'words' | 'phrases' | 'memory') => {
    try {
      const fileMap = {
        words: wordsFile,
        phrases: phrasesFile,
        memory: memoryFile,
      };
      const selected = fileMap[kind];

      if (!selected) {
        setError(`Select a ${kind} file first.`);
        setMessage(null);
        return;
      }

      if (kind === 'words') {
        await platformApi.importWords(selected, importMode);
        setWordsFile(null);
      } else if (kind === 'phrases') {
        await platformApi.importPhrases(selected, importMode);
        setPhrasesFile(null);
      } else {
        await platformApi.importMemory(selected, importMode);
        setMemoryFile(null);
      }

      await loadAll();
      setMessage(`${kind} import completed (${importMode}).`);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : `Failed to import ${kind}`);
      setMessage(null);
    }
  };

  const saveMemory = async () => {
    try {
      await platformApi.saveMemoryState(memoryExportName.trim() || undefined);
      await loadAll();
      setMessage('Memory state saved.');
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save memory state');
      setMessage(null);
    }
  };

  const clearData = async (target: 'words' | 'phrases' | 'memory' | 'all') => {
    try {
      await platformApi.clearDataset(target);
      await loadAll();
      setMessage(`Cleared ${target}.`);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : `Failed to clear ${target}`);
      setMessage(null);
    }
  };

  return (
    <section className="workspace-grid">
      {error && <div className="error-message workspace-alert">{error}</div>}
      {message && <div className="workspace-success workspace-alert">{message}</div>}

      <div className="workspace-card workspace-status">
        <h2>Platform Status</h2>
        <div className="workspace-kpis">
          <div><strong>Words:</strong> {status?.counts.words ?? 0}</div>
          <div><strong>Phrases:</strong> {status?.counts.phrases ?? 0}</div>
          <div><strong>Lessons:</strong> {status?.counts.lessons ?? 0}</div>
          <div><strong>Memory Entries:</strong> {status?.counts.memory_entries ?? 0}</div>
        </div>
      </div>

      <div className="workspace-card">
        <h3>Add Word</h3>
        <input placeholder="Word" value={wordForm.value} onChange={e => setWordForm({ ...wordForm, value: e.target.value })} />
        <input placeholder="Translation" value={wordForm.translation} onChange={e => setWordForm({ ...wordForm, translation: e.target.value })} />
        <div className="workspace-inline">
          <input type="number" min={1} value={wordForm.complexity} onChange={e => setWordForm({ ...wordForm, complexity: Number(e.target.value) })} />
          <input type="number" min={0} value={wordForm.frequency} onChange={e => setWordForm({ ...wordForm, frequency: Number(e.target.value) })} />
          <input type="number" min={0} value={wordForm.age} onChange={e => setWordForm({ ...wordForm, age: Number(e.target.value) })} />
        </div>
        <button className="btn btn-success" onClick={submitWord}>Save Word</button>
      </div>

      <div className="workspace-card">
        <h3>Add Phrase</h3>
        <input placeholder="Phrase" value={phraseForm.value} onChange={e => setPhraseForm({ ...phraseForm, value: e.target.value })} />
        <input placeholder="Translation" value={phraseForm.translation} onChange={e => setPhraseForm({ ...phraseForm, translation: e.target.value })} />
        <div className="workspace-inline">
          <input type="number" min={1} value={phraseForm.complexity} onChange={e => setPhraseForm({ ...phraseForm, complexity: Number(e.target.value) })} />
          <input type="number" min={0} value={phraseForm.frequency} onChange={e => setPhraseForm({ ...phraseForm, frequency: Number(e.target.value) })} />
          <input type="number" min={0} value={phraseForm.age} onChange={e => setPhraseForm({ ...phraseForm, age: Number(e.target.value) })} />
        </div>
        <button className="btn btn-success" onClick={submitPhrase}>Save Phrase</button>
      </div>

      <div className="workspace-card workspace-wide">
        <h3>Create Lesson</h3>
        <input placeholder="Lesson ID" value={lessonForm.lesson_id} onChange={e => setLessonForm({ ...lessonForm, lesson_id: e.target.value })} />
        <input placeholder="Lesson name" value={lessonForm.name} onChange={e => setLessonForm({ ...lessonForm, name: e.target.value })} />
        <input placeholder="Description" value={lessonForm.description} onChange={e => setLessonForm({ ...lessonForm, description: e.target.value })} />
        <textarea
          className="workspace-textarea"
          placeholder="Items (one per line): word:Gruezi or phrase:Guten Morgen"
          value={lessonForm.items_raw}
          onChange={e => setLessonForm({ ...lessonForm, items_raw: e.target.value })}
        />
        <button className="btn btn-primary" onClick={submitLesson}>Create Lesson</button>
      </div>

      <div className="workspace-card workspace-wide">
        <h3>Import CLI Files</h3>
        <div className="workspace-inline">
          <label className="workspace-label">Import Mode</label>
          <select value={importMode} onChange={e => setImportMode(e.target.value as 'replace' | 'append')}>
            <option value="replace">Replace existing</option>
            <option value="append">Append to existing</option>
          </select>
        </div>
        <div className="workspace-file-row">
          <label className="workspace-label">Words file</label>
          <input type="file" accept=".txt,.csv" onChange={e => setWordsFile(e.target.files?.[0] || null)} />
          <button className="btn btn-primary" onClick={() => runImport('words')}>Upload Words</button>
        </div>
        <div className="workspace-file-row">
          <label className="workspace-label">Phrases file</label>
          <input type="file" accept=".txt,.csv" onChange={e => setPhrasesFile(e.target.files?.[0] || null)} />
          <button className="btn btn-primary" onClick={() => runImport('phrases')}>Upload Phrases</button>
        </div>
        <div className="workspace-file-row">
          <label className="workspace-label">Memory file</label>
          <input type="file" accept=".txt,.json" onChange={e => setMemoryFile(e.target.files?.[0] || null)} />
          <button className="btn btn-primary" onClick={() => runImport('memory')}>Upload Memory</button>
        </div>
      </div>

      <div className="workspace-card workspace-wide">
        <h3>Memory and Dataset Controls</h3>
        <div className="workspace-inline">
          <input
            placeholder="Optional export file name (example: mem_snapshot.json)"
            value={memoryExportName}
            onChange={e => setMemoryExportName(e.target.value)}
          />
          <button className="btn btn-success" onClick={saveMemory}>Save Memory State</button>
        </div>
        <div className="workspace-inline-actions">
          <button className="btn btn-secondary" onClick={() => clearData('memory')}>Clear Memory</button>
          <button className="btn btn-secondary" onClick={() => clearData('phrases')}>Clear Phrases</button>
          <button className="btn btn-secondary" onClick={() => clearData('words')}>Clear Words</button>
          <button className="btn btn-error" onClick={() => clearData('all')}>Clear All</button>
        </div>
      </div>

      <div className="workspace-card workspace-wide">
        <h3>Teaching Statistics</h3>
        <div className="workspace-kpis">
          <div><strong>Total taught events:</strong> {teachingStats?.summary.total_taught_frequency ?? 0}</div>
          <div><strong>Word taught events:</strong> {teachingStats?.summary.total_word_frequency ?? 0}</div>
          <div><strong>Phrase taught events:</strong> {teachingStats?.summary.total_phrase_frequency ?? 0}</div>
          <div><strong>Taught items:</strong> {(teachingStats?.summary.taught_words ?? 0) + (teachingStats?.summary.taught_phrases ?? 0)}</div>
        </div>
        <div className="workspace-two-col">
          <div>
            <h4>Top Words</h4>
            <div className="workspace-list">
              {(teachingStats?.top_words || []).map(item => (
                <div className="workspace-list-item" key={`word-${item.value}`}>
                  <div>
                    <strong>{item.value}</strong>
                    <small>{item.translation}</small>
                  </div>
                  <span className="pill">{item.frequency}</span>
                </div>
              ))}
            </div>
          </div>
          <div>
            <h4>Top Phrases</h4>
            <div className="workspace-list">
              {(teachingStats?.top_phrases || []).map(item => (
                <div className="workspace-list-item" key={`phrase-${item.value}`}>
                  <div>
                    <strong>{item.value}</strong>
                    <small>{item.translation}</small>
                  </div>
                  <span className="pill">{item.frequency}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="workspace-card workspace-wide">
        <h3>Lesson Catalog</h3>
        {lessons.length === 0 && <p className="empty-state">No lessons yet.</p>}
        {lessons.map(lesson => (
          <div className="workspace-list-item" key={lesson.lesson_id}>
            <strong>{lesson.name}</strong>
            <span>{lesson.lesson_id}</span>
            <small>{lesson.items.length} items</small>
          </div>
        ))}
      </div>
    </section>
  );
};
