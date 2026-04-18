# Design Principles for Arduino PBL at Agourim School

*Phase B deliverable. Distilled from the Phase A literature review across 65 verified full-text articles. These principles drive the design of the 8 Arduino projects in Phase D, the methodology section of the master proposal in Phase C, and the day-to-day workshop practice described in [Robotics_Workshop_DI_PBL_Framework.md](Robotics_Workshop_DI_PBL_Framework.md).*

**Super-target:** Create small, positive, empowering experiences for students with emotional and behavioural disorders (ADHD, ODD, anxiety, depression, OCD, post-trauma) whose confidence in learning was broken by regular primary school.

---

## How the principles were chosen

Phase A produced ~20 candidate principles across three clusters. Phase B reduced them to the **9 principles** through Principle 9; **Principle 10** was added in a later iteration from a staff-training lecture at Agourim school (Michal & Smadar, 2025) on flexibility in defining ways of participation — see Principle 10's evidence section for the reasoning and the explicit caveat that its support comes from clinical practice at the school rather than from the verified 65-article corpus. The 10 principles together were selected using three criteria:

1. **Citation strength** — each principle rests on at least 2 verified articles; most rest on 3–5. No principle depends on a single study or on inferential extension alone.
2. **Translatability** — each principle translates into a concrete design rule for the 8 Arduino projects (no abstract theorizing).
3. **Distinctiveness** — principles that collapsed into the same design rule were merged. Principles that only shaded a nuance of another were folded in as sub-notes.

Principles dropped or merged:
- "MTSS and universal screening" (Mitchell 2019) → folded into Principle 8 as a methodology note, not a principle.
- "UDL three-principle framework" (Almeqdad 2023; Phelan 2025) → kept as a design language the whole curriculum uses, not as its own principle (too abstract for per-project translation).
- "Exposure-informed anxiety support vs. avoidance accommodation" (Håland 2025) → folded into Principle 5 as a sub-note on population profile mapping, because its prescription depends on whether the student has anxiety-without-trauma or anxiety-with-trauma.
- "Functional Behavior Analysis informs intervention selection" (Harrison 2019; Barker 2022) → important but out of scope for PBL curriculum design; belongs in the teacher-implementation section of the master doc.

---

## The 10 Principles

### Principle 1 — Predictable routine is load-bearing for executive function

**Statement.** Every session follows the same rhythm. Routine is not decoration — it is the structural beam that protects executive function from stress-collapse and lets students arrive ready to work with minimum anxiety.

**Evidence.** Cumming et al. (2024, *Remedial and Special Education*) and the related Cumming et al. (2024) academic-performance paper (Verification_Log rows P1 and 69) show that perceived stress directly and negatively predicts executive function (working memory, cognitive flexibility), which in turn mediates academic outcomes (β = .61 for ELA, β = .65 for math). **EF is a state, not a trait — it collapses under stress.** Koslouski, Stark & Chafouleas (2023) describe how chronic trauma activates survival-mode (fight/flight/freeze) responses under unpredictable conditions, disrupting executive function; their trauma-primer for educators frames predictable, safe environments as foundational. Watson & Astor (2025), in their critical review of trauma-informed approaches in schools, endorse the safety and relationships components of the approach as well-founded while cautioning that the whole-school empirical base is more limited (§9 returns to this caveat). Harrison, Soares, Rudzinski & Johnson (2019) identify **instructional and self-management interventions** as the two classroom intervention categories that meet What Works Clearinghouse evidence-based standards for ADHD — both categories fit the shape of a workshop built around predictable navigation cards and self-monitoring routines. CICO (Check-In/Check-Out) studies (Flannery et al. 2024; Kittelman et al. 2024) show that predictable daily check-in routines improve on-task behavior and engagement for high-school students with or at risk for EBD.

**Design rule for the Arduino projects.**
- Every workshop session follows the 7-phase structure from [Robotics_Workshop_DI_PBL_Framework.md](Robotics_Workshop_DI_PBL_Framework.md) Part 1: Arrival & Board Check → Mini-Huddle → Work Block 1 → Movement Break → Work Block 2 → Clean-Up → Close-Out Circle.
- No surprises. Any deviation from routine is announced at the Mini-Huddle with an explicit reason.
- Every project's navigation cards live at predictable physical locations (same place on the workbench, same color-coded clip) so students never have to hunt for their work.
- Every project begins with a predictable recap: "Here's where you left off; here's what you're doing next."

---

### Principle 2 — The navigation card traces the path

**Statement.** Visual navigation cards, checklists, and reference sheets guide students through work. The teacher rotates, supports, and celebrates — but does not give verbal multi-step instructions or direct commands. This bypasses ODD power-struggle triggers, bypasses working-memory overload, and lets students work independently so the teacher can focus on whoever needs help.

