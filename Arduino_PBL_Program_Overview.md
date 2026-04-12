# Differentiated Arduino Workshop Program for Students with Emotional and Behavioural Challenges

## Program Overview for Agourim School, Grades 7–12

*Yon, Robotics and Programming Teacher, Agourim School, Israel*
*Version 1.0 — April 2026*

---

## Why this program exists

This program was born from two problems I encountered as a workshop teacher.

The first was **the rotation problem.** In a robotics workshop with 3–8 students, each working on a different project at a different pace, I found myself running between workstations and often failing to give each student the help they needed. By the time I reached one student, another had been waiting too long and had disengaged. The workshop was designed for individual work, but the teacher had become a bottleneck.

The second was **the overwhelm problem.** The workshop had a rich inventory of materials — Arduino boards, motors, sensors, chassis kits, cameras, tools — and students were free to choose what to build. I expected this freedom to be motivating. Instead, for many students, the large variety and the open-ended choice were overwhelming and intimidating. Students who already struggled with decision-making and self-regulation froze in front of too many options. I understood that I needed to bring structure to the workshop: structure that would make the available equipment accessible rather than paralyzing, and that would allow students to work independently so that the teacher could rotate without becoming a bottleneck.

This program is the result. It turns the open workshop into a structured progression of eight projects, each with pre-built task cards that guide students step-by-step at three readiness tiers, supported by an AI coding assistant that provides immediate help when the teacher is with another student.

## What this program is

An eight-project Arduino and ESP32 workshop program designed for 3–8 students per cohort in grades 7–12 with emotional and behavioural challenges (ADHD, oppositional defiant disorder, anxiety, depression, OCD, post-trauma). Students progress from a first-session LED circuit through a student-built tiny quadcopter, working individually at their own pace and tier, with a solo teacher rotating between workstations.

The program combines three ingredients: **differentiated instruction** with three readiness tiers per project; **hands-on physical computing** that produces visible, tangible results every 15 minutes; and **Claude Code** (an AI coding assistant) integrated as both a pair-programming collaborator and a conversational tutorial channel.

The design rests on **nine research-grounded principles** distilled from 77 verified peer-reviewed sources. The full research document, per-project files, student-facing materials (in Hebrew and English), and a reproducible build pipeline are available in the project repository.

---

## The population

The Agourim student body is defined by heterogeneity across every dimension — reading level, home context, prior technology experience, social comfort, diagnostic profile. Students commonly carry diagnoses of ADHD, ODD, anxiety, depression, OCD, or post-trauma, often multiple concurrently. What nearly all share is a sense that school has been a place where they fail, or where they are failed.

This program responds to the student in front of the teacher, not to the label on a file. The **super-target** is the creation of small, positive, empowering learning experiences for students whose confidence in school has been damaged.

---

## The 9 design principles

Every design decision in the program traces to one or more of these nine research-grounded principles. Each principle states a rule, names its strongest evidence, and describes what it looks like in practice.

### Principle 1 — Predictable routine is load-bearing

Every session follows an identical seven-phase structure. No surprises without announcement. Routine protects executive function from stress-collapse and lets students work with minimum anxiety.

*Evidence: Cumming et al. (2024) — stress degrades EF (β ≈ .61–.65); Harrison et al. (2019) — instructional interventions meeting WWC standards.*

### Principle 2 — The task card is the boss, not the teacher

Laminated visual task cards guide students step-by-step. The teacher rotates and supports but never gives verbal multi-step instructions. This bypasses power-struggle dynamics common in ODD profiles and reduces working-memory load.

*Evidence: Barker & de Lugt (2022) — environmental modifications for ODD; Thomas & Karuppali (2022) — visual schedules reduce task-initiation latency.*

### Principle 3 — Physical-first, then abstract

Students build the wiring before writing the code. The concrete → representational → abstract sequence is not optional for students with learning difficulties. Every project begins with a hardware-only milestone before any code upload.

*Evidence: Hwang & Taylor (2016) — CRA as prerequisite for students with disabilities; Belland et al. (2017) — meta-analysis showing g = 0.46 overall, with larger effects for underperforming students.*

