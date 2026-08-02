# OverTheWire: Natas Level 21 -> Level 22 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to authenticate as an administrator on the main application site and retrieve the password for Natas Level 22. 

Upon analysis, the main site provides no visible vector for direct parameter injection to alter session states. However, it references a co-located companion site termed the "Experimenter" website (`http://overthewire.org`).

### The Core Vulnerability: Cross-Application Session Contamination (Shared Storage Session Poisoning)
The architecture of this challenge exhibits two critical architectural and logical flaws:
1. **Shared Session Storage (Co-location)**: Because both applications are hosted on the same underlying physical server, they share the identical backend directory for session state persistence (typically `/var/lib/php/sessions/`). A cryptographic cookie tracking token (`PHPSESSID`) generated on one site points directly to the exact same physical text storage file on the other.
2. **Unsanitized Variable Overwrite (`foreach` Injection)**: The companion Experimenter application features an exceptionally weak implementation for form submission processing:
```php
if(array_key_exists("submit", $_REQUEST)) {
    foreach ($_REQUEST as $key => $val) {
        $_SESSION[$key] = $val;
    }
}
```
The application blindly trusts user input by utilizing a global `foreach` loop [🔍](https://php.net). It maps every arbitrary query parameter or POST pair directly into the `$_SESSION` superglobal array without validation against an allowed blocklist.

---

## 2. Solution Strategy & Exploitation

### Target Authentication Condition:
To harvest the flag, the target main application environment requires the existence of a specific privileged flag within the active session file:
```php
if($_SESSION["admin"] == 1)
```

### Mechanics of the `&` Separator in `foreach` Loop:
Unlike the previous level where we had to manually disrupt the physical storage structure via an explicit newline character (`%0A`), this level leverages native URL parsing. 

In a standard web query context, the ampersand (`&`) character instructs the server's HTTP parser to split the incoming buffer into discrete independent items. By crafting a URL with multiple query parameters (`?submit=1&admin=1`), the server's loose `foreach` wrapper loops exactly twice, automatically generating separate sequential storage rows inside the active session context file:
```text
submit 1
admin 1
```

### Execution Steps (Bypassing Scripts via F12 Cookie Hijacking):

#### Step 1: Session Poisoning on the Companion Site
1. Navigate directly to the experimental subdomain interface:
   `http://overthewire.org`
2. Leverage the query parameter field directly to pass the trigger check and inject the target variable:
   `http://overthewire.orgindex.php?submit=1&admin=1`
3. Hit Enter. The loose backend code instantly writes `admin 1` into the server-side text block map corresponding to your current tracker.
4. Open the Browser Developer Tools (**F12**) → Navigate to `Application` (or `Storage`) → `Cookies`. Locate and copy the current value of the `PHPSESSID` string asset token.

#### Step 2: Privilege Cross-Replay on the Main Site
1. Pivot back to the primary target context domain:
   `http://overthewire.org`
2. Fire up Developer Tools (**F12**) → `Application` → `Cookies`.
3. Locate the native `PHPSESSID` row for the main domain, double-click its data parameter field, and **paste** the exact token identifier string copied from Step 1.
4. Refresh the main webpage (**F5**).

Because the structural token pointer is identical, the main application invokes `session_start()`, reads the file populated by the companion side, maps `$_SESSION["admin"]` as `1`, and grants immediate administration access clearance.

---

## 3. Flag / Final Result
* **Natas Level 22 Password**: `964laB0r7TuDqJj5b3HFtwsQoc0GhjBF`
