# Image Generation System - Full Specification

## Overview

Integrate AI-powered image generation (Nano Banana Pro / Gemini 3 Pro Image) into the storyboard generator, adding smart visual content to all 12 storyboard types across both PPTX and DOCX engines.

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| DOCX image handling | Embedded inside documents | Designers see images inline while reading |
| DOCX image placement | Inside content table cells | Integrated alongside Arabic text |
| Generation timing | During storyboard creation | Seamless, one-step process |
| Art style system | Fully custom per project | Each client defines style in config.json |
| PPTX image density | 8-12 per lecture | Most slides get images, agent decides which |
| DOCX image density | Smart per type | Video: 6-8, Activity: 3-5, Test: 1-2, Summary: 2-3 |
| Resolution | 2K (balanced) | Sharp for screens + Storyline, cost-effective |
| Image caching | Yes, by topic | Reuse across storyboards for consistency |
| Script approach | Copy and modify | Copy generate_image.py, add our customizations |
| API key | Embedded (from skill) | Simplifies UX, no env setup needed |
| Error handling | Stop and ask user | Halt and ask whether to retry, skip, or provide own |

---

## Architecture

### Component Overview

```
Project config.json → visualDirection (style, colors, rules)
                          ↓
Storyboard Agent → builds content + calls image generator
                          ↓
engine/image_gen.py → wraps Nano Banana API
  - Applies visual direction from config
  - Enforces cultural rules
  - Manages caching (topic-based)
  - Handles aspect ratio per slide/cell type
                          ↓
Generated images saved to: output/[PROJECT]/U[XX]/images/
                          ↓
Engine builders (PPTX/DOCX) → embed images into documents
```

### File Changes

| File | Action | Description |
|------|--------|-------------|
| `engine/image_gen.py` | **NEW** | Image generation module (copy+modify from nano-banana-pro) |
| `engine/pptx_engine.py` | **MODIFY** | Already has image support, enhance smart placement |
| `engine/docx_engine.py` | **MODIFY** | Add image embedding in content cells for all builders |
| `projects/*/config.json` | **MODIFY** | Expand visualDirection schema |
| `.claude/skills/storyboard-templates/SKILL.md` | **MODIFY** | Document image generation API |
| `.claude/skills/storyboard-templates/references/image-gen.md` | **NEW** | Detailed image gen reference |
| `.claude/agents/storyboard-*.md` | **MODIFY** | Add image generation instructions to all agents |

---

## Visual Direction System (config.json)

### Schema

```json
{
  "visualDirection": {
    "style": "vector-flat",
    "description": "Clean geometric vector illustrations for educational context",
    "colorPalette": ["#2D588C", "#156082", "#009688", "#FF9800"],
    "promptPrefix": "",
    "promptSuffix": "flat vector illustration, clean geometric shapes, educational context",
    "negativeRules": [
      "no human faces or facial features",
      "no female characters",
      "no Arabic text or writing inside images",
      "no photorealistic style",
      "no gradients or shadows in illustrations"
    ],
    "defaultResolution": "2K",
    "defaultContentType": "illustration",
    "aspectRatios": {
      "pptx_content": "16:9",
      "pptx_card": "1:1",
      "pptx_section": "16:9",
      "pptx_two_column": "3:2",
      "pptx_closing": "16:9",
      "pptx_quiz": "1:1",
      "docx_hero": "16:9",
      "docx_scene": "16:9",
      "docx_step": "1:1",
      "docx_inline": "1:1"
    },
    "imageDensity": {
      "interactive_lecture": "most",
      "pdf_lecture": "most",
      "video": "per_scene",
      "activity": "per_step",
      "discussion": "hero_only",
      "assignment": "hero_only",
      "test": "minimal",
      "summary": "moderate",
      "infographic": "moderate",
      "objectives": "hero_only"
    }
  }
}
```

### Style Examples

**vector-flat** (current NJR01):
```
promptSuffix: "flat vector illustration, clean geometric shapes, educational context, muted professional colors"
negativeRules: ["no faces", "no females", "no Arabic text", "no photorealistic", "no gradients"]
```

**editorial-hand-drawn** (Anthropic-inspired):
```
promptSuffix: "hand-drawn editorial illustration, Saul Steinberg style, imperfect linework, risograph aesthetic"
negativeRules: ["no gradients", "no 3D", "no glossy surfaces", "no smooth vectors"]
```

