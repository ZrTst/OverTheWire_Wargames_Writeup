# OverTheWire: Natas Level 1 -> Level 2 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to retrieve the password for Natas Level 2. On this page, the developers attempted a client-side restriction by disabling the right-click context menu via JavaScript, preventing users from using the traditional "View page source" method. 

However, this is a classic "Client-Side Security Controls" flaw, as browser native developer tools cannot be blocked by frontend scripts.

## 2. Solution Strategy & Exploitation
To bypass the disabled right-click restriction, we can directly invoke the browser's built-in developer tools to inspect the source files and DOM structure.

### Step-by-step Execution:
1. Access the challenge page.
2. Press **F12** (or `Ctrl + Shift + I` / `Cmd + Option + I`) to open the **Developer Tools**.
3. Navigate to the **Sources** (or Elements/Inspector) tab.
4. Inspect the HTML structure to locate the commented section at the bottom of the source file.

The password was found exposed inside an HTML comment block:
```html
<!--The password for natas2 is vsDOxoXyq3wckCP1ZmTZ71ngIA606odB -->
```

## 3. Flag / Final Result
* **Natas Level 2 Password**: `vsDOxoXyq3wckCP1ZmTZ71ngIA606odB`
