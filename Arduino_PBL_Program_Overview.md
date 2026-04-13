# A Differentiated Project-Based Learning Program for Students with Emotional and Behavioural Challenges in the Robotics Workshop at Agourim School

## Program Overview for Agourim School, Grades 7–12

---

## Why this program exists

This program was born from two difficulties I cope with as a workshop teacher at Agourim School.

The first is **the rotation difficulty.** In a robotics workshop with 3–8 students, each working on a different project at a different pace, I found myself running between workstations and often failing to give each student the help they needed. By the time I reached one student, another had been waiting too long and had disengaged. The workshop was designed for individual work, but I as the teacher had become a bottleneck in the flow of the activity.

The second is **the overwhelm difficulty.** The workshop had a rich inventory of materials — Arduino boards, motors, sensors, chassis kits, cameras, soldering equipment, Lego robotics kits, computers, tools, and more — and students were free to choose what to build. I expected this freedom to be motivating. Instead, for many students, the large variety and the open-ended choice led to overwhelm, fear, and avoidance. Students who already struggled with decision-making and self-regulation froze in front of too many options. I understood that I needed to bring structure to the workshop: structure that would make the available equipment accessible rather than paralyzing, and that would allow students to work independently so that the teacher could support without becoming a bottleneck.

This program is the result. It turns the open workshop into a structured progression of eight projects, each built around three differentiated versions (a choice element) with printed and online navigation cards that guide students step-by-step, supported by an AI coding assistant that provides immediate help when the teacher is with another student.

## What this program is

An eight-project Arduino and ESP32 workshop program designed for 3–8 students per cohort in grades 7–12 with emotional and behavioural challenges (ADHD, oppositional defiant disorder, anxiety, depression, OCD, post-trauma, and others). Students progress from a first-session LED circuit through a student-built tiny quadcopter, working individually at their own pace and version, with a solo teacher (sometimes with an additional instructional assistant) rotating between workstations.

The program combines three ingredients: **differentiated instruction** with three readiness versions per project; **hands-on physical computing** that produces visible, tangible results every 15 minutes; and **Claude Code** (an AI coding assistant) integrated as both a pair-programming collaborator and a conversational tutorial channel.

The design rests on **nine research-grounded principles** distilled from 77 verified peer-reviewed sources. The full research document, per-project files, student-facing materials (in Hebrew and English), and a reproducible build pipeline are available in the project repository.

---

## The population

The Agourim student body is defined by heterogeneity across every dimension — reading level, home context, prior technology experience, social comfort, diagnostic profile. Students commonly carry diagnoses of ADHD, ODD, anxiety, depression, OCD, or post-trauma, often multiple concurrently (and others too). What nearly all share is a sense that school has been a place where they fail, or where they are failed.

This program responds to the student in front of the teacher, not to the label on a file. The **super-target** is the creation of small, positive, empowering learning experiences for students whose confidence in school has been damaged.

---

## What research grounds this program

The program rests on four threads of evidence, each attached to the design choices it informs.

**Differentiated instruction in secondary education.** The strongest meta-analytic evidence comes from Smale-Jacobse et al. (2019), which found achievement effects of d = 0.509–0.741 when DI is implemented as adaptation of process, product, and assessment to student readiness — not as tracking or as a single extension task. The available evidence base in secondary settings is modest (twelve unique studies), so the effect size is directional rather than definitive. This thread grounds the three-tier structure at the heart of every project.

**Scaffolded project-based and inquiry learning in STEM.** Belland et al. (2017), a meta-analysis of computer-based scaffolding in STEM, reports an overall effect of g = 0.46, with scaffolding producing directionally stronger effects in project-based learning contexts than in problem-based learning, and significantly larger effects for underperforming students than for their traditional peers. This thread grounds the card-mediated workflow, the 15-minute milestone chunks, and the decision to make AI (Claude Code) part of the scaffold rather than a separate channel.

