"use client";

import { AudioLesson } from "@/src/modules/audio-lesson/domain/types";
import { LessonPlan } from "@/src/modules/lesson-planner/domain/types";
import { FormEvent, useMemo, useState } from "react";

interface PlannerFormState {
  learnerId: string;
  languageCode: string;
  targetGoal: string;
  maxItems: number;
}

const DEFAULT_FORM: PlannerFormState = {
  learnerId: "demo-learner-1",
  languageCode: "gsw-CH",
  targetGoal: "travel and cafe basics",
  maxItems: 3,
};

export function LessonWorkbench() {
  const [form, setForm] = useState<PlannerFormState>(DEFAULT_FORM);
  const [plan, setPlan] = useState<LessonPlan | null>(null);
  const [audioLesson, setAudioLesson] = useState<AudioLesson | null>(null);
  const [isPlanning, setIsPlanning] = useState(false);
  const [isGeneratingAudio, setIsGeneratingAudio] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const hasSpeechSupport = useMemo(() => {
    return typeof window !== "undefined" && "speechSynthesis" in window;
  }, []);

  async function submitPlanner(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setIsPlanning(true);
    setAudioLesson(null);

    try {
      const response = await fetch("/api/lessons/plan", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify(form),
      });

      if (!response.ok) {
        const payload = (await response.json()) as { error?: string };
        throw new Error(payload.error ?? "Unable to plan lesson.");
      }

      const payload = (await response.json()) as LessonPlan;
      setPlan(payload);
    } catch (reason) {
      const message =
        reason instanceof Error ? reason.message : "Unexpected error.";
      setError(message);
    } finally {
      setIsPlanning(false);
    }
  }

  async function generateAudio() {
    if (!plan) {
      return;
    }

    setError(null);
    setIsGeneratingAudio(true);

    try {
      const response = await fetch("/api/audio/generate", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ lessonPlan: plan }),
      });

      if (!response.ok) {
        const payload = (await response.json()) as { error?: string };
        throw new Error(payload.error ?? "Unable to generate audio.");
      }

      const payload = (await response.json()) as AudioLesson;
      setAudioLesson(payload);
    } catch (reason) {
      const message =
        reason instanceof Error ? reason.message : "Unexpected error.";
      setError(message);
    } finally {
      setIsGeneratingAudio(false);
    }
  }

  function playWithBrowserTts() {
    if (!audioLesson || !hasSpeechSupport) {
      return;
    }

    window.speechSynthesis.cancel();

    audioLesson.transcript.forEach((segment) => {
      const utterance = new SpeechSynthesisUtterance(segment.text);
      utterance.lang = audioLesson.languageCode;
      window.speechSynthesis.speak(utterance);
    });
  }

  return (
    <main className="mx-auto flex w-full max-w-6xl flex-1 flex-col gap-8 px-4 py-10 sm:px-8">
      <section className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm">
        <h1 className="text-3xl font-semibold text-zinc-900">
          Adaptive Language Lesson Studio
        </h1>
        <p className="mt-2 max-w-3xl text-zinc-600">
          Plan practical phrase-first lessons, then convert the lesson plan into
          a narrated audio lesson through a modular synthesis pipeline.
        </p>
      </section>

      <section className="grid gap-6 lg:grid-cols-2">
        <form
          onSubmit={submitPlanner}
          className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm"
        >
          <h2 className="text-xl font-semibold text-zinc-900">Plan Lesson</h2>
          <div className="mt-5 grid gap-4">
            <label className="grid gap-1 text-sm text-zinc-700">
              Learner ID
              <input
                className="rounded-xl border border-zinc-300 px-3 py-2"
                value={form.learnerId}
                onChange={(event) =>
                  setForm((current) => ({
                    ...current,
                    learnerId: event.target.value,
                  }))
                }
              />
            </label>

            <label className="grid gap-1 text-sm text-zinc-700">
              Language Code
              <select
                className="rounded-xl border border-zinc-300 px-3 py-2"
                value={form.languageCode}
                onChange={(event) =>
                  setForm((current) => ({
                    ...current,
                    languageCode: event.target.value,
                  }))
                }
              >
                <option value="gsw-CH">Swiss German</option>
                <option value="en">English (demo)</option>
              </select>
            </label>

            <label className="grid gap-1 text-sm text-zinc-700">
              Goal
              <input
                className="rounded-xl border border-zinc-300 px-3 py-2"
                value={form.targetGoal}
                onChange={(event) =>
                  setForm((current) => ({
                    ...current,
                    targetGoal: event.target.value,
                  }))
                }
              />
            </label>

            <label className="grid gap-1 text-sm text-zinc-700">
              Max Items
              <input
                className="rounded-xl border border-zinc-300 px-3 py-2"
                type="number"
                min={1}
                max={6}
                value={form.maxItems}
                onChange={(event) =>
                  setForm((current) => ({
                    ...current,
                    maxItems: Number(event.target.value),
                  }))
                }
              />
            </label>
          </div>

          <button
            className="mt-6 rounded-xl bg-zinc-900 px-4 py-2 text-white disabled:opacity-50"
            disabled={isPlanning}
            type="submit"
          >
            {isPlanning ? "Planning..." : "Create Lesson Plan"}
          </button>

          {error ? <p className="mt-4 text-sm text-red-600">{error}</p> : null}
        </form>

        <section className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-semibold text-zinc-900">Lesson Plan</h2>

          {!plan ? (
            <p className="mt-4 text-zinc-600">
              Create a plan to inspect phrase dependencies and priorities.
            </p>
          ) : (
            <div className="mt-4 space-y-3">
              <p className="text-sm text-zinc-500">Plan ID: {plan.planId}</p>
              {plan.items.map((item) => (
                <article
                  key={item.phraseId}
                  className="rounded-xl border border-zinc-200 bg-zinc-50 p-3"
                >
                  <p className="font-medium text-zinc-900">{item.phraseText}</p>
                  <p className="text-sm text-zinc-600">{item.meaning}</p>
                  <p className="mt-2 text-xs text-zinc-500">
                    Unknown concepts: {item.unknownConceptIds.join(", ")}
                  </p>
                </article>
              ))}
            </div>
          )}

          <button
            className="mt-6 rounded-xl border border-zinc-300 px-4 py-2 text-zinc-900 disabled:opacity-50"
            disabled={!plan || isGeneratingAudio}
            onClick={generateAudio}
            type="button"
          >
            {isGeneratingAudio ? "Generating audio..." : "Generate Audio Lesson"}
          </button>
        </section>
      </section>

      <section className="rounded-3xl border border-zinc-200 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold text-zinc-900">Narration</h2>
        {!audioLesson ? (
          <p className="mt-3 text-zinc-600">
            Generate audio to preview narration segments and stream endpoint.
          </p>
        ) : (
          <div className="mt-4 space-y-3">
            <p className="text-sm text-zinc-600">
              Provider: {audioLesson.provider} | Stream URL: {audioLesson.streamUrl}
            </p>
            <ol className="list-decimal space-y-1 pl-5 text-zinc-700">
              {audioLesson.transcript.map((segment) => (
                <li key={segment.segmentId}>{segment.text}</li>
              ))}
            </ol>
            <button
              className="rounded-xl bg-emerald-700 px-4 py-2 text-white disabled:opacity-50"
              onClick={playWithBrowserTts}
              type="button"
              disabled={!hasSpeechSupport}
            >
              {hasSpeechSupport
                ? "Play with Browser TTS"
                : "Browser speech synthesis unavailable"}
            </button>
          </div>
        )}
      </section>
    </main>
  );
}
