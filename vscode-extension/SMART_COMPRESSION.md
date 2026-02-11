# Smart Context-Aware Compression Plan

## Overview
Use a lightweight language model to intelligently detect which phrases can be compressed/removed based on context understanding, rather than hard-coded rules.

## Model Selection

### Phase 1: Quick Implementation (BERT-tiny)
**Model:** `prajjwal1/bert-tiny` or `huawei-noah/TinyBERT_General_4L_312D`
- **Size:** 16-60MB
- **Speed:** 10-30ms on laptop, 30-80ms on phone
- **Task:** Binary classification (keep vs remove/abbreviate)
- **Integration:** Use transformers.js (JavaScript) or ONNX Runtime
- **Timeline:** 2-3 days

**Advantages:**
- Fastest to implement
- Runs entirely in JavaScript/WebAssembly
- No Python dependency
- Can bundle with extension

**Implementation:**
```javascript
import { pipeline } from '@xenova/transformers';

const classifier = await pipeline(
  'text-classification',
  'Xenova/bert-tiny-finetuned-compression'
);

const result = await classifier("please make a picture for me");
// Output: { label: 'FILLER', score: 0.95 }
```

### Phase 2: Advanced (SmolLM-135M)
**Model:** `HuggingFaceTB/SmolLM-135M-Instruct`
- **Size:** 135MB (quantized to ~80MB)
- **Speed:** 20-50ms on laptop
- **Task:** Instruction following with context understanding
- **Integration:** llama.cpp via node bindings
- **Timeline:** 1 week

**Advantages:**
- Better context understanding
- Can provide reasoning
- More flexible

**Implementation:**
```javascript
const llama = await loadModel('SmolLM-135M-Q4');

const prompt = `Analyze this text and mark filler words:
"please make a picture for me in high quality"

Filler words (can remove):`;

const result = await llama.generate({
  prompt,
  max_tokens: 50,
  temperature: 0.1
});
// Output: "please, for me"
```

## Training Data Format

Create a dataset of 10,000-50,000 examples:

```json
[
  {
    "text": "please make a picture for me",
    "filler_phrases": ["please", "for me"],
    "important_phrases": ["make a picture"],
    "context": "image_generation"
  },
  {
    "text": "this is for my project deadline",
    "filler_phrases": [],
    "important_phrases": ["for my project deadline"],
    "context": "business"
  }
]
```

## Integration Architecture

### Current (Rule-based):
```
User Input → Hard-coded Rules → Compressed Output
```

### Smart Compression:
```
User Input → Context Model → Identify Filler → Compress → Output
            ↓
         [Cache results for speed]
```

## Performance Targets

| Model | Cold Start | Warm (cached) | Accuracy Goal |
|-------|-----------|---------------|---------------|
| BERT-tiny | 100-200ms | 20-40ms | 85%+ |
| SmolLM-135M | 200-400ms | 30-80ms | 92%+ |

## Fallback Strategy

1. **First run:** Use lightweight model to analyze
2. **Cache results:** Store common phrase decisions
3. **Fallback:** If model unavailable, use hard-coded rules
4. **Hybrid mode:** Model + rules (rules as safety net)

## Development Phases

### Phase 1: Proof of Concept (3-5 days)
- [ ] Choose BERT-tiny or similar
- [ ] Set up transformers.js in extension
- [ ] Test with 100 sample prompts
- [ ] Measure performance

### Phase 2: Training (1 week)
- [ ] Create training dataset (5k examples)
- [ ] Fine-tune BERT-tiny for compression task
- [ ] Evaluate accuracy vs rules
- [ ] Optimize for speed

### Phase 3: Integration (3-5 days)
- [ ] Bundle model with extension
- [ ] Add caching layer
- [ ] Create hybrid rule + model system
- [ ] Add user preference toggle

### Phase 4: Polish (2-3 days)
- [ ] Add progress indicators
- [ ] Handle offline mode
- [ ] Add model download on first use
- [ ] Documentation

## Total Timeline: 2-3 weeks for production-ready smart compression

## Expected Improvements

- **Accuracy:** 85-95% (vs 60-70% with pure rules)
- **Adaptability:** Works with new domains without new rules
- **User experience:** "Just works" without manual tuning
- **Token savings:** 50-80% (vs current 30-50%)

## Resource Requirements

### Development:
- GPU for training: 4GB VRAM (can use free Colab)
- Development time: 2-3 weeks total

### End-user (bundled with extension):
- Disk space: 80-150MB (model)
- RAM: 200-400MB during compression
- One-time download: ~100MB on first use
- CPU: Works on any modern laptop/phone