**Emotional-behavioural population and technology-mediated instruction.** Robotics-in-special-education studies (Berrezueta-Guzmán et al. 2021; Cibrian et al. 2022) show that structured, hands-on technological work sustains attention and task completion in children with ADHD by providing non-threatening feedback from a non-human source. We describe this informally as a "non-human mediator" effect — cards and AI as the authority, the teacher as the relational anchor — aggregating across studies rather than citing a unified synthesis.

**Universal Design for Learning.** Almeqdad et al. (2023) summarise the UDL evidence base on reducing access barriers by designing multiple means of representation, engagement, and expression into the material up front rather than retrofitting accommodations. This thread grounds the dual print + HTML delivery, Claude Code's dual-channel role (pair programmer + conversational tutorial), and the three-tier differentiation — the same milestone in three entry points.

**Honest caveat.** No single randomised controlled trial combines all four threads with Arduino hardware and an AI pair programmer in an EBD secondary classroom. The program is research-*grounded*, not research-*proven*. Section "What this program is — and is not" below carries this limitation forward explicitly.

---

## The 9 design principles

Every design decision in the program traces to one or more of these nine research-grounded principles. Each principle states a rule, names its strongest evidence, and describes what it looks like in practice.

### Principle 1 — Predictable routine is load-bearing

Every session follows an identical seven-phase structure. No surprises without announcement. Routine protects executive function from stress-collapse and lets students work with minimum anxiety.

*Evidence: Cumming et al. (2024) — stress degrades EF (β ≈ .61–.65); Harrison et al. (2019) — instructional interventions meeting WWC standards.*

### Principle 2 — The navigation card traces the path

Laminated visual navigation cards guide students step-by-step. The teacher rotates and supports but never gives verbal multi-step instructions. This bypasses power-struggle dynamics common in ODD profiles and reduces working-memory load.

*Evidence: Barker & de Lugt (2022) — environmental modifications for ODD; Thomas & Karuppali (2022) — visual schedules reduce task-initiation latency.*

### Principle 3 — Physical-first, then abstract

Students build the wiring before writing the code. The concrete → representational → abstract sequence is not optional for students with learning difficulties. Every project begins with a hardware-only milestone before any code upload.

*Evidence: Hwang & Taylor (2016) — CRA as prerequisite for students with disabilities; Belland et al. (2017) — meta-analysis showing g = 0.46 overall, with larger effects for underperforming students.*

### Principle 4 — Hyper-chunked 15-minute milestones with visible wins

Every navigation card maps to ≤ 15 minutes and produces an observable result ("the LED blinks," "the motor turns"). No silent work periods longer than that. This is the engagement mechanism for ADHD attention profiles.

*Evidence: Taylor et al. (2024) — very large on-task effect sizes (BC-SMD 95% CI [1.70, 3.81]) with frequent visible milestones; Cibrian et al. (2022) — hands-on tangible feedback as core ADHD mechanism.*

### Principle 5 — Structured autonomy, not forced compliance

Every project offers at least one genuine choice point, even at the most guided version. Choice reduces oppositional resistance. External structure enables autonomy rather than undermining it.

*Evidence: Taylor et al. (2024) — student voice as essential quality element; Morsink et al. (2022) — no undermining effect of external rewards on intrinsic motivation in ADHD.*

### Principle 6 — Movement is medicine for ADHD

A structured 3-minute movement break between work segments is non-negotiable — not a reward, not a release valve, but a first-class intervention with the largest effect sizes in the ADHD executive-function literature.

*Evidence: Qiu et al. (2023) — meta-analysis of 67 EF intervention studies: physical exercise produced g = 0.900 on inhibitory control, g = 1.377 on cognitive flexibility.*

### Principle 7 — Claude Code as dual-channel coding support

Claude Code serves two roles. **Channel A** is a pair programmer in three versions (upload pre-written code / modify code with AI help / free dialogue). **Channel B** is a conversational tutorial that walks students through navigation cards in small chunks with checkpoint questions. Both scaffold; neither replaces the teacher or the navigation card.

*Evidence: Rosen et al. (2014) — external scaffolds enabling EF practice. Caveat: no direct empirical research exists for AI-paired coding with neurodivergent learners. This is the program's most evidence-thin component; it is flagged as a piloted practice, not an evidence-based one.*