### Principle 4 — Hyper-chunked 15-minute milestones with visible wins

Every task card maps to ≤ 15 minutes and produces an observable result ("the LED blinks," "the motor turns"). No silent work periods longer than that. This is the engagement mechanism for ADHD attention profiles.

*Evidence: Taylor et al. (2024) — very large on-task effect sizes (BC-SMD 95% CI [1.70, 3.81]) with frequent visible milestones; Cibrian et al. (2022) — hands-on tangible feedback as core ADHD mechanism.*

### Principle 5 — Structured autonomy, not forced compliance

Every project offers at least one genuine choice point, even at the most guided tier. Choice reduces oppositional resistance. External structure enables autonomy rather than undermining it.

*Evidence: Taylor et al. (2024) — student voice as essential quality element; Morsink et al. (2022) — no undermining effect of external rewards on intrinsic motivation in ADHD.*

### Principle 6 — Movement is medicine for ADHD

A structured 3-minute movement break between work blocks is non-negotiable — not a reward, not a release valve, but a first-class intervention with the largest effect sizes in the ADHD executive-function literature.

*Evidence: Qiu et al. (2023) — meta-analysis of 67 EF intervention studies: physical exercise produced g = 0.900 on inhibitory control, g = 1.377 on cognitive flexibility.*

### Principle 7 — Claude Code as dual-channel coding support

Claude Code serves two roles. **Channel A** is a pair programmer at three levels (upload pre-written code / modify code with AI help / free dialogue). **Channel B** is a conversational tutorial that walks students through task cards in small chunks with checkpoint questions. Both scaffold; neither replaces the teacher or the task card.

*Evidence: Rosen et al. (2014) — external scaffolds enabling EF practice. Caveat: no direct empirical research exists for AI-paired coding with neurodivergent learners. This is the program's most evidence-thin component; it is flagged as a piloted practice, not an evidence-based one.*

### Principle 8 — The teacher–student relationship is the multiplier

Structure alone does not work. The teacher–student relationship is first-class infrastructure: greeting by name, relational check-in before task-progress check, consistent presence. The relationship is the soil in which independent work grows.

*Evidence: Gersib & Mason (2023) — meta-analysis of EBD behaviour interventions (g = 0.93 overall) with relational components as strongest moderator (B = 1.26, p < .05); Sciacca (2025) — trust-building as first and most pervasive theme.*

### Principle 9 — Teacher sustainability is a first-class design constraint

The program must be runnable by one teacher managing 3–8 students without burnout. Pre-prepared materials, task-card discipline, and predictable session rhythms are non-negotiable. If the teacher burns out, the program fails regardless of its design quality.

*Evidence: Gilmour et al. (2022) — teacher burnout profile linked to classroom management quality; Sciacca (2025) — "the kids drive so much more of their own learning" (teacher S.F.).*

---

## The 8 projects

Students progress through projects in order. Each project introduces new hardware and new skills. The three tiers within each project provide differentiation by readiness:

- **Tier 1 (Guided Build)** — Step-by-step task cards with pre-written code. The student follows instructions and builds.
- **Tier 2 (Guided Design)** — The student makes 2–3 design choices and modifies code with Claude Code's help.
- **Tier 3 (Open Design)** — The student designs their own version of the project from scratch.

| # | Project | Hardware | New skills | Sessions |
|---|---------|----------|------------|----------|
| 1 | **Light Signals** | Arduino Uno + LEDs + button | Breadboarding, digital I/O, first upload, Claude Code intro | 1–2 |
| 2 | **Reaction-Time Game** | Arduino + LEDs + buzzer + buttons | `millis()` timing, game logic | 2 |
| 3 | **Don't Get Too Close** | Arduino + ultrasonic sensor | Sensor reading, threshold logic | 2 |
| 4 | **Line-Following Car** | Car chassis + IR sensors + motors | **First soldering**, motor control, proportional correction | 3 |
| 5 | **Remote-Controlled Car** | Car chassis + Bluetooth/IR receiver | External input, state machines | 3–4 |
| 6 | **ESP32 Wi-Fi Controller** | ESP32 + I2C sensor + web UI | ESP32 transition, Wi-Fi, I2C, web hosting | 4 |
| 7 | **Camera Explorer** | ESP32-CAM + car chassis + motors | Integration capstone (ground): streaming + control | 5–6 |
| 8 | **Tiny Quadcopter** | Custom ESP32 drone (8.5×20mm motors) | **Apex capstone**: soldering, IMU, PID, flight safety | 6–8 |

