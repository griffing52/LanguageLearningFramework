/**
 * Workspace component for cohesive platform operations.
 */

import { FC, useEffect, useState } from 'react';
import { platformApi, LessonDefinition, TtsProviderConfig, PlatformStatus } from '@/api/platform';
import '@/styles/components.css';

export const Workspace: FC = () => {
  const [status, setStatus] = useState<PlatformStatus | null>(null);
  const [lessons, setLessons] = useState<LessonDefinition[]>([]);
  const [providers, setProviders] = useState<TtsProviderConfig[]>([]);
  const [defaultProvider, setDefaultProvider] = useState<string>('');
  const [ttsResult, setTtsResult] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  const [wordForm, setWordForm] = useState({ value: '', translation: '', complexity: 1, frequency: 0, age: 0 });
  const [phraseForm, setPhraseForm] = useState({ value: '', translation: '', complexity: 1, frequency: 0, age: 0 });
  const [lessonForm, setLessonForm] = useState({ lesson_id: '', name: '', description: '', items_raw: '' });
  const [providerForm, setProviderForm] = useState<TtsProviderConfig>({
    provider_id: '',
    name: '',
    base_url: '',
    synthesize_path: '/synthesize',
    health_path: '/health',
    api_key: '',
    enabled: true,
    extra_headers: {}
  });
  const [inferForm, setInferForm] = useState({ provider_id: '', text: '', language: '', voice: '' });

  const loadAll = async () => {
    try {
      const [statusData, lessonsData, ttsData] = await Promise.all([
        platformApi.getStatus(),
        platformApi.listLessons(),
        platformApi.listTtsProviders()
      ]);
      setStatus(statusData);
      setLessons(lessonsData);
      setProviders(ttsData.providers || []);
      setDefaultProvider(ttsData.default_provider || '');
      if (!inferForm.provider_id && ttsData.default_provider) {
        setInferForm(prev => ({ ...prev, provider_id: ttsData.default_provider || '' }));
      }
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
    }
  };

  const submitPhrase = async () => {
    try {
      await platformApi.addPhrase(phraseForm);
      setPhraseForm({ value: '', translation: '', complexity: 1, frequency: 0, age: 0 });
      await loadAll();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add phrase');
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
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create lesson');
    }
  };

  const submitProvider = async () => {
    try {
      await platformApi.upsertTtsProvider(providerForm);
      setProviderForm({
        provider_id: '',
        name: '',
        base_url: '',
        synthesize_path: '/synthesize',
        health_path: '/health',
        api_key: '',
        enabled: true,
        extra_headers: {}
      });
      await loadAll();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save provider');
    }
  };

  const makeDefault = async (providerId: string) => {
    try {
      await platformApi.setDefaultProvider(providerId);
      await loadAll();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to set default provider');
    }
  };

  const runInference = async () => {
    try {
      const result = await platformApi.runTtsInference({
        provider_id: inferForm.provider_id,
        text: inferForm.text,
        language: inferForm.language || undefined,
        voice: inferForm.voice || undefined,
        options: {}
      });
      setTtsResult(JSON.stringify(result, null, 2));
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Inference failed');
    }
  };

  return (
    <section className="workspace-grid">
      {error && <div className="error-message workspace-alert">{error}</div>}

      <div className="workspace-card workspace-status">
        <h2>Platform Status</h2>
        <div className="workspace-kpis">
          <div><strong>Words:</strong> {status?.counts.words ?? 0}</div>
          <div><strong>Phrases:</strong> {status?.counts.phrases ?? 0}</div>
          <div><strong>Lessons:</strong> {status?.counts.lessons ?? 0}</div>
          <div><strong>TTS Providers:</strong> {status?.counts.tts_providers ?? 0}</div>
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

      <div className="workspace-card workspace-wide">
        <h3>TTS Provider Config</h3>
        <input placeholder="Provider ID" value={providerForm.provider_id} onChange={e => setProviderForm({ ...providerForm, provider_id: e.target.value })} />
        <input placeholder="Display Name" value={providerForm.name} onChange={e => setProviderForm({ ...providerForm, name: e.target.value })} />
        <input placeholder="Base URL" value={providerForm.base_url} onChange={e => setProviderForm({ ...providerForm, base_url: e.target.value })} />
        <div className="workspace-inline">
          <input placeholder="Synthesize Path" value={providerForm.synthesize_path} onChange={e => setProviderForm({ ...providerForm, synthesize_path: e.target.value })} />
          <input placeholder="Health Path" value={providerForm.health_path} onChange={e => setProviderForm({ ...providerForm, health_path: e.target.value })} />
        </div>
        <input placeholder="API key (optional)" value={providerForm.api_key || ''} onChange={e => setProviderForm({ ...providerForm, api_key: e.target.value })} />
        <button className="btn btn-primary" onClick={submitProvider}>Save Provider</button>

        <div className="workspace-list">
          {providers.map(provider => (
            <div className="workspace-list-item" key={provider.provider_id}>
              <div>
                <strong>{provider.name}</strong>
                <span>{provider.provider_id}</span>
              </div>
              <div className="workspace-inline-actions">
                {defaultProvider === provider.provider_id ? (
                  <span className="pill">Default</span>
                ) : (
                  <button className="btn btn-secondary" onClick={() => makeDefault(provider.provider_id)}>Set Default</button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="workspace-card workspace-wide">
        <h3>TTS Inference</h3>
        <select value={inferForm.provider_id} onChange={e => setInferForm({ ...inferForm, provider_id: e.target.value })}>
          <option value="">Select provider</option>
          {providers.map(provider => (
            <option key={provider.provider_id} value={provider.provider_id}>{provider.name}</option>
          ))}
        </select>
        <textarea
          className="workspace-textarea"
          placeholder="Text to synthesize"
          value={inferForm.text}
          onChange={e => setInferForm({ ...inferForm, text: e.target.value })}
        />
        <div className="workspace-inline">
          <input placeholder="Language (optional)" value={inferForm.language} onChange={e => setInferForm({ ...inferForm, language: e.target.value })} />
          <input placeholder="Voice (optional)" value={inferForm.voice} onChange={e => setInferForm({ ...inferForm, voice: e.target.value })} />
        </div>
        <button className="btn btn-primary" onClick={runInference}>Run Inference</button>
        {ttsResult && <pre className="workspace-pre">{ttsResult}</pre>}
      </div>
    </section>
  );
};