### Principle 8 — The relationship is the multiplier

Structure alone does not work. The teacher–student relationship is first-class infrastructure: greeting by name, relational check-in before task-progress check, consistent presence. The relationship is the soil in which independent work grows.

*Evidence: Gersib & Mason (2023) — meta-analysis of EBD behaviour interventions (g = 0.93 overall) with relational components as strongest moderator (B = 1.26, p < .05); Sciacca (2025) — trust-building as first and most pervasive theme.*

### Principle 9 — Teacher sustainability is a first-class design constraint

The program must be runnable by one teacher managing 3–8 students without burnout. Pre-prepared materials, navigation-card discipline, and predictable session rhythms are non-negotiable. If the teacher experiences significant burnout as a result of the program, this is a red flag requiring re-examination of the design.

*Evidence: Gilmour et al. (2022) — teacher burnout profile linked to classroom management quality; Sciacca (2025) — "the kids drive so much more of their own learning" (teacher S.F.).*

---

## The 8 projects

Students progress through projects in the order shown below, but the sequence is a suggestion, not a requirement. Choice within the structure is a built-in element of the program. However, handling refusal to the prescribed order is a complex challenge: there is an inherent tension between offering choice and encouraging the student to engage with order and structure, and it is not always possible to fill the prerequisite skills gaps needed for jumping ahead immediately. The teacher must balance the two according to what is possible in the moment and according to familiarity with the student's individual path. Each project introduces new hardware and new skills. The three versions within each project provide differentiation by readiness:

- **Version 1 (Guided Build)** — Step-by-step navigation cards with pre-written code. The student follows instructions and builds.
- **Version 2 (Guided Design)** — The student makes 2–3 design choices and modifies code with Claude Code's help.
- **Version 3 (Open Design)** — The student designs their own version of the project from scratch.

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
| **Work Segment 1** | **15** | Independent work on navigation card. Teacher rotates (~3 min/student). |
| Movement Break | 3 | Everyone stands, walks, stretches. Non-negotiable. |
| **Work Segment 2** | **15** | Continue project work. Teacher finishes rotations. |
| Clean-Up | 3 | Tools away, workspace tidy, navigation card returned. |
| Close-Out Circle | 3 | Each student says one thing they worked on or got stuck on. |

**30 minutes of actual work time** in two 15-minute segments. The remaining 15 minutes are routine infrastructure that supports the work time.

---

## Budget at a glance (full budget in Appendix 2)

| | Year 1 (setup + all 8 projects) | Year 2 (consumables only) |
|---|---|---|
| **Total for 8-student cohort** | USD 1,753–1,828 | USD 415–505 |
| **Per student** | USD 219–229 | USD 52–63 |

The program's highest-cost single item is Project 8 (quadcopter) at ~USD 65 per drone. The first five projects together cost less than one educational drone kit. All components are sourced from AliExpress with 15–45 day lead time.

**Implementation roadmap.** Year one is a single-cohort pilot. At year's end, three paths: **continue** if the success criteria below are met; **revise and re-pilot** if results are mixed; or **stop and document honestly** if the program is not working. Year-two cost drops to approximately USD 460–560 because most hardware is reusable. The program commits to honest reporting of whichever outcome occurs — a funder will know within one year whether this is worth continuing.

---

## How we will know if it is working

The program uses a simple measurement framework designed to be sustainable for a solo teacher:

- **Per-session tracking sheet** (30 seconds per student per session): three columns — started work within 5 minutes (yes/no), completed at least one milestone checkpoint (yes/no), behavioural incident (yes/no). This is the primary longitudinal data source.
- **Weekly tracking form** (~10 minutes per week): per-student trajectory, cohort observations, Claude Code usage, teacher-burnout indicators.
- **End-of-semester teacher reflection** (15–20 minutes): structured self-assessment of burnout level, relational capacity, and what to revise.