**Evidence.** Barker & de Lugt (2022, *International Journal of Special Education*) present the theoretical framing that ODD is best understood as **an interactional disorder** — symptoms occur in relationships, not as fixed traits — and quote Barkley & Benton (2013) on the theoretical concern that children with ODD may read direct behavior-modification attempts as manipulation. More importantly for the workshop's design, Barker & de Lugt's own empirical review reports that environmental modifications — including self-monitoring, group contingencies, and well-structured classroom interventions — produce strong positive effects for students with ODD in classroom settings (§4 Principle 5 returns to this evidence base in detail). Berrezueta-Guzmán, Robles-Bykbaev, Pau, Pesántez-Avilés & Martín-Ruiz (2021, *IEEE Access*) and Cibrian, Lakes, Schuck & Hayes (2022, *International Journal of Child-Computer Interaction*) document that hands-on technological interventions and robot-assisted supports provide structured, non-threatening feedback that sustains attention and task completion in children with ADHD — a pattern we describe informally as a "non-human mediator" effect, aggregating across multiple studies rather than citing a unified synthesis of it. Rosen, Boyle, Cariss & Forchelli (2014, EJ1168865) show that external cognitive scaffolds open pathways for students with EF deficits to access and flexibly deploy cognitive strategies — students don't need intact EF to USE the scaffold, and practicing with the scaffold is how their EF improves. Thomas & Karuppali (2022) show visual activity schedules reduce latency to initiate tasks and reduce off-task behavior during transitions in ADHD children.

**Design rule for the Arduino projects.**
- Every step of every project lives on a Navigation Card (template in [Robotics_Workshop_DI_PBL_Framework.md](Robotics_Workshop_DI_PBL_Framework.md) Part 2).
- Teachers never give verbal multi-step instructions. Instead: "Check your next card." Or: "What does the card say the next step is?"
- When a student gets stuck, the teacher points at the card's "Stuck? Try this first" protocol before offering a direct hint.
- Task cards are laminated and placed at each workstation. For project 1 (first session), the teacher walks students through the card format once, then stops explaining and lets the card do the work.
- Corrections come from the hardware, not the teacher where possible: "Your LED isn't lighting up — check the card. What does the checkpoint say?"

---

### Principle 3 — Physical-first, then abstract (concrete → representational → abstract)

**Statement.** Students build the wiring before they write the code. They see the hardware do something before they abstract it. CRA — concrete first, representational (diagrams) second, abstract (code, equations) third — is not optional for students with learning disabilities and ADHD. They cannot skip the concrete phase.

**Evidence.** Hwang & Taylor (2016, *Journal of Science Education for Students with Disabilities*) frame CRA as prerequisite for students with disabilities in STEM. Israel et al. (2015, *Computers & Education*) show that explicit, scaffolded support within computational-thinking work is critical for diverse learners, including those with EF deficits — students thrive when the abstract (code) is grounded in the concrete (physical). Kuzmina & Romero (2025) explored divergent thinking with children with ADHD using a modular robotic task (CreaCube); while their quantitative hypotheses that ADHD children would score higher on divergent-thinking measures (fluency, flexibility, originality) were NOT statistically supported, their qualitative observations noted distinct process differences — most notably, five out of seven ADHD children spontaneously used a think-aloud technique during the task, which the authors interpret as a self-regulation strategy. The paper's direct evidence is therefore about process patterns, not performance effects. Belland, Walker, Kim & Lefler (2017, *Review of Educational Research*) meta-analysis of computer-based scaffolding in STEM reports an overall effect size of **g = 0.46** across contexts, with scaffolding producing **directionally stronger effects in project-based learning contexts than in problem-based learning** (z = 6.08, p < .01), and **significantly higher effects for underperforming students than for traditional learners** (z = 2.29, p < .05). Their analysis of effective scaffolds includes physical/material supports as a category alongside peer collaboration and teacher modeling. The Berrezueta-Guzmán et al. (2021) robot-assistant studies and Cibrian et al. (2022) on emerging technologies show that **hands-on manipulation with immediate feedback** supports self-regulation in ADHD — students see the effect of their action before they need to explain it.

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
- Every navigation card maps to ≤ 15 minutes of work with an observable "done when" checkpoint.
- Long steps in the existing quadcopter source material (e.g., "Power Wiring — 15 min") are subdivided into 3–5 micro-tasks of 4–8 minutes each, each with its own physical checkpoint.
- No project has a silent middle where students work for 20+ minutes with nothing visible happening. If the natural work unit is that long, it must be broken or scaffolded with an intermediate indicator (serial-monitor print, LED status, buzzer beep) that shows progress.
- Every milestone completion is celebrated with visible progress tracking — a checkmark, a clip moved to the next position, a sticker on the tracking sheet, or just a fist bump when the teacher rotates past.

---

### Principle 5 — Structured autonomy, not forced compliance

