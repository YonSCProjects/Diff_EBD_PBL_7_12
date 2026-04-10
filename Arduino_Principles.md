# Design Principles for Arduino PBL at Agourim School

*Phase B deliverable. Distilled from the Phase A literature review across 65 verified full-text articles. These principles drive the design of the 8 Arduino projects in Phase D, the methodology section of the master proposal in Phase C, and the day-to-day workshop practice described in [Robotics_Workshop_DI_PBL_Framework.md](Robotics_Workshop_DI_PBL_Framework.md).*

**Super-target:** Create small, positive, empowering experiences for students with emotional and behavioural disorders (ADHD, ODD, anxiety, depression, OCD, post-trauma) whose confidence in learning was broken by regular primary school.

---

## How the principles were chosen

Phase A produced ~20 candidate principles across three clusters. Phase B reduced them to the **9 principles below** using three criteria:

1. **Citation strength** — each principle rests on at least 2 verified articles; most rest on 3–5. No principle depends on a single study or on inferential extension alone.
2. **Translatability** — each principle translates into a concrete design rule for the 8 Arduino projects (no abstract theorizing).
3. **Distinctiveness** — principles that collapsed into the same design rule were merged. Principles that only shaded a nuance of another were folded in as sub-notes.

Principles dropped or merged:
- "MTSS and universal screening" (Mitchell 2019) → folded into Principle 8 as a methodology note, not a principle.
- "UDL three-principle framework" (Almeqdad 2023; Phelan 2025) → kept as a design language the whole curriculum uses, not as its own principle (too abstract for per-project translation).
- "Exposure-informed anxiety support vs. avoidance accommodation" (Håland 2025) → folded into Principle 5 as a sub-note on population profile mapping, because its prescription depends on whether the student has anxiety-without-trauma or anxiety-with-trauma.
- "Functional Behavior Analysis informs intervention selection" (Harrison 2019; Barker 2022) → important but out of scope for PBL curriculum design; belongs in the teacher-implementation section of the master doc.

---

## The 9 Principles

### Principle 1 — Predictable routine is load-bearing for executive function

**Statement.** Every session follows the same rhythm. Routine is not decoration — it is the structural beam that protects executive function from stress-collapse and lets students arrive ready to work with minimum anxiety.

**Evidence.** Cumming et al. (2024, *Remedial and Special Education*) and the related Cumming et al. (2024) academic-performance paper (Verification_Log rows P1 and 69) show that perceived stress directly and negatively predicts executive function (working memory, cognitive flexibility), which in turn mediates academic outcomes (β = .61 for ELA, β = .65 for math). **EF is a state, not a trait — it collapses under stress.** Sadin (2022) and Watson & Astor (2025) show that predictable, low-surprise environments reduce trauma-response activation and support emotional regulation. Harrison, Soares, Rudzinski & Johnson (2019) identify antecedent modification — making the environment predictable before behavior happens — as one of the two classroom intervention categories that meet What Works Clearinghouse evidence-based standards for ADHD. CICO (Check-In/Check-Out) studies (Flannery et al. 2024; Kittelman et al. 2024) show that the *ritual itself* of a predictable daily check-in is calming, independent of its content.

**Design rule for the Arduino projects.**
- Every workshop session follows the 7-phase structure from [Robotics_Workshop_DI_PBL_Framework.md](Robotics_Workshop_DI_PBL_Framework.md) Part 1: Arrival & Board Check → Mini-Huddle → Work Block 1 → Movement Break → Work Block 2 → Clean-Up → Close-Out Circle.
- No surprises. Any deviation from routine is announced at the Mini-Huddle with an explicit reason.
- Every project's task cards live at predictable physical locations (same place on the workbench, same color-coded clip) so students never have to hunt for their work.
- Every project begins with a predictable recap: "Here's where you left off; here's what you're doing next."

---

### Principle 2 — The task card is the boss, not the teacher

**Statement.** Visual task cards, checklists, and reference sheets guide students through work. The teacher rotates, supports, and celebrates — but does not give verbal multi-step instructions or direct commands. This bypasses ODD power-struggle triggers, bypasses working-memory overload, and lets students work independently so the teacher can focus on whoever needs help.