**Total program span:** approximately 24–31 sessions across a school year, assuming 45-minute sessions and allowing for setup/review sessions between projects. Not all students will reach Project 8 in year one — and that is by design. The skill progression is cumulative; students arrive at each project with every sub-skill already earned from the ones before it.

---

## How a session works

Every 45-minute session follows the same seven-phase structure:

| Phase | Minutes | What happens |
|-------|---------|-------------|
| Arrival & Board Check | 3 | Greet by name. One-word check-in. Student checks their task board. |
| Mini-Huddle | 3 | Teacher sets expectations for the session. Acknowledge milestones. |
| **Work Block 1** | **15** | Independent work on task card. Teacher rotates (~3 min/student). |
| Movement Break | 3 | Everyone stands, walks, stretches. Non-negotiable. |
| **Work Block 2** | **15** | Continue project work. Teacher finishes rotations. |
| Clean-Up | 3 | Tools away, workspace tidy, task card returned. |
| Close-Out Circle | 3 | Each student says one thing they worked on or got stuck on. |

**30 minutes of actual work time** in two 15-minute blocks — aligned with the hyper-chunked milestone design. The remaining 15 minutes are routine infrastructure that protects the work time.

---

## Budget at a glance

| | Year 1 (setup + all 8 projects) | Year 2 (consumables only) |
|---|---|---|
| **Total for 8-student cohort** | USD 1,753–1,828 | USD 415–505 |
| **Per student** | USD 219–229 | USD 52–63 |

The program's highest-cost single item is Project 8 (quadcopter) at ~USD 65 per drone. The first five projects together cost less than one educational drone kit. All components are sourced from AliExpress with 15–45 day lead time.

---

## What this program is — and is not

**It is** a carefully designed pilot program grounded in 77 verified research sources, structured for a specific population, and honest about what the evidence does and does not support.

**It is not** an evidence-based intervention in the strict sense. No randomized trial of the full combination (DI + PBL + EBD + Arduino + AI) exists anywhere in the literature. The program crosses several evidence gaps openly:

- No research on Arduino/microcontroller education for EBD/ADHD populations was found.
- No research on aerial robotics for any special-needs population was found.
- The Claude Code integration (Principle 7) is the most evidence-thin component — it is a responsible inference from adjacent scaffolding literature, flagged as a piloted practice.
- The program is designed as a living document: everything in it is a hypothesis, adjustable based on actual experience with actual students.

**Year-one success criteria** include: the workshop runs a full year without teacher burnout; at least two thirds of students complete at least two projects; on-task initiation improves across the first semester; no safety incidents on Project 8 if attempted. What year-one success does *not* require: every student completing every project, quantitative comparison to a baseline, or demonstrated transfer of skills outside the workshop.

---

## Appendix: Project 1 student materials (Hebrew)

The complete Hebrew student-facing materials for Project 1 (Light Signals) are attached as a separate packet. These include:

- 5 reference cards (R1 Wiring, R2 Stuck Protocol, R3 Claude Code Prompts, R4 Safety, R5 Sketch Index)
- 8 Tier 1 task cards (guided build, milestones 1–8)
- 5 Tier 2 task cards (guided design, milestones 1–5)
- 1 Tier 3 project planner (open design)
- 1 HTML tutorial (browser-viewable single-page mirror of all task cards)
- 1 Claude Code Channel B scaffold (conversational walk-through scripts)

These materials demonstrate the level of detail, visual design, and Hebrew-language quality of the student-facing artifacts. Equivalent artifact families are planned for Projects 2–8.

---

*Full documentation, source files, and the complete 77-citation research document are available at the project repository. Contact: Yon, Agourim School.*