**Statement.** Every project offers at least one genuine choice point, even at Tier 1. "Do you want a red or blue LED?" "Which sensor — ultrasonic or IR?" "Which name for your robot?" Choice reduces oppositional resistance, increases intrinsic motivation, and respects student agency. But structure and choice are partners, not opposites. External structure (checklists, scaffolds, reinforcement, pre-built templates) is enabling, not undermining, for ADHD — it creates the safe envelope inside which autonomy becomes possible.

**Evidence.** Billingsley, Thomas & Webber (2018, *Learning Disability Quarterly*) show that when students with comorbid LD and EBD chose *how* they received instruction, engagement and task completion improved; **choice itself reduced problem behavior by transferring ownership**. Barker & de Lugt (2022) — same paper cited in Principle 2 — supports ODD interventions grounded in environmental modification and structured autonomy rather than direct coercion. Taylor et al. (2024) HQPBL framework explicitly lists Student Voice as one of the eight elements and attributes large on-task effects in an EBD classroom to PBL's choice-and-authenticity design. Smith, Langberg, Cusick, Green & Becker (2020, *Journal of Abnormal Child Psychology*) show that adolescents with ADHD have lower intrinsic motivation (d = 0.49) AND lower extrinsic motivation (d = 0.43) than peers — but **extrinsic motivation paradoxically supports homework completion and GPA for ADHD students**, meaning structured external support is not undermining, it's enabling. Morsink et al. (2022) applies Self-Determination Theory to ADHD motivation research, arguing that ADHD research has focused narrowly on external reinforcement effects while under-investigating internal motives (autonomy, competence, relatedness). Their review of empirical studies that tested whether external rewards undermine intrinsic motivation in children with ADHD — Carlson et al. (2000) and Carlson & Tamm (2000) — reports that neither study found the undermining effect, though Morsink et al. call for more research into conditions under which it might appear. The broader implication for design is that motivation is best supported by a balance of structure and autonomy: rigid structure without choice frustrates the autonomy need; pure autonomy without structure frustrates the competence need.

**Autonomy applies across projects, not just within them.** The same logic extends beyond choice points within a single project to the order and timing of projects across the program. For some students — particularly those whose school history includes many encounters with prescribed sequences they had no voice in — the refusal to follow the prescribed eight-project order is itself an expression of the very autonomy this principle protects. Treating that refusal as a failure to comply reproduces the same power dynamic the principle is trying to avoid. Instead, the program reframes prerequisites as **skills to acquire**, not **projects to complete in sequence**: a student who wants to start with a later project can do so, and the teacher scaffolds the missing skills just-in-time with targeted mini-modules rather than blocking the student at the doorway. A student's refusal to engage with a specific project on a specific day is treated as information about what they need ("what would make today worth your time?"), not as defiance to be corrected. The master document's §5 Methodology section contains the detailed teacher guidance for this case, including a short decision tree for the most common refusal patterns.

**Design rule for the Arduino projects.**
- Every project has at least one genuine choice point at Tier 1 (color, name, one parameter).
- Every project has 2–3 choice points at Tier 2 (component selection, design decision, output behavior).
- Tier 3 of every project is an open-design brief with hard constraints (hardware budget, time, safety) but free creative direction.
- **Internal recognition within the workshop is social, immediate, and tangible** — a shared moment when a robot moves, a visible checkmark on a navigation card, a peer noticing the work — rather than bureaucratic and deferred. The rationale is NOT that token economies are bad for this population. Phase C citation re-verification established that the research the workshop draws on actually *supports* token economies in classroom settings for students with ODD and ADHD. **Barker & de Lugt (2022)** review empirical classroom studies of ODD interventions and include a study by Rosenberg (1986) in their evidence table showing a token economy produced M PND = 82% for on-task behavior (with rule reminders) and M PND = 91% for reducing disruptive behavior; Barker & de Lugt's own synthesis concludes that "each of these studies indicated a reduction in disruptive behaviour when these approaches and strategies were implemented," listing token economies among the effective interventions. **Morsink et al. (2022)** review two studies that explicitly tested whether rewards undermine intrinsic motivation in children with ADHD — Carlson et al. (2000) and Carlson & Tamm (2000) — and report that *neither* study found an undermining effect. (An earlier draft of this principle cited Barker and Morsink as opposing token economies. That was a Phase B misreading, caught and re-verified in Phase C. See Editorial_Preferences_Log.md Pattern 10 for the process lesson.) The workshop's choice to use social/immediate/tangible recognition is instead grounded in three workshop-specific fits: **(a)** hardware-based milestones are already inherently tangible — a motor spinning is its own reward signal — so layering a token on top adds little; **(b)** a small-group, rotating-teacher setting has the capacity for immediate personal acknowledgment in a way that larger classrooms may not; **(c)** at Agourim, a school-wide token economy is already operating across most aspects of daily school activity, and the workshop continues to operate within that school-wide system rather than adding a second parallel workshop-level token layer. The within-workshop recognition mechanism described here operates alongside the school's broader token economy, not instead of it.
- **Project order is not a rigid gate.** Prerequisites are skills, not sequence positions. Students may work on the eight projects in any order; when a student skips ahead, the teacher delivers missing prerequisite skills just-in-time via short targeted mini-modules rather than blocking the student at the doorway of the desired project. A student's refusal to do a specific project on a specific day is diagnostic, not defiant — the teacher's first response is "tell me what would make today worth your time," and the conversation itself is the intervention.
- **Population profile sub-rules:**
  - For **OCD** students: private workspace by default; never forced public demo; navigation cards with clear "done when" criteria to prevent perfectionism spirals; flexible timing with no "you must finish this before X." These design choices are inferred from the documented burden of pediatric OCD — Abramovitch et al. (2024) report that approximately 90% of affected children experience impairment in at least one domain, with school as the most-affected domain — and from Colbert et al.'s (2025) finding that school-staff knowledge of OCD-specific accommodations is limited. Neither paper prescribes these specific workshop design choices directly; they document the problem our design is trying to address. (Earlier drafts of this sub-rule cited Abramovitch and Colbert as if the papers prescribed these accommodations. That was a Phase B misattribution, corrected in Phase C.)
  - For **anxiety without trauma**: scaffold approaches to feared tasks rather than permanent avoidance accommodation. Håland & Bertelsen (2025) document that teacher accommodations correlate with increased student avoidance and anxiety severity, and warn that accommodations "can inadvertently intensify or prolong the anxiety over time" when they interfere with exposure-based treatment principles. Their finding is correlational, not a causal demonstration that short-term accommodation worsens long-term outcomes, but it is strong enough to make long-term avoidance accommodations a design concern worth naming.
  - For **anxiety with trauma history**: safety and predictability first; no forced exposure; use Principle 1 (predictable routine) as the anxiety management mechanism, not exposure (Watson & Astor 2025; Koslouski et al. 2023; Asselman et al. 2025 on trauma/EF mediation).
  - For **ODD**: frame tasks as choices or requests, never commands. "When you're ready, your next card is here."
  - For **depression**: smallest possible first step; visible tangible results; celebrate micro-progress privately.

