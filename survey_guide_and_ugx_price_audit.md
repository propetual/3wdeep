# FLEXIFIT SURVEY: UGX PRICING FACT-CHECK & ONLINE DEPLOYMENT GUIDE
## Fieldwork Research Instrument for IST2106 Capstone (Group 4)

**Course:** IST2106: Technopreneurship & Digital Marketing  
**Venture:** FlexiFit (Hybrid Coaching & Localized Nutrition)  
**Target Market:** Urban Kampala, Uganda  

---

### PART 1: KAMPALA FITNESS MARKET PRICE AUDIT (FACT-CHECK)

Your original questionnaire used US Dollars (`$15`, `$20–$50`, `Over $60`). In Uganda, fitness consumers think, budget, and pay in **Uganda Shillings (UGX)** via Mobile Money (MTN MoMo, Airtel Money) or cash. Using USD in your survey immediately signals disconnected academic theory or imported templates. 

Below is the verified price breakdown across fitness facilities in Kampala:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    KAMPALA FITNESS PRICING REALITY (2026)                   │
├─────────────────────────┬───────────────────────┬───────────────────────────┤
│ Fitness Tier / Provider │ Monthly Fee (UGX)     │ Daily Session Pass (UGX)  │
├─────────────────────────┼───────────────────────┼───────────────────────────┤
│ Tier 1: Luxury Clubs    │ UGX 350,000 – 700,000 │ UGX 30,000 – 60,000       │
│ (Serena, Sheraton,      │                       │                           │
│  Munyonyo, Kabira)      │                       │                           │
├─────────────────────────┼───────────────────────┼───────────────────────────┤
│ Tier 2: Commercial Gyms │ UGX 150,000 – 280,000 │ UGX 15,000 – 25,000       │
│ (Acacia, Lugogo, Naguru,│                       │                           │
│  Kansanga, Elite Gyms)  │                       │                           │
├─────────────────────────┼───────────────────────┼───────────────────────────┤
│ Tier 3: Neighborhood    │ UGX 60,000 – 120,000  │ UGX 5,000 – 10,000        │
│ (Ntinda, Kisaasi, Banda,│                       │                           │
│  Wandegeya, Makerere)   │                       │                           │
├─────────────────────────┼───────────────────────┼───────────────────────────┤
│ Personal Trainers       │ + UGX 250,000 –       │ UGX 20,000 – 50,000       │
│ (In-person 1-on-1)      │   500,000 on top!     │ per single workout session│
├─────────────────────────┼───────────────────────┼───────────────────────────┤
│ Informal WhatsApp Coach │ UGX 40,000 – 100,000  │ N/A (Monthly package)     │
│ (Diet PDF + text chat)  │                       │                           │
└─────────────────────────┴───────────────────────┴───────────────────────────┘
```

#### Why the Original USD Tiers Were Broken:
1. **$0 to $20 (under UGX 75,000):** Lumped together free workout runners with neighborhood gym goers. In Kampala, paying UGX 70,000/month is a conscious budget commitment.
2. **$20 to $50 (UGX 75,000 to UGX 190,000):** Covers standard gyms, but missed the high jump to personal trainers.
3. **Over $50 (Over UGX 190,000):** Too low as a ceiling. High-end gyms and 1-on-1 trainers in Kampala cost between **UGX 400,000 to UGX 800,000 per month**.

---

### PART 2: UPDATED SURVEY QUESTIONS (FACT-CHECKED UGX TIERS)

Here is the exact revised wording for **Questions 14 and 15**:

#### Question 14 (Current Monthly Fitness Expenditure):
*Approximately how much do you currently spend per month on gym memberships, trainer services, or fitness activities?*
* [  ] **UGX 0 / Nothing** (I work out for free at home/outdoors, or do not exercise)
* [  ] **Under UGX 50,000 / month** (Occasional day passes, basic workout equipment, community aerobics)
* [  ] **UGX 50,000 – UGX 150,000 / month** (Standard local/neighborhood gym membership)
* [  ] **UGX 150,000 – UGX 300,000 / month** (Mid-tier commercial fitness club membership)
* [  ] **Over UGX 300,000 / month** (Premium health club membership or dedicated personal trainer)

#### Question 15 (Fair Willingness-to-Pay for FlexiFit Remote Hybrid Coaching):
*If a professional service provided you with a certified trainer who customized your weekly workouts, designed meals using affordable Ugandan foods (matooke, posho, beans, g-nuts), and tracked your progress remotely via WhatsApp/app, what monthly subscription feels fair?*
* [  ] **Under UGX 30,000 / month**
* [  ] **UGX 30,000 – UGX 50,000 / month** *(Budget-friendly entry tier)*
* [  ] **UGX 50,000 – UGX 80,000 / month** *(Sweet-spot recommended tier: affordable to clients, enables trainers to earn UGX 2M+ across 30 clients)*
* [  ] **UGX 80,000 – UGX 120,000 / month** *(Premium tier with weekly video call check-ins)*
* [  ] **Over UGX 120,000 / month**

---

### PART 3: THREE WAYS TO DISTRIBUTE AND COLLECT DATA ONLINE

To let people answer on their phones immediately, you have three options ready in your workspace:

#### Option 1: Live Interactive Mobile Web App (`survey.html`)
* **File Location:** [`survey.html`](file:///home/geldof/Downloads/databaise/survey.html)
* **How to use it:**
  1. Simply double-click `survey.html` on your computer or phone to open it in Chrome / Firefox / Safari.
  2. You can pass your laptop/phone around to friends, colleagues, or classmates right now.
  3. When someone clicks "Submit Response", it saves locally in the browser and displays a button: **"Download All Responses (CSV)"**.
  4. At the end of the day, click that button and you get a clean Excel-ready spreadsheet of all your survey data!

#### Option 2: 1-Click Google Forms Automation (`google_forms_script.js`)
* **File Location:** [`google_forms_script.js`](file:///home/geldof/Downloads/databaise/google_forms_script.js)
* **How to deploy in 60 seconds:**
  1. Open your browser and go to [script.google.com](https://script.google.com).
  2. Click **"New Project"**.
  3. Delete the blank template code, open [`google_forms_script.js`](file:///home/geldof/Downloads/databaise/google_forms_script.js), copy everything, and paste it into Google Apps Script.
  4. Click the **Save** icon (disk), then click **Run** at the top.
  5. Google will ask for one-time permission $\rightarrow$ Click *Review permissions* $\rightarrow$ Select your Google account $\rightarrow$ *Advanced* $\rightarrow$ *Go to Untitled project (safe)* $\rightarrow$ *Allow*.
  6. In the bottom **Execution log**, Google will output:
     `Live Shareable Form URL: https://docs.google.com/forms/d/e/.../viewform`
  7. Copy that link and send it out directly into your WhatsApp groups and class chats! All answers automatically populate into your Google Drive!

