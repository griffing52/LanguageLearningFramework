# Frontend Architecture

Modern React TypeScript frontend with clean component and service architecture.

## Architecture Layers

```
┌─────────────────────────────────────┐
│      React Components               │  UI rendering
│      (components/*/)                │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Custom Hooks                   │  State management
│      (hooks/*.ts)                   │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Services                       │  Business logic
│      (services/*.ts)                │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      API Clients                    │  HTTP communication
│      (api/*.ts)                     │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│      Backend API                    │
│      (http://127.0.0.1:5000/api)    │
└─────────────────────────────────────┘
```

## Module Responsibilities

### Components (`src/components/`)

Reusable React components organized by feature:

#### Study (`Study/`)

Interactive study interface - similar to Mango Learning/Pimsleur.

| Component | Purpose |
|-----------|---------|
| `StudyCard.tsx` | Main study container, orchestrates sub-components |
| `WordDisplay.tsx` | Shows word/phrase + translation in large format |
| `AudioPlayer.tsx` | Play audio pronunciation with visual feedback |
| `FeedbackUI.tsx` | Collect user response: correct/incorrect + confidence |
| `ProgressIndicator.tsx` | Visual lesson progress bar |

#### Vocabulary (`Vocabulary/`)

Word and phrase browsing.

| Component | Purpose |
|-----------|---------|
| `WordList.tsx` | Paginated, searchable list of words |

#### Progress (`Progress/`)

Learning analytics dashboard.

| Component | Purpose |
|-----------|---------|
| `Dashboard.tsx` | Statistics, milestones, progress charts |

#### Layout (`Layout/`)

Application structure.

| Component | Purpose |
|-----------|---------|
| `Header.tsx` | Navigation, branding, page switching |

### Custom Hooks (`src/hooks/`)

React hooks for state management and side effects.

| Hook | Purpose |
|------|---------|
| `useStudy.ts` | Manage study session state and progression |

**Key Principle**: Encapsulate stateful logic, reusable across components.

### Services (`src/services/`)

Frontend business logic, independent of React.

| Service | Responsibility |
|---------|-----------------|
| `studyService.ts` | Study session management, progression logic |
| `audioService.ts` | Audio playback control and events |

**Key Principle**: Pure JavaScript, no React dependencies, easily testable.

### API Clients (`src/api/`)

HTTP communication layer - single contact point with backend.

| Module | Endpoints |
|--------|-----------|
| `client.ts` | HTTP client wrapper, error handling |
| `vocabulary.ts` | Typed functions for vocabulary endpoints |
| `study.ts` | Typed functions for study endpoints |
| `progress.ts` | Typed functions for progress endpoints |

**Key Principle**: All backend communication goes through here. Easy to mock for testing.

## Component Hierarchy

```
App (src/App.tsx)
├── Header
│   └── Navigation buttons
│
└── Main content (one of):
    ├── Study Section
    │   ├── ProgressIndicator
    │   └── StudyCard
    │       ├── WordDisplay
    │       ├── AudioPlayer
    │       └── FeedbackUI
    │
    ├── Vocabulary Section
    │   └── WordList
    │
    └── Progress Section
        └── Dashboard
```

## Data Flow

### Study Session Flow

```
User clicks "Study"
      ↓
useStudy hook loads lesson
      ↓
studyService.loadLesson()
      ↓
studyApi.getLesson() → HTTP call to /api/study/lesson
      ↓
Backend returns 10 items
      ↓
StudyCard displays current item
      ↓
User provides feedback (correct/confidence/time)
      ↓
FeedbackUI calls studyService.submitFeedback()
      ↓
studyApi.submitFeedback() → HTTP POST to /api/study/feedback
      ↓
Backend updates progress, returns next item
      ↓
StudyCard auto-advances to next item
      ↓
Repeat until lesson complete
```

### Information Hiding

Multiple layers of abstraction:

1. **Components see only:** Props and event callbacks
   - Don't know about HTTP
   - Don't know about services
   - Just render UI

2. **Hooks orchestrate:** Component state and side effects
   - Know about services
   - Know about API clients
   - Coordinate component updates

3. **Services manage:** Business logic
   - Know about API clients
   - Pure functions
   - No React dependencies

4. **API Clients handle:** HTTP communication
   - Request/response transformation
   - Error handling
   - Type safety

## Styling

### CSS Organization

- `globals.css` - Theme, utilities, base styles
- `components.css` - Component-specific styles

### Design System

CSS custom properties (variables) for consistency:

```css
:root {
  --primary-color: #3b82f6;
  --success-color: #10b981;
  --error-color: #ef4444;
  --text-primary: #1f2937;
  --transition: all 0.3s ease;
}
```

### Responsive Design

Mobile-first approach with breakpoints:
- Base styles for mobile
- `@media (max-width: 768px)` for tablets
- Desktop gets larger elements

## State Management

### Global State
Currently none (can add Zustand/Redux/Context if needed).

### Component State
Managed via `useStudy` hook:
- Current study target
- Progress tracking
- Loading states
- Error handling

### Local Component State
Via `useState` for UI-only state:
- Confidence level selection
- Audio playing state
- Search input

## Type Safety

Full TypeScript coverage with:
- Strict mode enabled
- Interfaces for all props
- Typed API responses (Pydantic models from backend)
- No `any` types

Example:
```typescript
interface StudyCardProps {
  target: StudyTarget;
  onFeedback: (correct: boolean, confidence: number, timeSpent: number) => Promise<void>;
  isLoading?: boolean;
}

export const StudyCard: React.FC<StudyCardProps> = ({ ... }) => {
  // ...
}
```

## Performance Optimization

1. **Code Splitting**: Vite automatic splitting per route
2. **CSS Optimization**: Production builds minify
3. **Image Optimization**: Use vector SVG where possible
4. **Bundle Analysis**: `npm run build` shows size breakdown

## Accessibility

- Semantic HTML elements
- ARIA labels where needed
- Keyboard navigation support
- Color contrast compliance
- Focus indicators

## Configuration

### Environment Variables

In `src/config.ts`:
```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL ||
  'http://127.0.0.1:5000/api';
```

Override in `.env`:
```env
VITE_API_URL=http://your-api.com/api
```

### Build Configuration

`vite.config.ts`:
- API proxy for dev (localhost:5000 → /api)
- Path aliases for cleaner imports
- Output optimization for production

## Development Tools

### Commands

```bash
npm run dev         # Start dev server with HMR
npm run build       # Production build
npm run type-check  # TypeScript validation
npm run preview     # Test production build
npm run lint        # Code linting
```

### IDE Setup

Path aliases configured in `tsconfig.json`:
- `@/` → `src/`
- `@components/` → `src/components/`
- `@api/` → `src/api/`
- etc.

Enables clean imports:
```typescript
import { StudyCard } from '@components/Study/StudyCard';
import { studyApi } from '@api/study';
```

## Testing

TODO: Add Jest + React Testing Library

Recommended test structure:
```
__tests__/
├── components/
│   └── StudyCard.test.tsx
├── hooks/
│   └── useStudy.test.ts
├── services/
│   └── studyService.test.ts
└── api/
    └── client.test.ts
```

## Future Enhancements

- [ ] Dark mode theme
- [ ] Offline support (Service Workers)
- [ ] Progressive enhancement
- [ ] Advanced analytics visualization
- [ ] Multi-language support
- [ ] Customizable spaced repetition settings
- [ ] Export/import progress
- [ ] Social features (leaderboards, challenges)