---

### Principle 6 — Movement is medicine for ADHD (not a reward, not a release valve)

**Statement.** Every session includes a structured movement break. This is not an "optional energy release" for students who "can't sit still" — it is a first-class intervention with the largest effect sizes in the ADHD literature for exactly the deficits this population has.

**Evidence.** Qiu, Liang, Wang, Zhang & Shum (2023, *Asian Journal of Psychiatry*) meta-analysis of 67 non-pharmacological EF intervention studies for ADHD found **physical exercise produced the largest effect sizes of all intervention types**: g = 0.900 on inhibitory control and **g = 1.377 on cognitive flexibility**. For comparison, cognitive training produced g = 0.907 on working memory; EF-specific curriculum g = 0.532 on planning. Physical exercise is not just competitive with other interventions — it's the best single intervention measured for ADHD executive function. Cumming et al. (2024, both papers) independently shows that EF (especially cognitive flexibility) degrades under stress, and movement is a direct stress intervention.

**Design rule for the Arduino projects.**
- The workshop session structure from [Robotics_Workshop_DI_PBL_Framework.md](Robotics_Workshop_DI_PBL_Framework.md) Part 1 includes a 3–5 minute Movement Break between Work Block 1 and Work Block 2. This break is **non-negotiable and applies to every session**, even when a student is in flow state. ("Especially when a student is in flow state — the break protects the next hour's flow.")
- Movement breaks are structured, not free-for-all: stand up, get water, walk around the room once, stretch for 30 seconds. Structured because unstructured breaks spike dysregulation for students with ODD or trauma.
- Kinesthetic elements are embedded in navigation cards where possible: "Walk to the parts bin and get a 220Ω resistor" is better than "reach for the resistor." Test steps involve standing up: "Stand up, hold the drone, and spin the propeller with your finger — does it turn freely?"

---

### Principle 7 — Claude Code as a differentiated coding support AND a scaffolded tutorial channel

**Statement.** Claude Code serves two distinct roles in the workshop, and both are differentiated so that every student meets the AI at the level that is actually approachable for them today. The first role is **Claude Code as pair programmer** (Channel A) — a coding collaborator the student directs when writing, modifying, or debugging a sketch, implemented as a three-level access model. The second role is **Claude Code as scaffolded tutorial** (Channel B) — a conversational walk-through of a navigation card for students who prefer to receive instructions by voice-and-text dialogue rather than reading a printed card silently. Both channels sit alongside the printed navigation card; neither replaces it. Both channels enforce the same core discipline: the student describes what they are working on before the AI responds. Across both channels, the AI is a scaffold the student uses, not an obstacle the student has to overcome alone.