**What the program does NOT measure:** standardized test scores, behavioural rating scales, comparison to a non-workshop control group, or causal claims about durable change outside the workshop. The measurement framework matches the program's honest scope — it tracks in-workshop engagement and task completion, not clinical outcomes.

**The program targets four outcome clusters**:

1. **Positive learning experiences** — the super-target. Students experience moments where "something I did — worked."
2. **Technical skills** — breadboarding, wiring, uploading code, sensor reading, soldering (from Project 4), motor control, Wi-Fi, and integration.
3. **Executive-function practice** — the workshop provides structured opportunities to practice planning, task-initiation, self-regulation, and help-seeking. This is *not* a therapeutic EF-improvement claim; it is a practice-opportunity claim.
4. **Reduced within-workshop refusal and avoidance** — students approach tasks faster, engage with them for longer stretches of time, and ask for help instead of giving up when they get stuck.

---

## What this program is — and is not

**It is** a carefully designed pilot program grounded in 77 verified research sources, structured for a specific population, and honest about what the evidence does and does not support.

**It is not** an evidence-based intervention in the strict research sense. No randomized trial of the full combination (DI + PBL + EBD + Arduino + AI) exists anywhere in the literature I surveyed. The program crosses several evidence gaps openly:

- No research on Arduino/microcontroller education for EBD/ADHD populations was found.
- No research on aerial robotics for any special-needs population was found.
- The Claude Code integration (Principle 7) is evidence-thin — it is an inference from adjacent scaffolding literature, flagged as a piloted practice.
- The program is designed as a living process: everything in it is a hypothesis, adjustable based on actual experience with actual students.

**Year-one success criteria** include: at least two thirds of students complete at least two projects; engagement and participation improve across the first semester; no safety incidents in the workshop. The teacher does not experience burnout.

**Year-one success does NOT require:** every student completing every project, quantitative comparison to a baseline, or demonstrated transfer of skills outside the workshop.

---

## Appendix 2: Full budget breakdown

*(Full itemized budget to be included here — currently summarized in "Budget at a glance" above. Full line-item breakdown available in the master document §8.)*

---

## References

Almeqdad, Q. I., Alodat, A. M., Alquraan, M. F., Mohaidat, M. A., & Al-Makhzoomy, A. K. (2023). The effectiveness of universal design for learning: A systematic review of the literature and meta-analysis. *Cogent Education, 10*(1). https://doi.org/10.1080/2331186X.2023.2218191

Barker, C., & de Lugt, J. (2022). A review of evidence-based practices to support students with oppositional defiant disorder in classroom settings. *International Journal of Special Education, 37*(1), 85–98. https://internationalsped.com/ijse/article/view/47

Belland, B. R., Walker, A. E., Kim, N. J., & Lefler, M. (2017). Synthesizing results from empirical research on computer-based scaffolding in STEM education: A meta-analysis. *Review of Educational Research, 87*(2), 309–344. https://doi.org/10.3102/0034654316670999

Berrezueta-Guzmán, J., Robles-Bykbaev, V. E., Pau, I., Pesántez-Avilés, F., & Martín-Ruiz, M.-L. (2021). Robotic technologies in ADHD care: Literature review. *IEEE Access, 10*. https://doi.org/10.1109/access.2021.3137082

Cibrian, F. L., Lakes, K. D., Schuck, S. E. B., & Hayes, G. R. (2022). The potential for emerging technologies to support self-regulation in children with ADHD: A literature review. *International Journal of Child-Computer Interaction, 31*, 100421. https://doi.org/10.1016/j.ijcci.2021.100421

Cumming, M. M., Oblath, R., Qiu, Y., Frazier, S. L., Zelazo, P. D., Flores, H., & Park, J. (2024). Executive function, perceived stress, and academic performance among middle schoolers with and without behavior problems. *Remedial and Special Education, 45*(2), 85–100. https://doi.org/10.1177/07419325231176762

Gersib, J. A., & Mason, S. (2023). A meta-analysis of behavior interventions for students with emotional-behavioral disorders in self-contained settings. *Behavioral Disorders*. https://doi.org/10.1177/01987429231160285