**Evidence.** Barker & de Lugt (2022, *International Journal of Special Education*) state that **ODD is an interactional disorder** — symptoms occur in relationships, and children with ODD "rebel against any attempt to modify or influence their behavior, both positively (e.g., using rewards) or negatively (e.g., using punishments). They will see this as a manipulation, and will act in a way that counters the person trying to modify their behavior." The same paper reports that environmental modifications — including self-monitoring and group contingencies that remove the adult–child confrontation — are the evidence-based classroom interventions for ODD. The robotics-in-special-ed literature converges on the same point from the opposite direction: Papakostas et al. (2021) and Berrezueta-Guzmán et al. (2021, *IEEE Access*) show that **a non-human mediator** (a robot, a visual schedule, a physical checklist) reduces social anxiety and perceived coercion while maintaining task accountability. Rosen, Boyle, Cariss & Forchelli (2014, EJ1168865) show that external cognitive scaffolds open pathways for students with EF deficits to access and flexibly deploy cognitive strategies — students don't need intact EF to USE the scaffold, and practicing with the scaffold is how their EF improves. Thomas & Karuppali (2022) show visual activity schedules reduce latency to initiate tasks and reduce off-task behavior during transitions in ADHD children.

**Design rule for the Arduino projects.**
- Every step of every project lives on a Task Card (template in [Robotics_Workshop_DI_PBL_Framework.md](Robotics_Workshop_DI_PBL_Framework.md) Part 2).
- Teachers never give verbal multi-step instructions. Instead: "Check your next card." Or: "What does the card say the next step is?"
- When a student gets stuck, the teacher points at the card's "Stuck? Try this first" protocol before offering a direct hint.
- Task cards are laminated and placed at each workstation. For project 1 (first session), the teacher walks students through the card format once, then stops explaining and lets the card do the work.
- Corrections come from the hardware, not the teacher where possible: "Your LED isn't lighting up — check the card. What does the checkpoint say?"

---

### Principle 3 — Physical-first, then abstract (concrete → representational → abstract)

**Statement.** Students build the wiring before they write the code. They see the hardware do something before they abstract it. CRA — concrete first, representational (diagrams) second, abstract (code, equations) third — is not optional for students with learning disabilities and ADHD. They cannot skip the concrete phase.

**Evidence.** Hwang & Taylor (2016, *Journal of Science Education for Students with Disabilities*) frame CRA as prerequisite for students with disabilities in STEM. Israel et al. (2015, *Computers & Education*) show that explicit, scaffolded support within computational-thinking work is critical for diverse learners, including those with EF deficits — students thrive when the abstract (code) is grounded in the concrete (physical). Kuzmina & Romero (2025) show that modular robotic tasks with tangible components enable divergent thinking and task performance in children with ADHD. Belland, Walker, Kim & Lefler (2017, *Review of Educational Research*) meta-analysis (g = 0.71) shows scaffolding is especially effective in PBL contexts; their analysis of effective scaffolds includes physical/material supports as a category alongside peer collaboration and teacher modeling. The Berrezueta-Guzmán et al. (2021) robot-assistant studies and Cibrian et al. (2022) on emerging technologies show that **hands-on manipulation with immediate feedback** supports self-regulation in ADHD — students see the effect of their action before they need to explain it.

**Design rule for the Arduino projects.**
- Every project begins with a wiring-only milestone: breadboard and wires before any code is written. Students see the circuit and understand what it does physically.
- The first observable outcome of any project is physical: an LED lights, a motor spins, a buzzer sounds. Code comes after the hardware works.
- When students write their first code for a project, they are modifying pre-written scaffold code that already matches their wiring — they never start from a blank editor.
- Code explanations reference the hardware: "This line turns pin 13 HIGH, which sends voltage to the wire that goes to your LED's long leg."
- For project 8 (quadcopter), the CRA progression becomes: frame assembly (concrete) → wiring diagram tracing (representational) → Claude-Code-assisted firmware generation (abstract).

---

### Principle 4 — Hyper-chunked 15-minute milestones with visible wins

**Statement.** Every step of every project produces a concrete, observable outcome within 10–15 minutes. No silent work periods longer than that. No "and then you'll see the result tomorrow." Every 15 minutes, something in the real world changes because the student did something — a light turns on, a motor spins, a sensor reads a value, a number on the screen changes. This is the dopamine drip that sustains ADHD engagement, builds momentum for students with depression, and creates evidence of competence for students whose school history has taught them they can't do things.

