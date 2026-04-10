# Arduino PBL — Literature Review Working Notes (Phase A)

*Working synthesis document for the Arduino PBL program for Agourim School. Feeds Phase B (principle distillation) and Phase C (master document literature review section). Based on full-text reading of 65 of 66 verified articles from `articles_full_texts/`, delegated to three parallel Explore agents grouped by theme.*

**Sweep date:** 2026-04-10
**Cluster files (detailed deep-read summaries):**
- [Arduino_LitReview_Cluster1.md](Arduino_LitReview_Cluster1.md) — EBD / ADHD / ODD / OCD population and behavior interventions
- [Arduino_LitReview_Cluster2.md](Arduino_LitReview_Cluster2.md) — Trauma, anxiety, depression, SEL, cooperative learning, CICO
- [Arduino_LitReview_Cluster3.md](Arduino_LitReview_Cluster3.md) — PBL, DI, scaffolding, robotics, STEM, tangible computing, UDL

This document is the **index and synthesis layer**: cross-cluster principles, caveats, gaps, and corrections found during deep reading. The cluster files carry the per-paper summaries with direct quotes.

---

## Phase A completion checklist

- [x] All 65 full-text articles distributed across three Explore subagents and read
- [x] `gomez_2019.txt` audit complete — identified as the Alvaro Gomez (2019) makerspace dissertation, already in Verification_Log as entry #19 (author name now added)
- [x] Drone / aerial-robotics / flight-STEM search across all 78 files — **zero substantive hits**
- [x] Two Verification_Log corrections identified and authoritatively re-verified via ERIC and Crossref — both applied (P2 and P11)
- [x] Cluster 1 synthesis saved
- [x] Cluster 2 synthesis saved
- [x] Cluster 3 synthesis saved
- [x] Cross-cluster principles compiled (below)
- [x] Gaps compiled (below)
- [x] Honest caveats compiled (below)

---

## Cross-cluster candidate design principles

Consolidated from all three clusters. Phase B will select and refine ~6–10 of these as the curriculum's final design principles. Each is citation-backed; expand via the cluster files for primary evidence.

### Executive function, stress, and scaffolding

1. **Stress degrades executive function; predictable routine protects it.** EF is a state that collapses under stress, not a stable trait. Session routines must be identical across sessions, with any change announced in advance. *(Cumming 2024; Koslouski 2023; Watson 2025; Harrison 2019 ADHD)* [Sadin 2022 removed in Phase C re-audit — book, not verifiable]

2. **External cognitive scaffolds bypass working memory and flexibility deficits.** Task cards, visual schedules, reference sheets, and checklists let students access EF without needing intact EF first — and practicing with the scaffold is how EF improves. *(Rosen, Boyle, Cariss, & Forchelli 2014; Cumming 2024; Thomas & Karuppali 2022)*

3. **Embedded, individualized scaffolding beats generic, decontextualized skills training.** Scaffolds must mirror task demands and adapt to individual profiles. *(Rosen et al. 2014; Belland 2017a; Cumming 2024)*

4. **Scaffolding yields larger effects in project-based learning contexts than in problem-based learning; scaffolds do NOT need to be faded.** Belland et al. (2017a) meta-analysis reports an overall effect of g = 0.46, with scaffolding producing directionally stronger effects in PBL than in problem-based learning (z = 6.08, p < .01). Persistent scaffolding works — the field's instinct to "fade supports" is not empirically mandatory. *(Belland 2017a; Boardman & Coleman 2025)* [Phase C re-audit correction: the previous "g = 0.71 vs. g = 0.37" numbers were not found in Belland 2017a full text; g = 0.46 is the actual overall effect, with the directional PBL finding reported as z, not a subset g.]

### Autonomy, choice, and ODD-safe design

5. **Autonomy and choice reduce oppositional behavior and external control resistance.** ODD symptoms occur within relationships — direct reward/punishment is perceived as manipulation. Group contingencies, self-monitoring, and environmental modification work because they reduce adult–child confrontation. The task is "the boss," not the teacher. *(Barker & de Lugt 2022; Billingsley 2018; Taylor 2024; Jones 2018; Kaur 2022)*

6. **Student voice + public product + sustained inquiry yield large on-task effect sizes in EBD settings.** The only empirical PBL-in-EBD study reports BC-SMD ES = 1.70–3.81 on on-task behavior, plus improved teacher job satisfaction. *(Taylor 2024)*