Gilmour, A. F., Sandilos, L. E., Pilny, W. V., Schwartz, S., & Wehby, J. H. (2022). Teaching students with emotional/behavioral disorders: Teachers' burnout profiles and classroom management. *Journal of Emotional and Behavioral Disorders*. https://doi.org/10.1177/10634266211020258

Harrison, J. R., Soares, D. A., & Joyce, J. (2019). Inclusion of students with emotional and behavioural disorders in general education settings: A scoping review of research in the US. *International Journal of Inclusive Education, 23*(12), 1258–1277. https://doi.org/10.1080/13603116.2018.1444107

Hwang, J., & Taylor, J. C. (2016). Stemming on STEM: A STEM education framework for students with disabilities. *Journal of Science Education for Students with Disabilities, 19*(1). https://doi.org/10.14448/jsesd.06.00017

Morsink, S., Van der Oord, S., Antrop, I., Danckaerts, M., & Scheres, A. (2022). Studying motivation in ADHD: The role of internal motives and the relevance of self-determination theory. *Journal of Attention Disorders*. https://doi.org/10.1177/10870547211050948

Qiu, H., Liang, X., Wang, P., Zhang, H., & Shum, D. H. K. (2023). Efficacy of non-pharmacological interventions on executive functions in children and adolescents with ADHD: A systematic review and meta-analysis. *Asian Journal of Psychiatry, 87*, 103692. https://doi.org/10.1016/j.ajp.2023.103692

Rosen, S. M., Boyle, J. R., Cariss, K., & Forchelli, G. A. (2014). Changing how we think, changing how we learn: Scaffolding executive function processes for students with learning disabilities. *Learning Disabilities: A Multidisciplinary Journal, 20*(4), 165–176. https://eric.ed.gov/?id=EJ1168865

Sciacca, J. L. (2025). *Experiences of teachers using project-based learning with students with emotional and behavioral disorders* [Doctoral dissertation, Wilkes University]. ProQuest Dissertations & Theses (ID 32170831). https://www.proquest.com/openview/f3284aea35dd8d14dd8429e421c14110/1

Smale-Jacobse, A. E., Meijer, A., Helms-Lorenz, M., & Maulana, R. (2019). Differentiated instruction in secondary education: A systematic review of research evidence. *Frontiers in Psychology, 10*, 2366. https://doi.org/10.3389/fpsyg.2019.02366

Smith, Z. R., Langberg, J. M., Cusick, C. N., Green, C. D., & Becker, S. P. (2020). Academic motivation deficits in adolescents with ADHD and associations with academic functioning. *Journal of Abnormal Child Psychology*. https://doi.org/10.1007/s10802-019-00601-x

Taylor, J. C., Allen, L. M., Van, J., & Moohr, M. (2024). The effects of project-based learning on student behavior and teacher burnout in an emotional/behavioral support classroom. *Journal of Emotional and Behavioral Disorders, 32*(2). https://doi.org/10.1177/10634266241235933

---

# Appendix 1 — Reference Cards and Task Cards (Project 1)

This appendix contains the printable student-facing cards for Project 1 — *Light Signals*:

**Reference Cards (R1–R5):**

- R1 — Wiring Reference
- R2 — Stuck Protocol
- R3 — Claude Code Prompts
- R4 — Safety Reminder
- R5 — Sketch Index

**Task Cards — Version 1 (T1, 8 milestones):**

- T1·M1 — Set Up Your Workspace
- T1·M2 — First Upload
- T1·M3 — Wire First LED
- T1·M4 — Light Up the LED
- T1·M5 — Add a Second LED
- T1·M6 — Alternating Blink
- T1·M7 — Wire a Button
- T1·M8 — Button Control

**Task Cards — Version 2 (T2, 5 milestones):**

- T2·M1 — Startup
- T2·M2 — Pick a Pattern
- T2·M3 — Claude Code Level 2
- T2·M4 — Button Behavior
- T2·M5 — Signature Pattern

**Task Card — Version 3 (T3):**

- T3 — Project Planner

The cards follow on the subsequent pages.