**Evidence.** Guneysu Ozgur et al. (2020, *Frontiers in Robotics and AI*) show that iterative physical milestones with tangible robot-assisted output support engagement and reduce frustration in special education. Berrezueta-Guzmán, Robles-Bykbaev, Pau, Pesántez-Avilés & Martín-Ruiz (2021) literature review on robotic technologies in ADHD care identifies hands-on tangible feedback as a core mechanism supporting executive function, attention span, and task-completion rates. Cibrian, Lakes, Schuck & Hayes (2022, *International Journal of Child-Computer Interaction*) report that hands-on technological interventions supplying immediate tangible feedback support self-regulation in children with ADHD. Taylor, Allen, Van & Moohr (2024, *Journal of Emotional and Behavioral Disorders*) — the only empirical PBL-in-EBD classroom study we have — reports very large effect sizes on on-task behavior (BC-SMD = 1.70–3.81) for high-quality PBL in an EBD classroom; the study attributes much of this to the PBL design's "sustained inquiry" combined with frequent, visible milestones. Belland et al. (2017) meta-analysis supports persistent rather than faded scaffolding — students don't need big leaps, they need many small supported wins.

**Design rule for the Arduino projects.**
- Every task card maps to ≤ 15 minutes of work with an observable "done when" checkpoint.
- Long steps in the existing quadcopter source material (e.g., "Power Wiring — 15 min") are subdivided into 3–5 micro-tasks of 4–8 minutes each, each with its own physical checkpoint.
- No project has a silent middle where students work for 20+ minutes with nothing visible happening. If the natural work unit is that long, it must be broken or scaffolded with an intermediate indicator (serial-monitor print, LED status, buzzer beep) that shows progress.
- Every milestone completion is celebrated with visible progress tracking — a checkmark, a clip moved to the next position, a sticker on the tracking sheet, or just a fist bump when the teacher rotates past.

---

### Principle 5 — Structured autonomy, not forced compliance

**Statement.** Every project offers at least one genuine choice point, even at Tier 1. "Do you want a red or blue LED?" "Which sensor — ultrasonic or IR?" "Which name for your robot?" Choice reduces oppositional resistance, increases intrinsic motivation, and respects student agency. But structure and choice are partners, not opposites. External structure (checklists, scaffolds, reinforcement, pre-built templates) is enabling, not undermining, for ADHD — it creates the safe envelope inside which autonomy becomes possible.

**Evidence.** Billingsley, Thomas & Webber (2018, *Learning Disability Quarterly*) show that when students with comorbid LD and EBD chose *how* they received instruction, engagement and task completion improved; **choice itself reduced problem behavior by transferring ownership**. Barker & de Lugt (2022) same paper cited in Principle 2: ODD responds to autonomy, not coercion. Taylor et al. (2024) HQPBL framework explicitly lists Student Voice as one of the eight elements and attributes large on-task effects in an EBD classroom to PBL's choice-and-authenticity design. Smith, Langberg, Cusick, Green & Becker (2020, *Journal of Abnormal Child Psychology*) show that adolescents with ADHD have lower intrinsic motivation (d = 0.49) AND lower extrinsic motivation (d = 0.43) than peers — but **extrinsic motivation paradoxically supports homework completion and GPA for ADHD students**, meaning structured external support is not undermining, it's enabling. Morsink et al. (2022) explores the role of internal motives in ADHD and warns against external reinforcement systems that undermine intrinsic motivation — the nuance is that *structure* and *choice* must coexist: rigid structure without choice breeds resistance; pure autonomy without structure breeds paralysis.