**Why two channels.** A single "Claude Code is a coding AI" role misses the fact that these students also need *reading* and *instruction-parsing* support, not only coding support. A student who can happily build a circuit but struggles to read a dense navigation card on their own benefits enormously from having the same content delivered conversationally. A student who freezes at a blank code editor needs a pair-programmer channel whose first move is to hand them a pre-written sketch. The two channels address two different entry points into the workshop's material, and treating them as separate lets the program differentiate each channel independently.

**Channel A — Pair programmer (three levels).**
- **Level 1 — Pre-written sketch upload.** Student opens a pre-prepared `.ino`, clicks Upload, hardware responds. Coding is not yet a barrier because the student is not yet being asked to code.
- **Level 2 — Modify with Claude Code's help.** Student opens a partially-complete sketch, makes one small targeted change with prompt-scaffold support, tests it, and sees the result.
- **Level 3 — Free dialogue.** Student describes what they are trying to build, shows Claude Code their current attempt, and iterates. Discipline: the student fills in "(a) what I want to happen, (b) what's currently happening, (c) what I've tried" before sending the first prompt.
- Students move fluidly between levels in both directions, including downward. A student having a hard day drops from Level 3 to Level 1 for a session and returns to Level 3 next week without shame.

**Channel B — Scaffolded tutorial (conversational walk-through).**
- A student opens Claude Code and says: *"I'm on Project 3, Tier 2, navigation card 4 — walk me through it."* Claude Code, primed by the project's tutorial-channel scaffold, responds with the card's content in conversational form, breaks it into small steps, and asks follow-up questions at each checkpoint.
- **Available at any tier, including Tier 1.** Channel B is cognitively simpler than Channel A Level 3 because the interaction is receptive (Claude leads, the student confirms), not productive (the student has to describe a coding problem). A Tier 1 student who is not yet ready for code-level AI dialogue can still use Channel B.
- **Does not replace the printed card.** The student still holds the physical card, still checks off milestones on the physical card, and the teacher can still see the same card during rotation check-ins. The two formats run in parallel.
- **"Describe the problem first" discipline still applies.** If a student is stuck, Channel B asks what they are stuck on and what they have tried before offering a next step. A student using Channel B is directing a walk-through, not passively consuming instructions.
- **Primarily addresses reading load, not coding support.** A student who reads below grade level, who is overwhelmed by dense printed instructions, or who simply processes information better through back-and-forth dialogue benefits most from Channel B.

**Evidence.** This principle has **no direct empirical support in the verified corpus** — zero studies in the 65 full-text articles examine Claude Code, conversational AI tutors, or AI-paired learning for neurodivergent students. The principle rests on **responsible inference** from three adjacent bodies of evidence, and Channel B has even less direct support than Channel A (it is a novel application of the same "AI as external scaffold" logic to instruction-parsing rather than code-writing):

