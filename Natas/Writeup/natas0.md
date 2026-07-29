# OverTheWire: Natas Level 0 -> Level 1 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to find the access password for Natas Level 1. The challenge presents a basic web page with no visible clues on the interface, indicating a potential Information Disclosure vulnerability in the frontend source code.

## 2. Solution Strategy & Exploitation
Since developers sometimes leave debugging information, configurations, or credentials within frontend comments during development, the source code should be inspected.

### Step-by-step Execution:
1. Access the challenge page.
2. **Right-click** anywhere on the page and select **"View page source"** (or use the shortcut `Ctrl + U` / `Cmd + Option + U`).
3. Inspect the HTML structure and look for the commented section at the bottom.

The password was found hardcoded inside an HTML comment block:
```html
<!--The password for natas1 is scfWG6qNEIdzqVyfRwEGXyNUfFZkZeQ7 -->
```

## 3. Flag / Final Result
* **Natas Level 1 Password**: `scfWG6qNEIdzqVyfRwEGXyNUfFZkZeQ7`