**academic-classic** (textbook style):
```
promptSuffix: "clean academic illustration, textbook style, labeled diagrams, educational"
negativeRules: ["no cartoonish style", "no neon colors"]
```

---

## Image Generation Module (engine/image_gen.py)

### Core Functions

```python
def generate_storyboard_image(
    prompt: str,
    project_code: str,
    unit_number: int,
    image_type: str,      # "content", "scene", "step", "hero", "card", etc.
    topic_key: str = None, # For caching: "design_thinking", "digital_mindset"
    output_name: str = None,
    aspect_ratio: str = None,  # Override, else from config
    resolution: str = None,    # Override, else from config
) -> dict:
    """
    Generate an image with project visual direction applied.

    1. Load visual direction from project config
    2. Check cache (by topic_key)
    3. Build prompt: prefix + user prompt + suffix + negative rules
    4. Call Nano Banana API
    5. Save to output/[PROJECT]/U[XX]/images/
    6. Return {"success": bool, "path": str, "cached": bool}
    """

def get_cached_image(project_code, unit_number, topic_key) -> str or None:
    """Check if image already exists for this topic."""

def build_prompt(raw_prompt, visual_direction) -> str:
    """Apply visual direction rules to a raw prompt."""
```

### Caching Strategy

```
output/NJR01/U02/images/
  ├── design_thinking.png          # Reused by lecture + activity
  ├── digital_mindset.png          # Reused by multiple slides
  ├── entrepreneurial_mindset.png  # Topic-specific
  ├── scene_01_intro.png           # Video-specific (not cached)
  └── ...
```

- **Cache key**: `{project_code}_{unit}_{topic_key}` (slugified)
- **Cache hit**: Return existing path immediately
- **Cache miss**: Generate, save, return path
- Video scene images are NOT cached (unique per scene)

### Cultural Rules Enforcement

Applied automatically via prompt construction:

```python
def build_prompt(raw_prompt, visual_direction):
    parts = []
    if visual_direction.get("promptPrefix"):
        parts.append(visual_direction["promptPrefix"])
    parts.append(raw_prompt)
    parts.append(visual_direction["promptSuffix"])

    # Add negative rules as explicit instructions
    for rule in visual_direction["negativeRules"]:
        parts.append(f"IMPORTANT: {rule}")

    return ". ".join(parts)
```

---

## PPTX Engine Modifications

### Current State (Already Implemented)
- `_get_image_dimensions()` and `_add_image()` helper methods
- 6 slide types support `image_path` parameter
- Aspect ratio preservation, graceful fallback

### Enhancements Needed

1. **Auto-generate during slide creation**: When agent calls `content_slide()`, automatically generate image if `image_prompt` is provided (instead of requiring pre-generated `image_path`)
2. **Smart image sizing per slide type**: Use aspect ratios from config
3. **Support both modes**: `image_path` (pre-generated) AND `image_prompt` (generate on-the-fly)

### New Parameter Pattern

```python
# Current (keep backward-compatible)
builder.content_slide(title, bullets, image_path="/path/to/img.png")

# New addition
builder.content_slide(title, bullets, image_prompt="digital innovation concept")
# → Auto-generates using visual direction, saves, embeds
```

---

## DOCX Engine Modifications

### Current State
- No image support in any builder
- Content is in tables with RTL text

### New: Image Embedding in Content Cells

For each DOCX builder, add image support:

| Builder | Image Placement | Images Per Doc |
|---------|----------------|----------------|
| VideoBuilder | One per scene row (6-8 total) | Per scene |
| ActivityBuilder | One per step/interaction (3-5) | Per step |
| TestBuilder | Optional per question (1-2) | Minimal |
| DiscussionBuilder | Hero image at top (1) | Hero only |
| AssignmentBuilder | Hero image at top (1) | Hero only |
| SummaryBuilder | Topic illustrations (2-3) | Moderate |
| InfographicBuilder | Section illustrations (2-3) | Moderate |
| ObjectivesBuilder | Hero image at top (1) | Hero only |

### Implementation Approach