**Design rule for the Arduino projects.**
- Every project has at least one genuine choice point at Tier 1 (color, name, one parameter).
- Every project has 2–3 choice points at Tier 2 (component selection, design decision, output behavior).
- Tier 3 of every project is an open-design brief with hard constraints (hardware budget, time, safety) but free creative direction.
- No reward/token systems (per Barker & Morsink: ODD reads them as manipulation, ADHD responds to them as substitutes for intrinsic competence). Celebrations are social and immediate, not bureaucratic and deferred.
- **Population profile sub-rules:**
  - For **OCD** students: private workspace by default; never forced public demo; task cards with clear "done when" criteria to prevent perfectionism spirals; flexible timing with no "you must finish this before X." (Abramovitch et al. 2024; Colbert et al. 2025)
  - For **anxiety without trauma**: scaffold approaches to feared tasks rather than permanent avoidance accommodation (Håland 2025 — compassionate short-term accommodation can worsen long-term outcomes).
  - For **anxiety with trauma history**: safety and predictability first; no forced exposure; use Principle 1 (predictable routine) as the anxiety management mechanism, not exposure (Watson 2025; Sadin 2022; Koslouski et al. 2023).
  - For **ODD**: frame tasks as choices or requests, never commands. "When you're ready, your next card is here."
  - For **depression**: smallest possible first step; visible tangible results; celebrate micro-progress privately.

---

### Principle 6 — Movement is medicine for ADHD (not a reward, not a release valve)

**Statement.** Every session includes a structured movement break. This is not an "optional energy release" for students who "can't sit still" — it is a first-class intervention with the largest effect sizes in the ADHD literature for exactly the deficits this population has.

**Evidence.** Qiu, Liang, Wang, Zhang & Shum (2023, *Asian Journal of Psychiatry*) meta-analysis of 67 non-pharmacological EF intervention studies for ADHD found **physical exercise produced the largest effect sizes of all intervention types**: g = 0.900 on inhibitory control and **g = 1.377 on cognitive flexibility**. For comparison, cognitive training produced g = 0.907 on working memory; EF-specific curriculum g = 0.532 on planning. Physical exercise is not just competitive with other interventions — it's the best single intervention measured for ADHD executive function. Cumming et al. (2024, both papers) independently shows that EF (especially cognitive flexibility) degrades under stress, and movement is a direct stress intervention.

**Design rule for the Arduino projects.**
- The workshop session structure from [Robotics_Workshop_DI_PBL_Framework.md](Robotics_Workshop_DI_PBL_Framework.md) Part 1 includes a 3–5 minute Movement Break between Work Block 1 and Work Block 2. This break is **non-negotiable and applies to every session**, even when a student is in flow state. ("Especially when a student is in flow state — the break protects the next hour's flow.")
- Movement breaks are structured, not free-for-all: stand up, get water, walk around the room once, stretch for 30 seconds. Structured because unstructured breaks spike dysregulation for students with ODD or trauma.
- Kinesthetic elements are embedded in task cards where possible: "Walk to the parts bin and get a 220Ω resistor" is better than "reach for the resistor." Test steps involve standing up: "Stand up, hold the drone, and spin the propeller with your finger — does it turn freely?"

---

### Principle 7 — Claude Code as pair programmer, not oracle

**Statement.** Students don't copy-paste code from Claude Code. They describe what they're trying to build, show what they've already tried, ask for help understanding why it isn't working, and iterate in dialogue. The AI is a collaborator they direct — not an answer machine. This preserves metacognition, teaches debugging language, and prevents the dependency that comes from copy-paste learning.

**Evidence.** This principle has **no direct empirical support in the verified corpus** — zero studies in the 65 full-text articles examine Claude Code, conversational AI tutors, or AI-paired learning for neurodivergent students. The principle rests on **responsible inference** from three adjacent bodies of evidence that converge on the same implication:

1. Rosen, Boyle, Cariss & Forchelli (2014) on scaffolded EF: external cognitive scaffolds enable students to practice EF they don't yet have. A well-designed prompt scaffold is an external cognitive scaffold.
2. Morsink et al. (2022) on ADHD motivation: external reinforcers and answer-givers undermine intrinsic motivation and competence-building. An AI that gives answers on demand becomes an extrinsic reward system; an AI that asks questions back becomes a scaffold.
3. Smith, Langberg et al. (2020) on adolescent ADHD motivation: extrinsic support helps academic outcomes when structured, not when it replaces the student's own work.

**Honest caveat:** This principle is the weakest-supported in the list and will be flagged explicitly in the Honest Limitations section of the master document. If the master document is going to argue that Claude Code integration is a valuable feature, it must acknowledge this is an untested practice being piloted in good faith.