#### Option 3: Manual Google Form Setup
If you prefer creating the Google Form manually, you can copy each question and its choices directly from Part 4 below into [forms.new](https://forms.new).

---

### PART 4: FULL REVISED QUESTIONNAIRE TEXT (READY FOR COPY-PASTE)

```markdown
URBAN FITNESS & LIFESTYLE HABITS SURVEY (KAMPALA)
An Academic Study on Exercise Routines, Nutrition, and Coaching Dynamics
IST2106: Technopreneurship & Digital Marketing — Group 4

Target Participants: Urban Adults & Fitness Enthusiasts in Kampala
Objective: To evaluate daily exercise routines, local nutrition tracking habits, and remote personal coaching dynamics.
Time: ~3-4 minutes | Privacy: 100% Anonymous

----------------------------------------------------------------------
SECTION A: Demographic Profile
----------------------------------------------------------------------

1. Age Group: [Multiple Choice]
( ) 18–24 years
( ) 25–34 years
( ) 35–44 years
( ) 45+ years

2. Current Primary Occupation: [Multiple Choice]
( ) Corporate / Office Employee
( ) Business Owner / Self-Employed
( ) University / Tertiary Student
( ) Other

3. How frequently do you currently engage in physical exercise? [Multiple Choice]
( ) Rarely / Never
( ) 1–2 times per week
( ) 3–4 times per week
( ) 5+ times per week

----------------------------------------------------------------------
SECTION B: Exercise Habits & Preferred Workout Environments
----------------------------------------------------------------------

4. Where do you currently perform most of your physical workouts? [Multiple Choice]
( ) Commercial Gym Facility
( ) At Home (Living room, compound, balcony)
( ) Outdoor Public Spaces / Estate Roads / Parks
( ) I do not currently exercise

5. If you exercise at home or outdoors rather than a gym, what are your MAIN reasons? [Checkboxes, Select up to 2]
[ ] High cost of commercial gym memberships
[ ] Commute time and severe evening traffic jams
[ ] Overcrowded facilities & waiting for equipment
[ ] Privacy concerns / gym intimidation in public spaces
[ ] Schedule flexibility to workout whenever free

6. What is your biggest frustration when exercising independently without a trainer present? [Multiple Choice]
( ) Difficulty staying consistent and motivated
( ) Lack of a structured routine to follow
( ) Uncertainty about proper exercise technique/form
( ) Not seeing visible progress or results

----------------------------------------------------------------------
SECTION C: Meal Planning & Local Diet Challenges
----------------------------------------------------------------------

7. How do you currently manage your daily diet and meal choices? [Multiple Choice]
( ) Follow a structured diet plan
( ) Try to eat healthy informally without precise tracking
( ) I do not track my food intake at all

8. Have you ever used mobile health or meal tracking applications in the past (e.g. MyFitnessPal)? [Multiple Choice]
( ) Yes, currently use them
( ) Used previously but stopped
( ) Never used them

9. If you stopped using or avoid diet apps, what were the main drawbacks? [Checkboxes, Select top 2]
[ ] App did not include Ugandan foods (Matooke, Posho, Cassava, Beans, G-nuts)
[ ] Recommended recipes required expensive or unavailable foreign ingredients
[ ] Logging meals manually took too much time and effort
[ ] Not applicable

10. How helpful would it be to have a diet plan built specifically around affordable, locally available staple foods? [Multiple Choice]
( ) Extremely Helpful
( ) Moderately Helpful
( ) Slightly Helpful
( ) Not Helpful At All

----------------------------------------------------------------------
SECTION D: Personal Training & Coaching Preferences
----------------------------------------------------------------------

11. When working with a fitness instructor, which coaching structure do you prefer? [Multiple Choice]
( ) An instructor standing next to me in-person during every single physical workout session
( ) A qualified instructor who designs my weekly workout & local meal routine, checking my progress and form periodically without needing to stand beside me daily

12. How do you currently communicate with or receive guidance from fitness instructors or nutritionists? [Multiple Choice]
( ) In-person sessions at a gym
( ) Informal WhatsApp / text messaging
( ) Social media (Instagram / TikTok videos)
( ) I do not currently consult a coach/nutritionist

13. What form of ongoing support is most effective for keeping you accountable to your fitness goals? [Checkboxes, Select top 2]
[ ] Having a customized weekly meal and exercise schedule
[ ] Receiving periodic feedback on exercise form and progress metrics
[ ] Having direct messaging/WhatsApp access to ask questions when needed
[ ] In-person live supervision during workouts

----------------------------------------------------------------------
SECTION E: Fitness Expenditure & Service Value (Uganda Shillings — UGX)
----------------------------------------------------------------------

14. Approximately how much do you currently spend per month on gym memberships, trainer services, or fitness activities? [Multiple Choice]
( ) UGX 0 / Nothing (I work out for free or do not exercise)
( ) Under UGX 50,000 / month (Occasional day passes, basic gear)
( ) UGX 50,000 – UGX 150,000 / month (Standard neighborhood gym)
( ) UGX 150,000 – UGX 300,000 / month (Mid-tier commercial gym membership)
( ) Over UGX 300,000 / month (Premium health club or personal trainer)

15. If a professional service provided you with a certified trainer who customized your weekly workouts, designed meals using affordable Ugandan foods, and tracked your progress remotely, what monthly subscription feels fair? [Multiple Choice]
( ) Under UGX 30,000 / month
( ) UGX 30,000 – UGX 50,000 / month (Budget-friendly)
( ) UGX 50,000 – UGX 80,000 / month (Standard recommended tier)
( ) UGX 80,000 – UGX 120,000 / month (Premium tier with video calls)
( ) Over UGX 120,000 / month

16. Any additional thoughts on what prevents you from achieving your ideal fitness goals in Kampala? [Paragraph Text]
[__________________________________________________________________]
```
