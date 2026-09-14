# Natural Language Processing

[← Back to Artificial Intelligence](../../README.md#artificial-intelligence)

**Textbook:** Speech and Language Processing (Jurafsky and Martin)  
**Knowledge points:** 8

> **Turn your own idea into an animation:** [Create with Leadde →](https://leadde.ai/animation)

---

<a id="c27-a001"></a>
## Text Tokenization

`C27-A001` · **▶ Play video below**

https://github.com/user-attachments/assets/2d1b74c4-2d30-4877-ba34-40408685a0e9

> **Make this concept move:** [Create an animation with Leadde →](https://leadde.ai/animation)

### Prompt

```text
Create an animation: Show continuous text being split by vocabulary rules and converted into a processable token sequence.
Requirement: All explanatory text must be in English, and the video must have no audio.
Requirement: Strict typography requirements:
- Render every complete title, label, phrase, or sentence as one native Text(...) object so every character shares one baseline.
- Never rebuild a line from separately positioned word or letter objects, and never align words by their individual bounding boxes.
- Create Arial text at a base font_size of 64, then uniformly scale the complete Text object to its final visual size; do not render explanatory text directly at a tiny font size.
- Preserve ordinary spaces inside the same Text object, set disable_ligatures=True, and do not add manual tracking, special-width spaces, or per-character offsets.
Colors: Background `#F9E7E7`, English text `#5F271C`, primary visual (Text Tokenization) `#1EB81F`, supporting elements `#1816DF`.

Global rendering requirements:
- Never place plain English words, sentences, titles, or explanatory prose in MathTex, Tex, or inline LaTeX math mode. Use the native Text(...) component for all explanatory text and titles.
- If an English word is unavoidable inside a mathematical expression, explicitly wrap every word with \text{...}; never leave a word bare in algebra mode.
- Animate text at whole-word or whole-line granularity. Never split text into individually spaced letters or animate isolated letter spans.
- Do not use text-align: justify or the SVG textLength or lengthAdjust attributes.
- Use the final conclusion display as the video's opening poster frame; do not begin on an empty background.
```

[Back to course top](#natural-language-processing)

---

<a id="c27-a002"></a>
## N-Gram Language Model

`C27-A002` · **▶ Play video below**

https://github.com/user-attachments/assets/57e5c8cc-e980-427c-ba3f-20cf17f3e4d0

> **Make this concept move:** [Create an animation with Leadde →](https://leadde.ai/animation)

### Prompt

```text
Create an animation: Show the model using counts from a fixed number of preceding words to estimate the conditional probability of the next word.
Requirement: All explanatory text must be in English, and the video must have no audio.
Requirement: Strict typography requirements:
- Render every complete title, label, phrase, or sentence as one native Text(...) object so every character shares one baseline.
- Never rebuild a line from separately positioned word or letter objects, and never align words by their individual bounding boxes.
- Create Arial text at a base font_size of 64, then uniformly scale the complete Text object to its final visual size; do not render explanatory text directly at a tiny font size.
- Preserve ordinary spaces inside the same Text object, set disable_ligatures=True, and do not add manual tracking, special-width spaces, or per-character offsets.
Colors: Background `#F9E7E7`, English text `#5F271C`, primary visual (N-Gram Language Model) `#1EB81F`, supporting elements `#1816DF`.

Global rendering requirements:
- Never place plain English words, sentences, titles, or explanatory prose in MathTex, Tex, or inline LaTeX math mode. Use the native Text(...) component for all explanatory text and titles.
- If an English word is unavoidable inside a mathematical expression, explicitly wrap every word with \text{...}; never leave a word bare in algebra mode.
- Animate text at whole-word or whole-line granularity. Never split text into individually spaced letters or animate isolated letter spans.
- Do not use text-align: justify or the SVG textLength or lengthAdjust attributes.
- Use the final conclusion display as the video's opening poster frame; do not begin on an empty background.
```

[Back to course top](#natural-language-processing)

---

<a id="c27-a003"></a>
## Word Embeddings

`C27-A003` · **▶ Play video below**

https://github.com/user-attachments/assets/70fe17dc-6db9-4432-af49-22e554aab490

> **Make this concept move:** [Create an animation with Leadde →](https://leadde.ai/animation)

### Prompt

```text
Create an animation: Show discrete words mapping into a continuous vector space where semantically similar words move closer together.
Requirement: All explanatory text must be in English, and the video must have no audio.
Requirement: Strict typography requirements:
- Render every complete title, label, phrase, or sentence as one native Text(...) object so every character shares one baseline.
- Never rebuild a line from separately positioned word or letter objects, and never align words by their individual bounding boxes.
- Create Arial text at a base font_size of 64, then uniformly scale the complete Text object to its final visual size; do not render explanatory text directly at a tiny font size.
- Preserve ordinary spaces inside the same Text object, set disable_ligatures=True, and do not add manual tracking, special-width spaces, or per-character offsets.
Colors: Background `#F9E7E7`, English text `#5F271C`, primary visual (Word Embeddings) `#1EB81F`, supporting elements `#1816DF`.

Global rendering requirements:
- Never place plain English words, sentences, titles, or explanatory prose in MathTex, Tex, or inline LaTeX math mode. Use the native Text(...) component for all explanatory text and titles.
- If an English word is unavoidable inside a mathematical expression, explicitly wrap every word with \text{...}; never leave a word bare in algebra mode.
- Animate text at whole-word or whole-line granularity. Never split text into individually spaced letters or animate isolated letter spans.
- Do not use text-align: justify or the SVG textLength or lengthAdjust attributes.
- Use the final conclusion display as the video's opening poster frame; do not begin on an empty background.
```

[Back to course top](#natural-language-processing)

---

<a id="c27-a004"></a>
## Positional Encoding

`C27-A004` · **▶ Play video below**

https://github.com/user-attachments/assets/b097dcec-9352-4243-b8d9-b4e41b63bfd0

> **Make this concept move:** [Create an animation with Leadde →](https://leadde.ai/animation)

### Prompt

```text
Create an animation: Show position information being injected into word vectors so the model can distinguish the order of identical words in a sequence.
Requirement: All explanatory text must be in English, and the video must have no audio.
Requirement: Strict typography requirements:
- Render every complete title, label, phrase, or sentence as one native Text(...) object so every character shares one baseline.
- Never rebuild a line from separately positioned word or letter objects, and never align words by their individual bounding boxes.
- Create Arial text at a base font_size of 64, then uniformly scale the complete Text object to its final visual size; do not render explanatory text directly at a tiny font size.
- Preserve ordinary spaces inside the same Text object, set disable_ligatures=True, and do not add manual tracking, special-width spaces, or per-character offsets.
Colors: Background `#F9E7E7`, English text `#5F271C`, primary visual (Positional Encoding) `#1EB81F`, supporting elements `#1816DF`.

Global rendering requirements:
- Never place plain English words, sentences, titles, or explanatory prose in MathTex, Tex, or inline LaTeX math mode. Use the native Text(...) component for all explanatory text and titles.
- If an English word is unavoidable inside a mathematical expression, explicitly wrap every word with \text{...}; never leave a word bare in algebra mode.
- Animate text at whole-word or whole-line granularity. Never split text into individually spaced letters or animate isolated letter spans.
- Do not use text-align: justify or the SVG textLength or lengthAdjust attributes.
- Use the final conclusion display as the video's opening poster frame; do not begin on an empty background.
```

[Back to course top](#natural-language-processing)

---

<a id="c27-a005"></a>
## Self-Attention

`C27-A005` · **▶ Play video below**

https://github.com/user-attachments/assets/64a60450-916d-4839-8339-f984811adb50

> **Make this concept move:** [Create an animation with Leadde →](https://leadde.ai/animation)

### Prompt

```text
Create an animation: Show every word attending to other words and aggregating contextual information into a new representation.
Requirement: All explanatory text must be in English, and the video must have no audio.
Requirement: Strict typography requirements:
- Render every complete title, label, phrase, or sentence as one native Text(...) object so every character shares one baseline.
- Never rebuild a line from separately positioned word or letter objects, and never align words by their individual bounding boxes.
- Create Arial text at a base font_size of 64, then uniformly scale the complete Text object to its final visual size; do not render explanatory text directly at a tiny font size.
- Preserve ordinary spaces inside the same Text object, set disable_ligatures=True, and do not add manual tracking, special-width spaces, or per-character offsets.
Colors: Background `#F9E7E7`, English text `#5F271C`, primary visual (Self-Attention) `#1EB81F`, supporting elements `#1816DF`.

Global rendering requirements:
- Never place plain English words, sentences, titles, or explanatory prose in MathTex, Tex, or inline LaTeX math mode. Use the native Text(...) component for all explanatory text and titles.
- If an English word is unavoidable inside a mathematical expression, explicitly wrap every word with \text{...}; never leave a word bare in algebra mode.
- Animate text at whole-word or whole-line granularity. Never split text into individually spaced letters or animate isolated letter spans.
- Do not use text-align: justify or the SVG textLength or lengthAdjust attributes.
- Use the final conclusion display as the video's opening poster frame; do not begin on an empty background.
```

[Back to course top](#natural-language-processing)

---

<a id="c27-a006"></a>
## Encoder-Decoder Architecture

`C27-A006` · **▶ Play video below**

https://github.com/user-attachments/assets/774f7dfb-871d-4335-a040-ad15107fde17

> **Make this concept move:** [Create an animation with Leadde →](https://leadde.ai/animation)

### Prompt

```text
Create an animation: Show an encoder compressing input information and a decoder using it to generate an output sequence step by step.
Requirement: All explanatory text must be in English, and the video must have no audio.
Requirement: Strict typography requirements:
- Render every complete title, label, phrase, or sentence as one native Text(...) object so every character shares one baseline.
- Never rebuild a line from separately positioned word or letter objects, and never align words by their individual bounding boxes.
- Create Arial text at a base font_size of 64, then uniformly scale the complete Text object to its final visual size; do not render explanatory text directly at a tiny font size.
- Preserve ordinary spaces inside the same Text object, set disable_ligatures=True, and do not add manual tracking, special-width spaces, or per-character offsets.
Colors: Background `#F9E7E7`, English text `#5F271C`, primary visual (Encoder-Decoder Architecture) `#1EB81F`, supporting elements `#1816DF`.

Global rendering requirements:
- Never place plain English words, sentences, titles, or explanatory prose in MathTex, Tex, or inline LaTeX math mode. Use the native Text(...) component for all explanatory text and titles.
- If an English word is unavoidable inside a mathematical expression, explicitly wrap every word with \text{...}; never leave a word bare in algebra mode.
- Animate text at whole-word or whole-line granularity. Never split text into individually spaced letters or animate isolated letter spans.
- Do not use text-align: justify or the SVG textLength or lengthAdjust attributes.
- Use the final conclusion display as the video's opening poster frame; do not begin on an empty background.
```

[Back to course top](#natural-language-processing)

---

<a id="c27-a007"></a>
## Beam Search

`C27-A007` · **▶ Play video below**

https://github.com/user-attachments/assets/08cf684f-3ede-47c9-90df-b8b8eabc0c0e

> **Make this concept move:** [Create an animation with Leadde →](https://leadde.ai/animation)

### Prompt

```text
Create an animation: Show decoding retaining several high-probability candidates at once and expanding them step by step to choose the best sequence.
Requirement: All explanatory text must be in English, and the video must have no audio.
Requirement: Strict typography requirements:
- Render every complete title, label, phrase, or sentence as one native Text(...) object so every character shares one baseline.
- Never rebuild a line from separately positioned word or letter objects, and never align words by their individual bounding boxes.
- Create Arial text at a base font_size of 64, then uniformly scale the complete Text object to its final visual size; do not render explanatory text directly at a tiny font size.
- Preserve ordinary spaces inside the same Text object, set disable_ligatures=True, and do not add manual tracking, special-width spaces, or per-character offsets.
Colors: Background `#F9E7E7`, English text `#5F271C`, primary visual (Beam Search) `#1EB81F`, supporting elements `#1816DF`.

Global rendering requirements:
- Never place plain English words, sentences, titles, or explanatory prose in MathTex, Tex, or inline LaTeX math mode. Use the native Text(...) component for all explanatory text and titles.
- If an English word is unavoidable inside a mathematical expression, explicitly wrap every word with \text{...}; never leave a word bare in algebra mode.
- Animate text at whole-word or whole-line granularity. Never split text into individually spaced letters or animate isolated letter spans.
- Do not use text-align: justify or the SVG textLength or lengthAdjust attributes.
- Use the final conclusion display as the video's opening poster frame; do not begin on an empty background.
```

[Back to course top](#natural-language-processing)

---

<a id="c27-a008"></a>
## Retrieval-Augmented Generation

`C27-A008` · **▶ Play video below**

https://github.com/user-attachments/assets/e0ce9b34-c607-4bf8-b5de-4b31e026f024

> **Make this concept move:** [Create an animation with Leadde →](https://leadde.ai/animation)

### Prompt

```text
Create an animation: Show a system retrieving relevant material for a query and feeding that evidence into a generative model to form an answer.
Requirement: All explanatory text must be in English, and the video must have no audio.
Requirement: Strict typography requirements:
- Render every complete title, label, phrase, or sentence as one native Text(...) object so every character shares one baseline.
- Never rebuild a line from separately positioned word or letter objects, and never align words by their individual bounding boxes.
- Create Arial text at a base font_size of 64, then uniformly scale the complete Text object to its final visual size; do not render explanatory text directly at a tiny font size.
- Preserve ordinary spaces inside the same Text object, set disable_ligatures=True, and do not add manual tracking, special-width spaces, or per-character offsets.
Colors: Background `#F9E7E7`, English text `#5F271C`, primary visual (Retrieval-Augmented Generation) `#1EB81F`, supporting elements `#1816DF`.

Global rendering requirements:
- Never place plain English words, sentences, titles, or explanatory prose in MathTex, Tex, or inline LaTeX math mode. Use the native Text(...) component for all explanatory text and titles.
- If an English word is unavoidable inside a mathematical expression, explicitly wrap every word with \text{...}; never leave a word bare in algebra mode.
- Animate text at whole-word or whole-line granularity. Never split text into individually spaced letters or animate isolated letter spans.
- Do not use text-align: justify or the SVG textLength or lengthAdjust attributes.
- Use the final conclusion display as the video's opening poster frame; do not begin on an empty background.
```

[Back to course top](#natural-language-processing)

---
