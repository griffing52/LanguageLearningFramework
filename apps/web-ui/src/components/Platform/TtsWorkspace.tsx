/**
 * Dedicated TTS management page.
 */

import { FC, useEffect, useState } from 'react';
import { platformApi, TtsMethod, TtsProviderConfig } from '@/api/platform';
import '@/styles/components.css';

const TTS_METHOD_OPTIONS: Array<{ value: TtsMethod; label: string; description: string }> = [
  { value: 'provider', label: 'Remote provider', description: 'Use a configured TTS server.' },
  { value: 'speecht5', label: 'SpeechT5 local', description: 'Run the local fine-tuned SpeechT5 backend.' },
  { value: 'legacy_stitched', label: 'Legacy stitched audio', description: 'Use the legacy recording stitcher.' },
  { value: 'orpheus_lora', label: 'Orpheus LoRA', description: 'Run Orpheus LoRA via Hugging Face inference.' }
];

export const TtsWorkspace: FC = () => {
  const [providers, setProviders] = useState<TtsProviderConfig[]>([]);
  const [defaultProvider, setDefaultProvider] = useState<string>('');
  const [ttsResult, setTtsResult] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

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
  const [inferForm, setInferForm] = useState<{ provider_id: string; text: string; language: string; voice: string; tts_method: TtsMethod }>({
    provider_id: '',
    text: '',
    language: '',
    voice: '',
    tts_method: 'provider'
  });

  const loadTtsState = async () => {
    try {
      const ttsData = await platformApi.listTtsProviders();
      setProviders(ttsData.providers || []);
      setDefaultProvider(ttsData.default_provider || '');
      setInferForm(prev => {
        if (prev.provider_id || !ttsData.default_provider) {
          return prev;
        }

        return { ...prev, provider_id: ttsData.default_provider || '' };
      });
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load TTS state');
    }
  };

  useEffect(() => {
    void loadTtsState();
  }, []);

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
      await loadTtsState();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save provider');
    }
  };

  const makeDefault = async (providerId: string) => {
    try {
      await platformApi.setDefaultProvider(providerId);
      await loadTtsState();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to set default provider');
    }
  };

  const runInference = async () => {
    try {
      const result = await platformApi.runTtsInference({
        provider_id: inferForm.provider_id || undefined,
        text: inferForm.text,
        language: inferForm.language || undefined,
        voice: inferForm.voice || undefined,
        tts_method: inferForm.tts_method,
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

      <div className="workspace-card workspace-wide">
        <h2>TTS Provider Config</h2>
        <p className="subtitle">Keep speech generation separate from study/data management.</p>

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
        <h2>TTS Inference</h2>
        <div className="workspace-inline">
          <select
            value={inferForm.tts_method}
            onChange={e => {
              const nextMethod = e.target.value as TtsMethod;
              setInferForm(prev => ({
                ...prev,
                tts_method: nextMethod,
                provider_id: prev.provider_id || defaultProvider || ''
              }));
            }}
          >
            {TTS_METHOD_OPTIONS.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
          <small className="subtitle">
            {TTS_METHOD_OPTIONS.find(option => option.value === inferForm.tts_method)?.description}
          </small>
        </div>
        <select value={inferForm.provider_id} onChange={e => setInferForm({ ...inferForm, provider_id: e.target.value })}>
          <option value="">Run on local API host</option>
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