1. Rosen, Boyle, Cariss & Forchelli (2014) on scaffolded EF: external cognitive scaffolds enable students to practice EF they don't yet have. Both pre-written code (Channel A Level 1) and a conversational tutorial walk-through (Channel B) are external cognitive scaffolds; which one a student needs depends on whether the barrier is code-related or reading-related.
2. Morsink et al. (2022) applying self-determination theory to motivation in ADHD adolescents: the SDT framework distinguishes extrinsic from intrinsic motivation. This program *infers from that framework* (not from Morsink's own findings, which do not address AI tutoring) that an AI dispensing answers on demand would function more like extrinsic reward, whereas an AI asking questions back and requiring the student to describe the problem first preserves student agency more in line with intrinsic-motivation support. This is why both channels enforce a "describe first" discipline, and why requiring AI dialogue from a student who is not ready for it (the failure mode Channel A Level 1 exists to prevent) would also undermine competence-building.
3. Smith, Langberg, Cusick, Green & Becker (2020) on adolescent ADHD motivation: higher extrinsic academic motivation was associated with better homework and GPA outcomes in adolescents with ADHD. The program infers from this (as a design inference, not as the paper's own recommendation) that structured external support can help academic outcomes for this population, provided the structure is scaffolding the student's own work rather than replacing it. Pre-written code and conversational walk-throughs both structure the experience; neither replaces the student's work on everything else in the project (wiring, testing, debugging the circuit, making choices about what to build next).

**Honest caveat:** This principle is the weakest-supported in the list and is flagged explicitly in the Honest Limitations section of the master document. Both channels are piloted practices, not evidence-based interventions. The three-level differentiated Channel A has no direct precedent in published research; the Channel B tutorial-channel role has even less. Both are the program's own design responses to the heterogeneity of the student population, grounded in adjacent evidence but not directly empirically tested. A reviewer who asks *"where is the research that shows this works?"* gets an honest answer: it doesn't exist yet; we are piloting carefully; the design is inferentially grounded; the practice will be evaluated in use.

**Design rule for the Arduino projects.**
- **Channel A — Pair programmer:**
  - Every project provides all three Channel A levels explicitly: a **pre-written sketch** (Level 1) that students upload as-is; a **partially-filled sketch with guided modification targets** (Level 2) with Claude Code prompt scaffolds for specific small changes; **open-ended prompt templates** (Level 3) for students ready to describe new ideas and iterate.
  - Task cards for each milestone indicate what Level 1 / 2 / 3 looks like at that step.
  - At Level 2 and Level 3, students describe the problem before asking for help: "Before asking Claude, fill in: (a) what you want to happen, (b) what's currently happening, (c) what you've tried."
  - At Level 2 and Level 3, a quick comprehension check follows any AI interaction: "After Claude helps you, can you explain in one sentence what changed?" At Level 1, the check is softer: "What does your device do right now that it did not do before you uploaded the code?"
  - Students can move up (Level 1 → 2 → 3) and back down without shame.
  - For Project 8 (quadcopter), the `TinyQuadcopter.ino` file in the source material is currently an empty stub and the real firmware lives as pseudocode in the README. This is a feature of the three-level model: **Level 1** students upload a simpler pre-written motor-test sketch that proves the electronics work (no stabilization), and **Level 2/3** students use Claude Code to generate the full PID-stabilized `.ino` from the README pseudocode. Even within the most complex project in the program, the three-level model applies.
- **Channel B — Scaffolded tutorial:**
  - Every project ships with a **Claude Code tutorial-channel scaffold** — a short system prompt plus per-milestone invocation templates — stored alongside the printed cards and the HTML tutorial.
  - A student invokes Channel B by telling Claude Code their project, tier, and card number. Claude walks them through the card conversationally with checkpoint questions.
  - Channel B is available to students at **any tier**, including Tier 1.
  - The printed navigation card remains the physical anchor; Channel B supplements but never replaces it. The student still checks off each milestone on the printed card.
  - The setup checklist notes which students are currently using Channel B so that rotation check-ins can reference the walk-through conversation as well as the printed card.

---

### Principle 8 — The relationship is the multiplier

**Statement.** Structure alone does not work. Structure combined with a trustworthy adult presence works. The **teacher–student relationship** is the relational mechanism this program commits to as its first-class infrastructure: consistent adult presence, relational check-ins before task progress, greeting by name, listening without problem-solving, and the visible, formal support that comes from a named adult who knows what each student is working on. The relationship is the soil in which independent work grows, and the program's version of that soil is the teacher's attention. **Peer collaboration is not a first-class mechanism in this version of the program** — every student works on their own project at their own workstation, and the appendix in the master document on deferred peer collaboration explains what the program does not yet do and why.

**Evidence.** Gersib & Mason (2023) meta-analysis of behavior interventions in self-contained EBD classrooms: effects were large overall (g = 0.93, SE = 0.16), with **relational components as the strongest moderator** (B = 1.26, SE = 0.15, p < .05). Gersib & Mason's relational components include parent communication, peer support, and adult mentoring — this program's version of "relational components" is specifically the **adult mentoring** component (teacher rotation with relational check-ins, consistent caring adult presence in every session, Arrival and Close-Out rituals). The program does not claim Gersib's full moderator effect for itself — we are implementing one of the three components the moderator describes, and it is honest to say so. Gage, Kramer II & Ellis (2021, *Journal of Disability Policy Studies*) analyzing 350,000+ high-school students, including 5,000+ with/at-risk-for EBD, found that **EBD students with IEP services perceived more positive climates than EBD students without IEP services** — formal, visible adult support improves sense of belonging, which is specifically the mechanism this principle relies on. Koslouski, Stark & Chafouleas (2023) and Asselman et al. (2025) on trauma-informed environments emphasize relationship quality, trust, and adult co-regulation as the mechanism through which students develop resilience and self-regulation. Gomez (2019) UTSA dissertation on makerspace learning for EBD — the closest analog in the corpus to the Arduino workshop — found that makerspace participation supported social-emotional skill development, but Gomez's mechanism was **peer interaction** during makerspace work, which is specifically a mechanism this program does not implement as a default. This is a genuine gap between Gomez's finding and the program's current design, and the master document's §9 Honest Limitations restates it.

**Design rule for the Arduino projects.**
- Workshop sessions open with Arrival & Board Check (greet each student by name, brief 1-word check-in) and close with a Close-Out Circle (each student says one thing they worked on or got stuck on). These are not optional social filler — they are the relationship infrastructure Principle 8 rests on.
- Teacher rotation during work blocks includes relational check-ins, not just task progress: "How are you doing with this?" before "Where are you on the card?" A 5-second relational check-in signals to the student that the teacher sees them as a person first, which is the trust infrastructure on which all task work rests.
- The teacher knows each student's current project, current tier, current navigation card, and recent history — and shows that knowledge in the first sentence of every rotation. *"Last session you got the LED to blink — how did that feel?"* is a teacher move the program asks for explicitly.
- **Every student works on their own project, at their own workstation, at their own tier, at their own pace.** The workshop is a small-group physical setting (three to eight students in the same room, sharing a parts library and tools) but the work is individual. Peer collaboration is NOT a first-class mechanism in this version of the program. The master document's appendix on deferred peer collaboration explains the reasoning and the conditions under which a future version of the program would revisit this decision.
- **Trust accumulates across sessions.** A student who had a hard day last week gets the same greeting this week. A student who refused a project last session gets the same friendly opening line at next session's Arrival phase. The relationship is durable across hard sessions, not contingent on the student having a good day.

---

### Principle 9 — Teacher sustainability is a first-class design constraint

**Statement.** The curriculum must be designed so one teacher managing 3–8 EBD students can run a session without burning out. Pre-prepared materials. Self-directed navigation cards. Laminated reference sheets. Clear session structure. Predictable rhythms. If the teacher is exhausted, the whole system fails — student outcomes collapse first.

**Evidence.** Gilmour, Sandilos, Pilny, Schwartz & Wehby (2022, *Journal of Emotional and Behavioral Disorders*) used latent profile analysis to identify three teacher burnout profiles when teaching EBD students — flourishing, buffered, struggling — and showed that **burnout profile predicts observed classroom management quality**: struggling teachers used fewer effective strategies and gave less autonomy to students. Burnout is not just a teacher-welfare issue; it directly harms student outcomes. Taylor et al. (2024) uniquely measured teacher job satisfaction as a PBL outcome and showed it **improved** post-intervention: well-designed PBL can actually reduce teacher burden in EBD contexts by shifting the teacher from crisis-manager to facilitator. Koslouski et al. (2023) explicitly addresses secondary traumatic stress in educators and calls educator well-being "crucial to remaining healthy and effective" when working with traumatized students. Asselman et al. (2025) and Gilmour et al. (2022) converge: supporting teacher emotional resilience is not optional — it is necessary for student outcomes.

**Design rule for the Arduino projects.**
- Every project ships with **pre-prepared teacher materials**: printed navigation cards ready to laminate, a setup checklist for before students arrive, a rotation plan suggesting which students to start with, a troubleshooting crib sheet.
- No prep work should require the teacher to write from scratch during a session.
- Projects are scoped so they can be run the first time by a teacher who has read the master document once — no additional training required. (Colbert et al. 2025 on brief written materials outperforming long workshops directly supports this.)
- The session structure (Principle 1) IS a teacher-sustainability mechanism — predictable rhythms reduce the cognitive load of deciding what happens next.
- The Claude Code prompt scaffolds (Principle 7) are also a teacher-sustainability mechanism — the teacher is not the only debugging resource in the room.
- Ministry proposal implication: the program should include budget for teacher release time, peer co-facilitation, and a lightweight check-in protocol between sessions — not a heavy training/coaching apparatus.

---

### Principle 10 — Flexibility in defining ways of participation

**Statement.** Participation is not one shape. A student can participate **actively** (engages with the card and the session as designed), **passively** (physically present in the workshop space but not executing tasks independently), or **separately** (outside the shared activity — in an adjacent space, at a different table, seemingly disengaged, or absent from this session and working from home). All three are legitimate. The workshop's job is to see the participation style the student is offering today, legitimize it, and build from it — not to push every student toward the active style at every session. Belonging and a sense of having value are existential needs; a student who is not in the "active" zone still needs to feel like a participant, and making that possible is a first-class design concern.

**Evidence.** **Primary source:** a staff lecture at Agourim school (Michal & Smadar, 2025) on flexibility in participation styles, grounded in several years of clinical practice with the same EBD student population this workshop serves. The lecture presented two case examples that anchor the principle: (a) a seventh-grade student who could not sit in class but completed advanced English assignments on a hallway sofa; staff reframed the sofa from "leaving class" to "her working anchor," coordinated two structured acknowledgments per day, and over weeks she moved from war-of-attrition dynamics to sustained engagement; (b) a seventh-grade student with severe morning dysregulation who was given scheduled rest (sleep) for the first two hours of each school day, after which he could participate meaningfully for the rest of the day. In both cases, the staff's first move was to stop pushing for "active" participation and instead build around the student's actual capacity, which became a bridge rather than a concession.

**This principle has no direct support in the verified 65-article corpus.** It is grounded in the clinical practice of the school's educational/therapeutic staff, not in the research base the other nine principles rest on. It is most closely aligned with three of those nine:
- **Principle 5 (structured autonomy, not forced compliance)** — the subrule "a student's refusal to engage with a specific project on a specific day is diagnostic, not defiant" is an early articulation of the same idea that Principle 10 makes explicit and extends beyond project-level refusal into session-level and moment-level participation style.
- **Principle 8 (the relationship is the multiplier)** — the mechanism through which separate-style participation can become meaningful is the sustained adult presence Principle 8 commits to. Principle 10 specifies *what the adult is doing during sustained presence with a separate-style student*: seeing the anchor, naming it, legitimizing it, acknowledging it structurally.
- **Principle 2 (the navigation card traces the path)** — the card's authority does not depend on the student being "active"; a student working from a hallway sofa or a beanbag corner can still follow a navigation card. Principle 10 removes the implicit assumption that "following the card" looks the same for every student.

**Honest caveat:** This principle is the newest in the list, rests on clinical rather than empirical grounding, and is flagged explicitly in the master document's Honest Limitations section. The per-student accommodations it recommends (anchor logs, structured acknowledgment scripts, co-planning conversations, regression playbooks) are piloted practices, not evidence-based interventions.

**Design rule for the Arduino projects.**
- **Name the three participation styles** (active / passive in space / passive adjacent / separate in room / separate at home) as a vocabulary the staff team uses when discussing a specific student. The language itself is a design intervention — it displaces "not cooperating" and "no motivation" with descriptions of capacity and style.
- **No card or teacher-side document uses "not cooperating," "doesn't want to," "refuses," "lazy," or the Hebrew equivalents** (`לא משתף פעולה`, `לא רוצה`, `מתעצל`, `אין מוטיבציה`, `מלחמת התשה`, `אין סבלנות`, `אין התקדמות`). Substitutions: describe the capacity limit ("it is hard for her to sit in class for long"), name what the student is actually doing ("she is asking for help in the way she has"), or point to the anchor ("she is working on English from the sofa").
- **Every workshop-participating student has a Per-student Anchor & Accommodation Log** (see [teacher_materials/student_anchor_log.html](Arduino_Projects/Project_1_Light_Signals/teacher_materials/student_anchor_log.html) and the Hebrew version). The log records the student's current participation style, identified anchors, co-planned accommodations, and a structured acknowledgment script. The log is filled in through observation and through co-planning conversations with the student — not written at them.
- **Acknowledgments are structured, not spontaneous.** A prepared short sentence, delivered at a decided frequency, by a decided person, at a decided moment, without lingering or inspecting — see [teacher_materials/acknowledgment_scripts.html](Arduino_Projects/Project_1_Light_Signals/teacher_materials/acknowledgment_scripts.html). The dose matters: too few and it is invisible; too many (every adult who passes by) and it becomes overwhelming and loses meaning.
- **Co-plan accommodations with the student using the principle of delay.** Ask, listen, do not answer yes/no on the spot. Collect the student's ideas. Come back with the staff team's response the next day or the next session. Prepare questions and candidate options in case the student offers nothing the first time.
- **Wave motion is expected, not an emergency.** Progress is non-linear; regressions return even after breakthroughs; accumulated effort does not disappear when a student has a hard week. The staff-side response to a regression is to consult the anchor log and return to the known-good anchors, not to treat regression as failure of the program.
- **Environmental adaptation is legitimization, not concession.** A beanbag corner, an alternative seat with back to the board, a personal work area outside the main group, a scheduled rest slot, a day-off arrangement — each of these becomes a bridge to sustained participation when named and legitimized, and a source of conflict when framed as "special treatment" or "we gave in."
- **Tier movement downward carries no shame** (Principle 5 already says this for tier movement; Principle 10 extends it to participation style movement within a session — a student who was active last session and is separate this session is still a participant, and the acknowledgment script still applies).

---

## How the principles map to the 8 Arduino projects

**Principle 10 applies across every project and every session** — it is not project-specific; it is the stance the workshop takes toward every student regardless of which project they are on. The table below lists project-specific principle loads for Principles 1–9; Principle 10 is assumed throughout.

| # | Project | Primary principles this project demonstrates |
|---|---------|---------------------------------------------|
| 1 | Light Signals | 1, 2, 3, 4, 5, 6, 7 (all except relationships — mostly individual work) |
| 2 | Reaction-Time Game | 1, 2, 3, 4, 5, 6, 7, 8 (pair play introduces relational element) |
| 3 | Don't Get Too Close | 1, 2, 3, 4, 5, 6, 7 |
| 4 | Line-Following Car | 1, 2, 3, 4, 5, 6, 7, 8 (pair build) — soldering prerequisite introduced |
| 5 | Remote-Controlled Car | 1, 2, 3, 4, 5, 6, 7, 8 |
| 6 | ESP32 Wi-Fi Controller | 1, 2, 3, 4, 5, 6, 7, 8 — I2C prerequisite for Project 8 introduced |
| 7 | Camera-Equipped Explorer | 1, 2, 3, 4, 5, 6, 7, 8 |
| 8 | Tiny ESP32 Quadcopter (8.5×20mm) | **Principles 1–9 all load-bearing simultaneously** (plus 10 as always). Routine protects EF under the stress of first flight; navigation cards handle the fine-motor wiring steps; physical-first wiring before firmware; hyper-chunked safety protocol; structured autonomy in flight sequences; movement breaks between high-focus tuning sessions; Claude Code generates the firmware from the README pseudocode; peer collaboration during build, strict one-at-a-time during flight; teacher sustainability protected by pre-assembled Tier-1 cores and a dedicated safety checklist. |

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
