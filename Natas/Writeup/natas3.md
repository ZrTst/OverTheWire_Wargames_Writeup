# OverTheWire: Natas Level 3 -> Level 4 Writeup

## 1. Challenge Background & Analysis
The objective of this level is to retrieve the password for Natas Level 4. In this challenge, there are no direct links or visible asset paths leading to sensitive files in the HTML source. 

However, a hint left by the developer points toward search engine indexing mechanisms, suggesting an **Information Disclosure via Misconfigured Robots Exclusion Protocol**.

## 2. Solution Strategy & Exploitation
Websites use a file named `robots.txt` at their root directory to instruct web crawlers (like Googlebot) which paths should not be indexed or crawled. Attackers frequently check this file because developers often accidentally reveal hidden or sensitive directories inside the `Disallow` directives.

### Step-by-step Execution:
1. Access the challenge page, **right-click**, and select **"View page source"**.
2. Locate a suspicious hint hidden inside an HTML comment block:
   ```html
   <!-- No more information leaks!! Not even Google will find it this time... -->
   ```
3. The keyword "Google" strongly implies the use of spider/crawler restrictions. Therefore, check the standard path for the robots configuration file by navigating to:
   ```text
   http://overthewire.org
   ```
4. The server successfully returns the `robots.txt` file with the following contents:
   ```text
   User-agent: *
   Disallow: /s3cr3t/
   ```
5. Navigate directly to the restricted directory exposed by the configuration file:
   ```text
   http://overthewire.org
   ```
6. Inside the directory listing (or file index), locate and open the credentials file to obtain the cleartext password for the next level:
   ```text
   natas4:JDrPnuZAKyl6MkiqQGFIddrqpvgOASth
   ```

## 3. Flag / Final Result
* **Natas Level 4 Password**: `JDrPnuZAKyl6MkiqQGFIddrqpvgOASth`