```python
# In docx_engine.py - each builder gets image support

# Example: ActivityBuilder
def build(self, data):
    # ... existing header code ...

    for step in data["steps"]:
        # Add text content (existing)
        self._add_step_row(step["title"], step["description"])

        # NEW: Add image if provided
        if step.get("image_path"):
            self._add_image_to_cell(cell, step["image_path"],
                                     width=Cm(8), height=Cm(5))
```

### python-docx Image in Table Cell

```python
from docx.shared import Cm

def _add_image_to_cell(self, cell, image_path, width=None, height=None):
    """Add image to a table cell, maintaining RTL layout."""
    paragraph = cell.paragraphs[0]  # or add_paragraph()
    run = paragraph.add_run()

    # Add image with size constraints
    if width and height:
        run.add_picture(image_path, width=width, height=height)
    elif width:
        run.add_picture(image_path, width=width)
    else:
        run.add_picture(image_path)

    # Center the image
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
```

---

## Image Density Per Storyboard Type

### PPTX (Interactive Lecture / PDF Lecture)

| Slide Type | Gets Image? | Aspect Ratio | Notes |
|------------|-------------|--------------|-------|
| Title slide | No | - | Has branding already |
| Section divider | Yes | 16:9 | Topic-related illustration |
| Content slide | Yes (most) | 16:9 | Agent decides per slide |
| Cards slide | Yes (some) | 1:1 | Small per-card thumbnails |
| Two-column | Yes | 3:2 | In one column |
| Quiz/interaction | Optional | 1:1 | If question benefits from visual |
| Closing slide | Yes | 16:9 | Decorative/summary |

**Total: ~8-12 images per lecture**

### DOCX (All Types)

| Storyboard Type | Images | Placement |
|-----------------|--------|-----------|
| Motion Video | 6-8 | One per scene in scene row |
| Interactive Activity | 3-5 | One per interaction step |
| Pre/Post Test | 1-2 | Hero + optional per question |
| Discussion | 1 | Hero at top |
| Assignment | 1 | Hero at top |
| Summary | 2-3 | Per topic section |
| Infographic | 2-3 | Per learning milestone |
| Objectives | 1 | Hero at top |

---

## Error Handling

```python
def generate_storyboard_image(...):
    try:
        result = generate_image(prompt=final_prompt, ...)
        if result["success"]:
            return {"success": True, "path": result["path"]}
        else:
            # API returned error
            return {
                "success": False,
                "error": result["error"],
                "action": "ask_user"  # Signal to agent to stop and ask
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "action": "ask_user"
        }
```

**Agent behavior on error**: Stop generation, show the error to user, ask:
1. Retry with modified prompt?
2. Skip this image?
3. Provide your own image path?

---

## Implementation Phases

### Phase 1: Core Image Generation Module
- Copy and modify `generate_image.py` → `engine/image_gen.py`
- Add visual direction integration
- Add caching system
- Add cultural rules enforcement
- Test with simple prompts

### Phase 2: PPTX Engine Enhancement
- Add `image_prompt` parameter to all slide methods
- Auto-generate images when prompt provided
- Smart sizing per slide type
- Test with Interactive Lecture

### Phase 3: DOCX Engine Enhancement
- Add `_add_image_to_cell()` helper method
- Add image support to all 8 builders
- Smart placement per builder type
- Test with each document type

### Phase 4: Skill & Agent Updates
- Add image generation reference to skill
- Update all 10 agent prompts with image instructions
- Document image density guidelines per type
- Update config.json schema documentation

### Phase 5: Testing & Polish
- End-to-end test: generate a full unit with images
- Verify caching works across storyboards
- Check RTL compatibility with embedded images
- Validate Storyline 360 import with images

---

## Dependencies

- `google-genai` or `requests` (for API calls)
- `Pillow` (already used for image dimensions)
- Gemini API key (embedded)

## API Cost Estimate

Per unit (12 storyboards):
- Interactive Lecture: ~10 images = ~$0.20
- PDF Lecture: ~10 images = ~$0.20
- Video: ~7 images = ~$0.14
- Activities (x3): ~12 images = ~$0.24
- Other (discussion, assignment, tests, summary, etc.): ~8 images = ~$0.16
- **Total per unit: ~47 images = ~$0.94**

With caching (reusing ~30% of images): **~$0.66 per unit**