**Design rule for the Arduino projects.**
- Every code-writing milestone in every project includes a **Claude Code prompt scaffold** — a template the student adapts. Example: *"I want to make the LED blink every half second. Here's my current code: [paste]. When I run it, [what happens]. Can you help me understand why it's not doing what I want?"*
- Students must describe the problem before asking for help. Task cards say: "Before asking Claude, fill in: (a) what you want to happen, (b) what's currently happening, (c) what you've tried."
- No copy-paste-without-understanding. Task cards include a quick comprehension check: "After Claude helps you, can you explain in one sentence what changed?"
- For project 8 (quadcopter), the `TinyQuadcopter.ino` file in the source material is currently an empty stub — the real firmware lives as pseudocode in the README. This is actually a feature: Tier 2/3 students generate the actual .ino from the README pseudocode using Claude Code as their pair programmer, which is a perfect real-world application of this principle.

---

### Principle 8 — Relationships are the multiplier

**Statement.** Structure alone does not work. Structure + relationships works. Peer collaboration must be explicitly taught (not just "put kids in groups"), teacher rotation must include relational check-ins (not just task progress), and the workshop culture must prioritize trust over task completion. The relationship is the soil in which independent work grows.

**Evidence.** Gersib & Mason (2023) meta-analysis of behavior interventions in self-contained EBD classrooms: effects were large overall (g = 0.93), but **relational components — parent communication, peer support, adult mentoring — were the strongest moderator** (B = 1.26, p < .05). Structured classrooms with relational supports outperformed structured classrooms alone. Wattanawongwan, Smith & Vannest (2021, *Beyond Behavior*) show cooperative learning for EBD requires explicit teaching and monitoring of five elements (positive interdependence, individual accountability, face-to-face interaction, social skills, group processing) — just grouping students does not work. Gage, Kramer II & Ellis (2021, *Journal of Disability Policy Studies*) analyzing 350,000+ high school students, including 5,000+ with/at-risk-for EBD, found that EBD students report more negative perceptions of school climate, but **EBD students with IEP services perceived more positive climates than EBD students without IEP services** — formal, visible adult support improves sense of belonging. Koslouski, Stark & Chafouleas (2023) and Asselman et al. (2025) on trauma-informed environments emphasize relationship quality, trust, and adult co-regulation as the mechanism through which students develop resilience and self-regulation. Gomez (2019) UTSA dissertation on makerspace learning for EBD — the closest analog in the corpus to the Arduino workshop — found that makerspace participation supported social-emotional skill development compared to traditional classroom contexts, specifically through peer interaction opportunities.