7. **Adolescents with ADHD respond to daily self-rating and student-set goals more than externally-imposed monitoring.** Self-monitoring builds metacognition and motivation. *(Flannery 2024; Kittelman 2024; Del Vecchio 2025; Moohr 2021)*

### Tangible, embodied, physical-first learning

8. **Concrete → Representational → Abstract (CRA) sequence is prerequisite for students with disabilities and ADHD.** They cannot skip the concrete phase. Manipulatives → drawings → symbols/equations. Multi-modal output (build, draw, speak, perform) allows diverse learners to demonstrate understanding. *(Hwang & Taylor 2016; Belland 2017a; Israel et al. 2015)* [Kuzmina & Romero 2025 removed 2026-04-10 during Phase C Kuzmina review: the paper does not test or support CRA; citing it here was inferential overreach. The paper's relevance is narrowly to the think-aloud self-regulation observation, not to the CRA sequence.]

9. **Modular, tangible robotics (vs. pre-made) enable agency, creativity, and self-regulation.** LEGO Mindstorms, Cubelets, modular platforms align with constructionist learning theory. Pre-made robots limit creativity. Directly argues for Arduino/ESP32 over closed educational platforms. *(Díaz-Boladeras 2025; Israel et al. 2015)* [Kuzmina & Romero 2025 removed 2026-04-10 during Phase C Kuzmina review: the paper's study used pre-made Cubelets (not open construction), and its quantitative hypotheses that children with ADHD would show higher divergent-thinking scores were NOT statistically supported. Citing Kuzmina here to support "modular tangible robotics enable creativity" is doubly contradicted — CreaCube is exactly the pre-made platform the principle argues against, and the paper's own findings do not support the principle's claim about creativity. The principle statement itself may also need softening; the paper's null result is specifically relevant to it.]

10. **"Non-human mediator" effect — robots and structured systems reduce anxiety while maintaining accountability.** The emotional distance of a task card or robotic system vs. a human teacher reduces demand perception. "Body doubling" (presence of another entity) helps ADHD students reduce procrastination. *(Berrezueta-Guzmán 2021a, 2021b; Cibrian 2022; O'Connell 2024)* [Papakostas 2021 removed in Phase C re-audit — the framing was an inference across the review's constituent studies, not a synthesis by Papakostas themselves]

### Movement, physical exercise, and regulation

11. **Physical exercise produces the largest EF effect sizes for ADHD** — g = 0.900 on inhibitory control and g = 1.377 on cognitive flexibility. Movement breaks are not an optional extra; they're a core intervention. *(Qiu et al. 2023)*

### Motivation and external structure

12. **External structure is enabling, not undermining, for ADHD.** Structured external supports (task breakdowns, checklists, reinforcement schedules, explicit contingencies) are not deficits-focused — they are optimizing conditions. Intrinsic motivation is cultivated through competence + autonomy within structure, not instead of it. Extrinsic motivation paradoxically supports ADHD academic outcomes. *(Smith, Langberg et al. 2020; Morsink 2022; Rosen et al. 2014)*

### Collaboration, relationships, and SEL

13. **Relationships are the strongest moderator of behavior intervention effectiveness.** Structure + relationships > structure alone. Relational components (peer support, adult mentoring, where possible family communication) multiply the effects of other interventions. *(Gersib & Mason 2023; Gage et al. 2021; Koslouski 2023; Asselman 2025)*

14. **Cooperative learning requires explicit teaching and monitoring of five core elements: positive interdependence, individual accountability, face-to-face interaction, social skills, group processing.** Just "putting kids in groups" fails for EBD populations. *(Wattanawongwan 2021; Daunic 2023)*

15. **Session predictability, ritual, and daily check-in/check-out routines** reduce anxiety and build trust. The ritual itself — not just its content — is calming for dysregulated students. *(Flannery 2024; Kittelman 2024; Kleinsmith 2025)*

### Staff, teacher well-being, and implementation

16. **Teacher burnout predicts reduced effective strategy use and less autonomy-giving.** Teacher well-being is a first-class design constraint, not an afterthought. Arduino PBL must reduce teacher load (pre-prepared materials, self-directed task cards, peer co-facilitation). *(Gilmour 2022; Taylor 2024 — teacher job satisfaction improved post-intervention; Koslouski 2023 on secondary traumatic stress)*

17. **Brief written psychoeducation for staff > long workshops for OCD knowledge transfer.** 2-page fact sheets produced significant improvements; 2-hour workshops did not. Implication for the Ministry proposal: deliverables should include printable staff reference cards, not multi-hour training obligations. *(Colbert 2025; Abramovitch 2024)*

18. **Embedded coaching during lessons outperforms one-shot professional development workshops.** Teacher collaboration, peer mentoring, and in-the-moment problem-solving sustain implementation fidelity. *(Israel et al. 2015; Taylor 2024; Sciacca 2025)*

### UDL and accessibility

19. **UDL's three principles (Representation, Expression, Engagement) have large meta-analytic effects (g = 3.56) but with high heterogeneity.** Implementation as school-wide, PD-supported intervention outperforms piecemeal application. *(Almeqdad 2023; Phelan 2025; Boysen 2024 — critical view)*

### Anxiety-specific

20. **Exposure-informed, approach-oriented anxiety support beats avoidance accommodation.** Schools often inadvertently reinforce avoidance through compassionate short-term accommodations, prolonging anxiety. Brief scaffolding to face feared situations + explicit fading > permanent opt-outs. (But: for OCD specifically, avoid public ritual visibility — see Abramovitch 2024.) *(Håland 2025; Werner-Seidler 2021)*

---

## Cross-cluster honest caveats

The curriculum's "Honest Limitations" section (Phase C) will draw from these. All the caveats below must be reflected honestly in the Ministry proposal — no overclaiming.

### On the research base itself

1. **The empirical base for trauma-informed schools is weaker than commonly claimed.** Watson & Astor (2025) critically reviews the field and finds that whole-school trauma-informed approaches lack robust RCT evidence. Safety, relationships, and strengths-based components have convergent but not causal evidence. Smaller localized practices (daily check-ins, clear expectations, relationship-building) have stronger evidence than sweeping framework adoption.

2. **Only ONE empirical study (Taylor 2024) directly examines PBL outcomes for EBD students in a classroom.** Sciacca 2025 is a qualitative dissertation (teacher perspective) that we could only access at abstract level. All other PBL-EBD synthesis in the corpus is inferential from adjacent literatures.

3. **Zero studies in the corpus examine Arduino, ESP32, Raspberry Pi, breadboards, circuit design, or student-built microcontroller projects for students with ADHD, EBD, or LD.** This is the largest single gap relative to the Agourim curriculum's core technology.

4. **Zero studies in the corpus examine aerial robotics / drone / flight-STEM for any special-needs population.** The quadcopter capstone (Project 8) has no direct research support — it is an inferential extension from ground robotics + modular hands-on STEM literature. Must be explicitly flagged in the Project 8 chapter.

5. **Zero studies in the corpus examine Claude Code / conversational AI tutors / AI-paired learning for neurodivergent students.** The curriculum's use of Claude Code as a coding collaborator is novel and untested empirically. Report this as a research opportunity, not a proven practice.

6. **Depression and anxiety prevention effect sizes are small (g ≈ 0.18–0.21 for universal; g ≈ 0.33 for targeted).** Effects attenuate at follow-up. *(Werner-Seidler 2021; Zhang 2023)*

7. **No studies on students designing, building, programming, or iteratively improving their own robots.** All robotics-in-special-education research examines students *interacting with* or *being supported by* pre-made robots (NAO, Pepper, educational kits). Construction-oriented robotics research is absent.

### On the verification pipeline itself (meta-caveat)

**The initial article-verifier sweep made TWO mis-corrections that Phase A deep-reading caught and re-verified:**

- **P2 — Rosen, Boyle, Cariss, Forchelli (2014), not Meltzer et al.** The initial sweep "corrected" an unattributed entry for ERIC EJ1168865 to "Meltzer, Reddy, Sales Pollica & Roditi (2014)." Phase A confirmed via direct ERIC lookup that EJ1168865 is actually Rosen, Boyle, Cariss, Forchelli (2014), "Changing How We Think, Changing How We Learn: Scaffolding Executive Function Processes for Students with Learning Disabilities," *Learning Disabilities: A Multidisciplinary Journal* 20(4), 165–176. The file `articles_full_texts/meltzer_2014.txt` contains the actual Rosen et al. paper with an explicit note flagging the misattribution. **Verification_Log P2 updated with re-correction note; Research_Articles_Bibliography.md #31 updated.**
- **P11 — Gibbs (2023), not Whitaker et al.** The initial sweep "corrected" an unattributed bibliography entry to "Whitaker, S., Poed, S., Wood, T., & Colyvas, K. (2023)" with a note that it was "approximate — full author list per publisher." Phase A confirmed via direct Crossref lookup of DOI 10.1080/13632752.2023.2194131 that the actual author is **Kathy Gibbs (single author, Griffith University)**. The file `articles_full_texts/whitaker_2023.txt` contains the actual Gibbs paper. **Verification_Log P11 updated with re-correction note; Research_Articles_Bibliography.md #35 updated.**

**Failure pattern:** In both cases, the initial sweep invented authorship where the original entry had none, rather than leaving authorship blank or flagging the entry as needing human review. The invented authors were plausible (real researchers in the same field) but incorrect. **Implication for Phase B:** Before finalizing the literature review, spot-check any other "Partial/Corrected" entries where the initial sweep added author names to previously-unattributed citations. Entries P4, P5, P6, P8, P9, P10, P11, P12 all fit that pattern. The ones where the correction came from Crossref DOI lookups (P3, P6, P7, P8, P9) are more trustworthy than the ones where the correction came from WebSearch or inference (P2, P11). Run a targeted re-verification pass on the remaining WebSearch-derived corrections.

### On measurement and implementation fidelity

- **CICO implementation fidelity ranges 65–87%** across studies — school buy-in and coaching are not optional. *(Kittelman 2024; Flannery 2024)*
- **Accommodation paradox** — compassionate short-term accommodation for anxiety can prolong avoidance and worsen long-term outcomes. *(Håland 2025)*
- **Meta-analytic effects of UDL are large (g = 3.56) but with high heterogeneity** and implementation fidelity is rarely measured. *(Almeqdad 2023; Boysen 2024 — critical)*
- **Small samples dominate.** Many EBD/PBL/robotics-special-ed studies have n < 20, single-case designs, or pilot scope. Most effect-size claims are provisional.

---

## Cross-cluster gaps relevant to the Arduino PBL program

Aggregated from all three clusters. Each will be flagged in the master document's Honest Limitations section.

1. **No Arduino / microcontroller / physical computing research for EBD/ADHD/LD populations.** Gap is total.
2. **No aerial robotics / drone / flight-STEM research for special-needs populations.** Gap is total.
3. **No Claude Code / AI-tutor research for neurodivergent students.** Gap is total.
4. **Limited research on students building robots vs. using pre-made ones.** Construction-oriented robotics research is absent.
5. **Only one empirical PBL-in-EBD-classroom study (Taylor 2024).**
6. **Limited research on small-group PBL in special education** — most studies are whole-class inclusive or 1:1.
7. **No research on failure, iteration, productive struggle in PBL for ADHD/EBD.** How should debugging failures and project setbacks be scaffolded? Unknown.
8. **Limited longitudinal data.** Most studies are 4–12 weeks; long-term skill transfer and identity development in STEM for EBD/ADHD students are untracked.
9. **Unclear how to simultaneously scaffold mixed ADHD/ODD/OCD/anxiety/trauma cohorts** — most studies target single diagnostic profiles.
10. **OCD-specific accommodation in open-ended problem-solving contexts unaddressed.**
11. **CICO evidence is concentrated in elementary (K–6) and high school (9–12) — middle school (7–8) is understudied.** Agourim spans both.
12. **Anxiety accommodation in project-based contexts unaddressed** — Håland (2025)'s accommodation paradox is not empirically reconciled with inclusive PBL practice.
13. **Family engagement in school-based PBL for EBD not addressed.** Relational moderators are strongest when they include family, but the Arduino workshop is school-centric.
14. **Cost, resource, and fidelity barriers to implementation are rarely discussed** — intervention studies assume availability and training.
15. **Scaffold fading and learned helplessness risk unclear.** When do you reduce scaffolding? How do you prevent dependency? No empirical decision rules.
16. **Teacher burnout mitigation within EBD-PBL contexts** — Taylor 2024 is the only study to measure teacher job satisfaction as an outcome.

---

## Special Task 1 — Audit of `gomez_2019.txt`

**Finding:** This file is **NOT** an unmatched orphan. It is the full text of Verification_Log entry **#19**:

- **Author:** Alvaro Gomez
- **Title:** *The Effects of Makerspace Learning on the Social Interactions among Students with Emotional or Behavioral Disorder*
- **Type:** Doctoral dissertation
- **Institution:** University of Texas at San Antonio
- **Year:** 2019
- **Identifier:** ERIC ED604859; ProQuest Dissertations & Theses
- **Summary:** Single-case experiment with multielement design; examined how makerspace participation (constructionist principles) affected social competencies and peer interactions of four middle-school EBD students. Found makerspace supported social-emotional skill development vs. traditional classroom contexts.

**Arduino PBL relevance: HIGH.** This is the closest thing in the corpus to a study of open-ended, constructionist, hands-on learning for middle-school EBD students. It is directly relevant and should be cited prominently in:
- Phase C literature review (as near-neighbor evidence for maker-style Arduino PBL with EBD)
- Phase B principle distillation (as evidence for constructionist learning for EBD populations)

**Recommendation:** The entry is already verified in Verification_Log (row #19). I've added the author name ("Gomez, A.") to the log entry so future sessions can match the file name directly to the citation. The Verification_Log summary "78 unique citations found" remains correct — no new citation, just a metadata fix.

---

## Special Task 2 — Drone / Aerial-Robotics / Flight-STEM Search

**Search scope:** All 78 files in `articles_full_texts/` (grep, case-insensitive) for: drone, drones, UAV, quadcopter, quadrotor, multirotor, aerial robot, flying robot, aircraft, flight, propeller, rotor, hover, hovering.

**Finding: zero substantive hits.** The only mention of "aircraft flying" was a metaphorical usage in CAST 2018's scaffolding-as-apprenticeship discussion. No paper in the corpus contains educational research on aerial robotics, drone construction, flight-STEM pedagogy, or quadcopter-based learning for any population — neurotypical or neurodivergent.

**Implication for Project 8 (Quadcopter):** The capstone project has no direct research base in the verified corpus. It rests on inferential extension from:
- Ground robotics for ADHD/EBD (Berrezueta-Guzmán 2021a, 2021b; Cibrian 2022; O'Connell 2024)
- Modular, tangible, student-built STEM (Guneysu Ozgur 2020; Israel et al. 2015) [Kuzmina & Romero 2025 removed 2026-04-10 during Phase C Kuzmina review: CreaCube is a pre-fab Cubelets assembly puzzle, not student-built construction in the Arduino sense; the paper does not support this category]
- Scaffolded computational thinking (Belland 2017a, 2017b; Hwang & Taylor 2016)
- Makerspace learning for EBD (Gomez 2019)

**This gap MUST be explicitly flagged in the Project 8 chapter of the master document and in the Honest Limitations section.** Phase B should also consider whether to search for quadcopter / drone education literature OUTSIDE the verified corpus — if yes, that's a Phase A+ extension and new citations would need verification via the article-verifier pipeline.

**Phase B decision point:** should we expand the verified corpus to include drone-specific education research, or should we leave Project 8 as explicitly evidence-thin and frame it honestly as an inferential extension?

---

## Open questions for Phase B

1. **Corpus expansion for drone research** — expand now, or frame Project 8 as inferential?
2. **Re-verification of other "Partial/Corrected" entries** — how thoroughly should we audit P4, P5, P6, P8, P9, P10, P12 in light of the two misattributions Phase A found?
3. **Weighting of evidence** — how honestly should the master document weight "large meta-analytic effect" (Almeqdad UDL g=3.56) against "critical review saying the field is weak" (Watson 2025, Boysen 2024)?
4. **Cluster 1/2/3 overlap resolution** — several candidate principles appear across clusters with slightly different framings. Phase B should merge these into a single unified principle set.

---

## What Phase B will do with this

Phase B (Principle Distillation) will:
1. Read this file plus the three cluster files as primary input
2. Select ~6–10 core design principles for the Arduino curriculum (down from the ~20 candidates above)
3. Each selected principle: 1 sentence statement + 2–3 verified citations + 1 paragraph evidence note + 1 design-rule translation for the 7+1 Arduino projects
4. Produce `Arduino_Principles.md` (or integrate the principles into `Arduino_PBL_Program.md` — decide in Phase B)
5. Audit the remaining Verification_Log Partial/Corrected entries per the meta-caveat above
6. Decide whether to expand the corpus with drone-specific literature
