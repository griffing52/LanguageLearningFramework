/**
 * Dedicated TTS management page.
 */

import { FC, useEffect, useState } from 'react';
import { platformApi, TtsMethod, TtsProviderConfig } from '@/api/platform';
import '@/styles/components.css';

type InferenceTtsMethod = Exclude<TtsMethod, 'provider'>;

const TTS_METHOD_OPTIONS: Array<{ value: InferenceTtsMethod; label: string; description: string }> = [
  { value: 'speecht5', label: 'SpeechT5 local', description: 'Run the local fine-tuned SpeechT5 backend.' },
  { value: 'legacy_stitched', label: 'Legacy stitched audio', description: 'Use the legacy recording stitcher.' },
  { value: 'orpheus_lora', label: 'Orpheus LoRA', description: 'Run Orpheus LoRA backend (requires server-side support).' }
];

export const TtsWorkspace: FC = () => {
  const [providers, setProviders] = useState<TtsProviderConfig[]>([]);
  const [defaultProvider, setDefaultProvider] = useState<string>('');
  const [ttsResult, setTtsResult] = useState<string>('');
  const [audioSrc, setAudioSrc] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  const [providerForm, setProviderForm] = useState<TtsProviderConfig>({
    provider_id: 'remote-tts',
    name: 'Remote TTS Server',
    base_url: 'http://127.0.0.1:7001',
    synthesize_path: '/synthesize',
    health_path: '/health',
    api_key: '',
    enabled: true,
    extra_headers: {}
  });
  const [inferForm, setInferForm] = useState<{ provider_id: string; text: string; language: string; voice: string; tts_method: InferenceTtsMethod }>({
    provider_id: '',
    text: '',
    language: '',
    voice: '',
    tts_method: 'speecht5'
  });

  const loadTtsState = async () => {
    try {
      const ttsData = await platformApi.listTtsProviders();
      const nextProviders = ttsData.providers || [];
      const resolvedDefaultProvider = ttsData.default_provider || nextProviders[0]?.provider_id || '';
      setProviders(nextProviders);
      setDefaultProvider(resolvedDefaultProvider);
      if (resolvedDefaultProvider) {
        const selected = nextProviders.find(provider => provider.provider_id === resolvedDefaultProvider);
        if (selected) {
          setProviderForm(prev => ({
            ...prev,
            provider_id: selected.provider_id,
            name: selected.name,
            base_url: selected.base_url,
            synthesize_path: selected.synthesize_path,
            health_path: selected.health_path,
            api_key: selected.api_key || ''
          }));
        }
      }
      setInferForm(prev => {
        if (prev.provider_id || !resolvedDefaultProvider) {
          return prev;
        }

        return { ...prev, provider_id: resolvedDefaultProvider };
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
        provider_id: 'remote-tts',
        name: 'Remote TTS Server',
        base_url: 'http://127.0.0.1:7001',
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
      const selectedProvider = inferForm.provider_id || defaultProvider || undefined;
      const result = await platformApi.runTtsInference({
        provider_id: selectedProvider,
        text: inferForm.text,
        language: inferForm.language || undefined,
        voice: inferForm.voice || undefined,
        tts_method: inferForm.tts_method,
        options: {}
      });
      setTtsResult(JSON.stringify(result, null, 2));

      const responsePayload = (result as { response?: { audio_base64?: string; audio_file?: string } }).response;
      const topLevel = result as { audio_base64?: string; audio_file?: string };
      const audioBase64 = topLevel.audio_base64 || responsePayload?.audio_base64 || '';
      const audioFile = topLevel.audio_file || responsePayload?.audio_file || '';

      if (audioBase64) {
        const extension = audioFile.split('.').pop()?.toLowerCase() || 'wav';
        const mimeType = extension === 'mp3' ? 'audio/mpeg' : extension === 'ogg' ? 'audio/ogg' : 'audio/wav';
        setAudioSrc(`data:${mimeType};base64,${audioBase64}`);
      } else {
        setAudioSrc('');
      }

      setError(null);
    } catch (err) {
      setAudioSrc('');
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
              const nextMethod = e.target.value as InferenceTtsMethod;
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
          <option value="">Use default provider from API (.env)</option>
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
        {audioSrc && (
          <div className="workspace-inline" style={{ marginTop: '0.75rem' }}>
            <audio controls src={audioSrc} style={{ width: '100%' }} />
          </div>
        )}
        {ttsResult && <pre className="workspace-pre">{ttsResult}</pre>}
      </div>
    </section>
  );
};
