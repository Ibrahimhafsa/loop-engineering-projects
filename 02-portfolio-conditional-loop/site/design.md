# The design decision
A tall-hero portfolio with project cards as discrete, equal-weight units showing problem-approach-solution, using teal accents on warm neutrals and a responsive type-space scale that grows with visual importance.

## Why this person
Hafsa builds AI systems that respond to intent—Smart AI TaskFlow (chatbot plus task management), Physical AI (interactive humanoid book), workflow automation. Her material is shaped around **input-process-output flows**: a problem arrives, her technical stack processes it, a working solution ships. The page structure mirrors this thinking: each project card is a complete pipeline, visibly discrete and equally important.

## How the page carries it out
- The hero anchors the page with Hafsa's practice—building AI systems that respond. It is the largest visual element, establishing what the page is about before the reader scrolls.
- Projects are arranged as a grid of cards, each card showing the three stages (problem statement, technical approach, working solution) with equal visual weight. No sidebar dates or roles; the flow is horizontal and complete.
- At 390px, cards stack to a single column and remain readable; the hero shrinks but keeps its proportion. Type and space scale down in measured steps, not arbitrary values.

## Tokens
:root {
  --bg: #f8f6f1; --fg: #2a2a2a; --accent: #006666;
  /* --fg on --bg = 12.7:1 ✓ | --accent on --bg = 6.33:1 ✓ */
  
  --text-xs: 0.75rem;
  --text-sm: 0.9rem;
  --text-base: 1.1rem;
  --text-lg: 1.5rem;
  --text-xl: clamp(2rem, 5vw, 3rem);
  --text-2xl: clamp(2.5rem, 8vw, 4.5rem);
  
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 1rem;
  --space-4: 1.5rem;
  --space-5: 2.5rem;
  --space-6: 4rem;
  
  --measure: 47ch;
}