**Design rule for the Arduino projects.**
- Workshop sessions open with Arrival & Board Check (greet each student by name, brief 1-word check-in) and close with a Close-Out Circle (each student says one thing they worked on or got stuck on). These are not optional social filler — they are relationship infrastructure.
- Teacher rotation during work blocks includes relational check-ins, not just task progress: "How are you doing with this?" before "Where are you on the card?"
- Peer collaboration is scaffolded explicitly with defined roles when groups work together (Driver, Navigator, Documentarian, Peacekeeper — inspired by the role taxonomy in the source quadcopter project's `claude.md`). Role swaps every 2–3 steps to build shared understanding.
- Projects 1–2 are primarily individual (building individual student–teacher trust). Projects 3–7 introduce structured pair work on specific milestones. Project 8 (quadcopter) has flight phases that require one-at-a-time attention but build phases that benefit from peer collaboration.

---

### Principle 9 — Teacher sustainability is a first-class design constraint

**Statement.** The curriculum must be designed so one teacher managing 3–8 EBD students can run a session without burning out. Pre-prepared materials. Self-directed task cards. Laminated reference sheets. Clear session structure. Predictable rhythms. If the teacher is exhausted, the whole system fails — student outcomes collapse first.

**Evidence.** Gilmour, Sandilos, Pilny, Schwartz & Wehby (2022, *Journal of Emotional and Behavioral Disorders*) used latent profile analysis to identify three teacher burnout profiles when teaching EBD students — flourishing, buffered, struggling — and showed that **burnout profile predicts observed classroom management quality**: struggling teachers used fewer effective strategies and gave less autonomy to students. Burnout is not just a teacher-welfare issue; it directly harms student outcomes. Taylor et al. (2024) uniquely measured teacher job satisfaction as a PBL outcome and showed it **improved** post-intervention: well-designed PBL can actually reduce teacher burden in EBD contexts by shifting the teacher from crisis-manager to facilitator. Koslouski et al. (2023) explicitly addresses secondary traumatic stress in educators and calls educator well-being "crucial to remaining healthy and effective" when working with traumatized students. Asselman et al. (2025) and Gilmour et al. (2022) converge: supporting teacher emotional resilience is not optional — it is necessary for student outcomes.

**Design rule for the Arduino projects.**
- Every project ships with **pre-prepared teacher materials**: printed task cards ready to laminate, a setup checklist for before students arrive, a rotation plan suggesting which students to start with, a troubleshooting crib sheet.
- No prep work should require the teacher to write from scratch during a session.
- Projects are scoped so they can be run the first time by a teacher who has read the master document once — no additional training required. (Colbert et al. 2025 on brief written materials outperforming long workshops directly supports this.)
- The session structure (Principle 1) IS a teacher-sustainability mechanism — predictable rhythms reduce the cognitive load of deciding what happens next.
- The Claude Code prompt scaffolds (Principle 7) are also a teacher-sustainability mechanism — the teacher is not the only debugging resource in the room.
- Ministry proposal implication: the program should include budget for teacher release time, peer co-facilitation, and a lightweight check-in protocol between sessions — not a heavy training/coaching apparatus.

---

## How the principles map to the 8 Arduino projects

| # | Project | Primary principles this project demonstrates |
|---|---------|---------------------------------------------|
| 1 | Light Signals | 1, 2, 3, 4, 5, 6, 7 (all except relationships — mostly individual work) |
| 2 | Reaction-Time Game | 1, 2, 3, 4, 5, 6, 7, 8 (pair play introduces relational element) |
| 3 | Don't Get Too Close | 1, 2, 3, 4, 5, 6, 7 |
| 4 | Line-Following Car | 1, 2, 3, 4, 5, 6, 7, 8 (pair build) — soldering prerequisite introduced |
| 5 | Remote-Controlled Car | 1, 2, 3, 4, 5, 6, 7, 8 |
| 6 | ESP32 Wi-Fi Controller | 1, 2, 3, 4, 5, 6, 7, 8 — I2C prerequisite for Project 8 introduced |
| 7 | Camera-Equipped Explorer | 1, 2, 3, 4, 5, 6, 7, 8 |
| 8 | Tiny ESP32 Quadcopter (8.5×20mm) | **All 9 principles.** This is the capstone where every principle is load-bearing simultaneously — routine protects EF under the stress of first flight; task cards handle the fine-motor wiring steps; physical-first wiring before firmware; hyper-chunked safety protocol; structured autonomy in flight sequences; movement breaks between high-focus tuning sessions; Claude Code generates the firmware from the README pseudocode; peer collaboration during build, strict one-at-a-time during flight; teacher sustainability protected by pre-assembled Tier-1 cores and a dedicated safety checklist. |

Every project file in `Arduino_Projects/` will include a `[Principles: #N, #M, …]` tag at each major design choice showing which of these principles it embodies.

---

## What the principles do NOT claim

In the spirit of the Phase A honest-caveats section, these principles do NOT claim to be:

- **Empirically validated as a package.** No study tests this combination of principles for EBD students in an Arduino PBL context.
- **Sufficient by themselves.** Students with severe trauma, OCD, or depression also need therapeutic support alongside good instruction.
- **Diagnosis-based prescriptions.** The population-profile sub-rules under Principle 5 are adaptive guidance, not universal prescriptions.
- **A guarantee of success.** The first 3–4 sessions of any new workshop will be rocky. Expect dysregulation before the routines set in.
- **Quantified.** The design rules are grounded in mechanisms, not in point estimates. Where effect sizes appear in the evidence sections, they describe the research findings, not predictions for Agourim outcomes.
- **A substitute for professional judgment.** Every principle has edge cases the teacher will recognize better than the curriculum document.

The master document (Phase C) will carry these caveats into its Honest Limitations section prominently, not as a footnote.

---

## Phase B audit findings (for the record)

During Phase B, a targeted re-audit of the Verification_Log "Partial / Corrected" entries where the initial verifier sweep might have invented authorship produced three findings:

1. **P1 (Cumming et al.) and row 69 — two different papers, not one.** The file `articles_full_texts/cumming_2024.txt` contains "Executive Function, Perceived Stress, and Academic Performance Among Middle Schoolers With and Without Behavior Problems" by Cumming, Oblath, Qiu, Frazier, Zelazo, Flores & Park (2024, *Remedial and Special Education*, 45(2), 85–100, DOI 10.1177/07419325231176762) — **now logged as row 69**. The original project files (Bibliography, Detailed_Article_Summaries, Framework) cite a DIFFERENT paper: "Perceived Stress, Executive Function, and Stress Regulation: Implications for Middle Schoolers' Emotional and Behavioral Well-being" by Cumming, Qiu, Oblath, Frazier, Criado, Theodore & Placido (2024, *Remedial and Special Education*, 46(6), 426–441, DOI 10.1177/07419325241265973) — **this is P1**. Both are real Crossref-verified papers by the same research group. Phase B corrected Detailed_Article_Summaries.md §8 and references (year 2025 → 2024; journal "Behavioral Disorders" → "Remedial and Special Education"; volume/issue/pages added) and Robotics_Workshop_DI_PBL_Framework.md (year 2025 → 2024). The lit review synthesis in Phase A used Paper B's content (the file) but will carry citations for both papers in the master document.

2. **P5 (Kuzmina & Romero 2025) — clean.** Crossref confirms: Kuzmina, O. & Romero, M. (2025). "Study of divergent thinking and task performance in children with ADHD through a modular robotic task." *Australian Journal of Learning Difficulties*, 30(2), 169–186. Matches the Verification_Log entry. Additional metadata (volume/issue/pages) available and can be added to the log during Phase C.

3. **P10 (Guneysu Ozgur et al. 2020) — clean.** Crossref confirms all 8 authors in the listed order. Matches the Verification_Log entry.

4. **P12 (Barker & de Lugt 2022) — clean, with bonus.** Publisher page confirms Barker, C. & de Lugt, J. (2022). "A review of evidence based practices to support students with oppositional defiant disorder in classroom settings." *International Journal of Special Education*, 37(1), 85–98. Bonus: the publisher page lists a DOI (10.52291/ijse.2022.37.29) that the Verification_Log entry is missing — can be added during Phase C.

5. **P2 (Rosen et al. 2014) and P11 (Gibbs 2023) — already re-corrected in Phase A.** No further action.

**Meta-conclusion.** The initial verifier sweep's failure pattern is confirmed: when a citation had a DOI and was cross-checked against Crossref, the correction is reliable (P3, P5, P7, P8, P9, P10 all check out). When a citation lacked a DOI and the correction had to come from WebSearch or inference, the correction is unreliable (P2 and P11 were both wrong; P12 turned out fine but had weaker provenance). For the master document's references section in Phase C, I recommend running every citation through Crossref one final time and treating Crossref as the source of truth.

**Paper A / Paper B caution for the master document.** The two Cumming papers are by the same research group on overlapping topics. The master document should cite both, with Paper A (the stress-regulation paper) for the broader framing and Paper B (the academic-performance paper) for the specific EF-mediation findings we read in full text (β = .61 for ELA, β = .65 for math).

---

## Phase C preview

Phase C (Master Document Assembly) will:

1. Use these 9 principles as the backbone of the Methodology section.
2. Write an Introduction and Population Profile that explains why these principles matter for Agourim students specifically.
3. Write a Literature Review section that draws from Arduino_LitReview_Cluster1/2/3 files and cites the 66 verified articles + the new row 69.
4. Run every citation through one final Crossref verification pass before committing to the References section.
5. Produce a Budget section built around the 8-project hardware list, including the 8.5×20mm quadcopter cohort budget from the plan file.
6. Write Honest Limitations prominently, including the untested Claude-Code-as-tutor principle and the drone-research gap.
7. Decide whether these principles stay in a standalone `Arduino_Principles.md` or get inlined into the master document. Current leaning: keep standalone, reference from the master doc, so that a teacher can print the principles alone as a quick reference without printing the full proposal.
