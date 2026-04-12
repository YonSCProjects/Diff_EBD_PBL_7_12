# Editorial Preferences Log

*A running list of editorial patterns observed in Yon's edit requests to the Arduino PBL program master document and related project files. Maintained by the main Claude Code agent as working memory, and consumed by the `editorial-coherence` subagent to propose consistent revisions to other parts of the text.*

**How this file is used:**
- The main agent (Claude, in the orchestrating conversation) updates this file any time Yon requests a change whose "spirit" or "pattern" is worth preserving for consistency — not every minor edit, but every edit that reveals a *voice preference* applicable elsewhere.
- The `editorial-coherence` subagent reads this file as its primary source of truth before scanning any part of the document for coherence issues.
- Patterns are added in the order observed; new patterns go at the bottom; updates to existing patterns are made in place with a date note.
- When a pattern turns out to have been mis-inferred (e.g. Yon's next edit contradicts it), mark the pattern as **RETRACTED** with a date and brief explanation rather than deleting it, so future sessions can see the history.

---

## Pattern 1 — Terminology: "program," not "curriculum"

**Rule:** Use "program" or "workshop program" (in the title and first mention) to describe the overall 8-project Arduino work. Reserve "curriculum" only for generic references to *other* formal secondary education curricula (e.g. "what most secondary curricula assume").

**Why:** "Curriculum" implies formal, prescriptive content coverage — like "the grade-10 math curriculum" — and the Arduino workshop is not that. It is an 8-project workshop track that students experience as part of their school day, but it is not replacing a core subject and its pacing is deliberately flexible.

**Scope:** The master document (`Arduino_PBL_Program.md`), all per-project files, and any future writing about the Arduino work. NOT retroactively applied to the earlier Research_Articles_Bibliography.md or Detailed_Article_Summaries.md, where "curriculum" may appear as part of older framing.

**Examples (from session 2026-04-10):**
- **Before:** "Differentiated Project-Based Arduino **Curriculum** for Students with EBD"
- **After:** "Differentiated Project-Based Arduino **Workshop Program** for Students with EBD"

- **Before:** "No prior published **curriculum** combines all three of these ingredients..."
- **After:** "No prior published **program** combines all three of these ingredients..."

- **Exception kept:** "These students need a learning environment that differs substantially from what most secondary **curricula** assume." (Here "curricula" refers generically to other schools' formal curricula, not our work.)

---

## Pattern 2 — Audience specificity: "potential evaluating and funding organizations," not named agencies

**Rule:** When describing the document's second audience (the one evaluating it for funding/support), use generic language like "potential evaluating and funding organizations" or "evaluating reviewer." Do not name the Israeli Ministry of Education or any other specific body.

**Why:** Keeps the document portable. If the proposal is later submitted to a different funder (a foundation, a grant body, another ministry), no text needs to change.

**Scope:** The master document and any companion proposal materials.

**Examples (from session 2026-04-10):**
- **Before:** "as a research-grounded proposal to the Israeli Ministry of Education"
- **After:** "as a research-grounded proposal for potential evaluating and funding organizations"

- **Before:** "written with the Ministry reviewer in mind"
- **After:** "written with an evaluating reviewer in mind"

- **Before:** "academic integrity and the Ministry's trust both depend on this honesty"
- **After:** "academic integrity and the reviewer's trust both depend on this honesty"

---

## Pattern 3 — Inclusive framing: examples must be labeled as illustrative, not exhaustive

**Rule:** When listing examples of student characteristics, diagnoses, behaviors, or contrasts, always introduce them with language that explicitly marks them as *representative, not comprehensive*. Phrases like "a few illustrative contrasts, drawn from a much longer list" or "among the more commonly seen" or "these examples are illustrative, not exhaustive" are preferred.

**Why:** The student population is genuinely heterogeneous. Any list of diagnoses, traits, or backgrounds will always miss students who don't fit. Labeling examples as illustrative respects that heterogeneity and prevents readers from assuming the list is definitive.

**Scope:** Any passage that describes the Agourim student population or any subgroup within it. Especially important in §1 Introduction and §2 Population Profile, but applies throughout.

**Examples (from session 2026-04-10):**
- **Before:** "They arrive at Agourim carrying a wide range of diagnoses — ADHD, oppositional defiant disorder, anxiety, depression, obsessive-compulsive disorder, post-trauma — and an even wider range of strengths, backgrounds, and literacy levels. Some read fluently; some can barely read or write. Some come from supportive, engaged homes; some come from neglect..."
- **After:** "They arrive at Agourim carrying a wide range of diagnoses — ADHD, oppositional defiant disorder, anxiety, depression, obsessive-compulsive disorder, and post-trauma **among the more commonly seen** — and an even wider range of strengths, backgrounds, and literacy levels. **A few illustrative contrasts, drawn from a much longer list of dimensions along which our students differ:** some read fluently while others can barely read or write; some come from supportive, engaged homes while others come from neglect... **These examples are illustrative, not exhaustive** — no two students at Agourim look alike, and this program is designed to make room for that range."

---

## Pattern 4 — Softened claims: prefer "many of them," "most of these students," "often" over universal claims

**Rule:** When making claims about what the students "need" or how they "behave," prefer inclusive-but-not-absolute framing:
- "They need X" → "Many of them need X" or "Most of these students benefit from X"
- "They all respond to Y" → "Many respond to Y"
- "Have not worked" → "Have often not worked"
- "Always triggers" → "Tends to trigger"

**Why:** The population is heterogeneous. Absolute claims flatten that heterogeneity and risk being wrong for specific students. The softer framing is both more accurate and more respectful of individual variation. Also: the softer framing maps more honestly onto the actual research base, where effect sizes describe average or majority responses, not universal ones.

**Scope:** All descriptive passages about student needs, behaviors, or responses to instructional choices. Does NOT apply to §9 Honest Limitations, where the job is to be blunt about what the research does and does not cover (so softening there would undermine the honesty; see Pattern 7 for the contrast).

**Examples (from session 2026-04-10):**
- **Before:** "These students need a learning environment that differs substantially from..."
- **After:** "Most of these students benefit from a learning environment that differs substantially from..."

- **Before:** "They need it to be predictable..."
- **After:** "They often need it to be predictable..."

- **Before:** "They need tasks that produce tangible, immediate results... because abstract academic wins have not worked for them."
- **After:** "Many of them need tasks that produce tangible, immediate results... because abstract academic wins have often not worked for them."

- **Before:** "And they need autonomy, choice, and voice..."
- **After:** "And many benefit from autonomy, choice, and voice..."

---

## Pattern 5 — Soft, forward-looking endings; no accusatory absolutes

**Rule:** When a paragraph ends with a claim about what an alternative approach would do wrong, rephrase as a forward-looking statement about what *this* program does right. Avoid absolute negative claims like "will fail most of them" or "will always go wrong."

**Why:** The super-target of the program is *small positive empowering experiences*. The document's tone should match — owned and constructive, not accusatory. "Any program that does X will fail" reads as blame-casting; "this program is designed to do Y" reads as design commitment.

**Scope:** All prose throughout the master document, especially paragraph endings and section transitions.

**Examples (from session 2026-04-10):**
- **Before:** "...and any program that treats them as a single type will fail most of them."
- **After (first revision):** "...and this program is designed to make room for that range rather than assume a single average."
- **After (second revision, same session):** "...and this program is designed to make room for that range."

  (Note the double-edit: Yon first asked to soften the absolute negative, then asked to drop the "rather than assume a single average" clause — see Pattern 6 for the terseness preference.)

---

## Pattern 6 — Terseness: when the point is made, stop

**Rule:** When a phrase has made its point, do not add an "as opposed to X" or "rather than Y" explanatory tail. Let the positive statement stand on its own.

**Why:** The explanatory tail often adds noise without adding meaning. Readers can infer the contrast from the positive statement. Shorter is sharper.

**Scope:** Prose throughout. Especially relevant for paragraph endings (see Pattern 5 for the related softening pattern).

**Examples (from session 2026-04-10):**
- **Before:** "...this program is designed to make room for that range rather than assume a single average."
- **After:** "...this program is designed to make room for that range."

**Caveat:** This does NOT mean to strip all explanatory phrases. Explanations that clarify a non-obvious term, introduce a research finding, or unpack a technical concept should stay. The rule is specific to rhetorical contrast tails that add nothing beyond what the positive statement already implies.

---

## Pattern 7 — Structural mismatch language, not student-failure language

**Rule:** When describing the students' prior school history, frame the mismatch at the system level rather than at the student level. "Mainstream primary school did not meet their needs" is preferred over "They did not survive primary school" or "They failed primary school."

**Why:** The framing shapes how students are seen. "Students who failed primary school" puts the deficit on the students; "students whose needs primary school did not meet" puts the mismatch on the mismatch — which is accurate (these students have strengths; the system was not designed around them) and respectful.

**Scope:** All descriptions of student history, both in the master document and in any materials that will be seen by students or by other teachers.

**Examples (from session 2026-04-10):**
- **Before:** "students who did not 'survive' regular primary school"
- **After:** "students whose needs were not met by mainstream primary school" / "mainstream primary school did not meet their needs"

---

## Pattern 8 — Honest limitations are NOT softened

**Rule:** §9 Honest Limitations and similar transparency sections (e.g. the Phase A meta-caveats in `Arduino_LitReview_Notes.md`) should be direct and blunt. Do not apply Pattern 4 (softening) or Pattern 5 (forward-looking endings) to these sections. When stating what the research does NOT cover, say it clearly. When flagging a principle as untested, say "zero direct empirical support" not "limited empirical support."

**Why:** The credibility of the entire document rests on the honesty of its limitations section. Softening limitations undermines the trust it was written to earn. Pattern 4 and Pattern 5 apply to *descriptive* passages about students and the program; Pattern 8 is the exception for *limitations/caveats* passages.

**Scope:** §9 Honest Limitations, any "what the research does not cover" subsections, any passage explicitly flagged as an integrity/transparency statement.

**Examples (from session 2026-04-10, Phase A/B notes):**
- **Bluntness preserved:** "Zero studies in the corpus examine Arduino, ESP32, Raspberry Pi, breadboards, circuit design, or student-built microcontroller projects for students with ADHD, EBD, or LD. This is the largest single gap relative to the Agourim curriculum's core technology."
- **Bluntness preserved:** "This principle has no direct empirical support in the verified corpus — zero studies in the 65 full-text articles examine Claude Code, conversational AI tutors, or AI-paired learning for neurodivergent students."

These are the *right* tone for limitations sections. If the `editorial-coherence` agent ever suggests softening them, the suggestion should be rejected.

---

## Pattern 9 — Absence claims must be scoped to "the verified literature we reviewed"

**Rule:** Any claim that something "has not been done," "has not been combined," "has not been tried," or "does not exist in the research" must be scoped to the specific body of evidence we actually reviewed. Phrases like "to the best of our knowledge" are not sufficient — use explicit scoping:
- "In the research literature we reviewed during Phase A, we did not find..."
- "The verified corpus we reviewed contained no..."
- "We found no study in the 65 full-text articles we deep-read that..."
- "These absence-claims are scoped to the verified corpus we reviewed in Phase A; we cannot rule out the existence of relevant work outside it."

**Why:** We have no way to know what individual teachers in individual classrooms have tried without publishing, or what exists in research literature we did not read, or what is happening in unpublished grey literature and private curricula. The only thing we can honestly defend is "we did not find it in the corpus we reviewed." Any stronger claim overreaches the evidence and invites correction from a reviewer who knows about work we didn't see.

**Scope:** All claims of novelty, absence, or gap in §1 Introduction, §3 Literature Review, §9 Honest Limitations, and any other section that makes evidence claims. This pattern is **consistent with** Pattern 8 (honest limitations not softened) — both are about epistemic honesty — but this one is specifically about the *scope of absence claims* rather than the *tone of limitation statements*. Keep the claims blunt (per Pattern 8); scope them honestly (per Pattern 9).

**Examples (from session 2026-04-10):**
- **Before:** "This program is built from three ingredients that the research supports independently but that, to the best of our knowledge, have not previously been combined for this population."
- **After:** "This program is built from three ingredients that the research supports independently. In the research literature we reviewed during Phase A of this work, we did not find a published study that combined all three for this population — which is not to say no teacher has tried similar combinations in their own classroom, only that we could not locate such work in the verified corpus."

- **Before:** "No prior published program combines all three of these ingredients for students with emotional and behavioural disorders."
- **After:** "In the research literature we reviewed during Phase A, we did not find a published program that combines all three of these ingredients for students with emotional and behavioural disorders."

- **Before:** "There is no published research on aerial robotics, drones, or flight-STEM for any special-needs population — a gap we confirmed by searching all 78 files in our full-text corpus..."
- **After:** "We also found no research on aerial robotics, drones, or flight-STEM for any special-needs population — we confirmed this by searching all 78 files in our full-text corpus for any mention of drones, quadcopters, UAVs, or flight, and found only one metaphorical hit in the CAST (2018) UDL guidelines. [...] These absence-claims are scoped to the verified corpus we reviewed in Phase A; we cannot rule out the existence of relevant work outside it."

**Nuance for different kinds of absence claims:**
- **Keyword-searched absences** (like the drone search) are stronger because we performed an explicit systematic check — mention the search.
- **Topical absences** (like "no Arduino research for EBD") are weaker because we did not explicitly keyword-search for them in every possible phrasing — scope to the corpus and acknowledge the limit.
- **Genuinely-new-technology absences** (like "no AI-tutor research for neurodivergent students") can lean on "this class of tool is too new for a research literature to have developed around it" as additional support, but should still be scoped to the corpus.

---

## Pattern 10 — When citing research, verify the claim is what the paper's own authors actually conclude

**Rule:** Before attributing a claim to a cited paper, open the paper's own full-text source file (not just a synthesis summary or a cluster notes file) and confirm four things:
1. The claim is what the paper's authors themselves conclude, not a sentence the paper quotes from a secondary source as framing or background.
2. If the paper reviews empirical studies, the claim is consistent with what those studies actually found, not a hypothesis the paper tested and failed to support.
3. The claim is not an oversimplification that strips away the paper's own nuance.
4. Effect sizes, percentages, and statistical claims come from the specific paper being cited and are not crossed with results from different papers by similar authors on similar topics.

**Why:** Phase B of this project distilled 9 design principles based on Phase A cluster summaries, which were themselves based on sub-agent readings of full-text files under token-budget pressure. Two significant misreadings survived into Phase C and were only caught when Yon asked to see the evidence directly:

- **Barker & de Lugt (2022)** was cited in Principle 5 as saying token economies are counterproductive for students with ODD. The paper actually reviews empirical studies of token economies in ODD classroom settings and reports strong positive effects (Rosenberg 1986, in their evidence table: 82% M PND for on-task behavior, 91% M PND for reducing disruptive behavior with rule reminders). The "rebel against any attempt to modify behavior... would see this as a manipulation" sentence I relied on (at lines 170–175 of the source file) is the paper's theoretical framing of *why ODD is hard*, attributed to a secondary source (Barkley & Benton 2013). It is not the paper's own conclusion about what works in classrooms, and the paper's own empirical review points the opposite way.
- **Morsink et al. (2022)** was cited in the same Principle 5 sentence as saying external reinforcers undermine intrinsic motivation in students with ADHD. The paper actually reviews two studies (Carlson et al. 2000; Carlson & Tamm 2000) that *explicitly tested* this hypothesis in children with ADHD, and **neither study found the undermining effect** — the first found no effect "contrary to their hypothesis," and the follow-up with manipulated task interest also found no detrimental effects. Morsink et al. are calling for more research into whether such an effect might exist under different conditions, not reporting that it does.

Both misattributions happened in the same sentence of the same principle because both relied on a Phase A cluster summary rather than on the source files. The cost of the error — a design principle recommending against token economies in a school that uses a school-wide token economy — was significant enough to make the verification discipline a first-class editorial pattern.

**How to apply:**
- For §3 Literature Review and every subsequent section of the master document, open the actual full-text source file for any claim that carries argumentative weight in the document. The cluster summary files (`Arduino_LitReview_Cluster1.md`, `Cluster2.md`, `Cluster3.md`) are useful navigation aids and map-readings, but they are not a substitute for the source.
- **Pay particular attention to claims that justify a contrarian or anti-default stance** — claims of the form "the research says we should NOT do X." These are the most dangerous to misattribute because they shape the document's recommendations against the intuitive choice, and reviewers who disagree may look for exactly these claims in the source and catch the misreading.
- **Pay particular attention to sentences the paper quotes from other papers.** A paper can quote a claim from a secondary source as theoretical framing, background, or "here is what has been said," without endorsing it. Those sentences do not represent the citing paper's own view and should not be attributed to the citing paper.
- **Pay particular attention to hypotheses the paper tested.** A paper can discuss a hypothesis at length without confirming it. The discussion is easy to mistake for confirmation if you read quickly. If the paper says "we tested X," find out what the test actually found before citing X as an established finding.
- **When a cluster summary makes a claim with certainty but the claim is load-bearing in the master document, the budget of one careful read of the source is small compared to the cost of being wrong in front of a reviewer.** Do the read.

**Examples:**
- **Wrong (Phase B initial):** "No reward/token systems (per Barker & Morsink: ODD reads them as manipulation, ADHD responds to them as substitutes for intrinsic competence)."
- **Right (Phase C corrected):** "The workshop's choice to use social/immediate/tangible recognition is NOT grounded in a research-based opposition to token economies — Barker & de Lugt (2022) actually report strong positive effects of token economies in ODD classroom studies (e.g., Rosenberg 1986: 82–91% PND), and Morsink et al. (2022) review studies that tested and failed to confirm an undermining effect of rewards on ADHD intrinsic motivation. The workshop's choice is grounded in workshop-specific fit: hardware-based milestones are already inherently tangible, a small-group setting has capacity for immediate personal acknowledgment, and Agourim already operates a school-wide token economy that the workshop does not need to duplicate."

**Related patterns:**
- Pattern 8 (honest limitations unsoftened) — both are about epistemic honesty, but Pattern 8 is about how to present *limits on what we know*, while Pattern 10 is about how to verify *what we are claiming to know*.
- Pattern 9 (scoped absence claims) — Pattern 9 is a specific instance of Pattern 10 applied to absence claims. Pattern 10 is the broader discipline of which Pattern 9 is one case.

**Audit note:** Given that two misreadings surfaced within the same Principle 5 sentence, the other Phase B principles should be treated as *plausible-but-unverified* until each citation in them has been checked against its source file. For §3 Literature Review and §4 Design Principles, run a citation-audit pass before or during drafting. §3 Literature Review in particular should not ship until every claim it makes has been directly sourced, not just synthesis-sourced.

---

## Pattern 11 — Frame the program as PBL-with-DI, not DI-with-projects

**Rule:** When naming or introducing the program in audience-facing framing (titles, abstracts, executive summaries), lead with "Project-Based Learning in a Differentiated-Instruction style." Do NOT lead with "Differentiated Arduino Workshop." PBL is the primary pedagogical frame; DI is the instructional modifier.

**Why:** PBL is the concept Ministry of Education officials and colleagues will immediately recognize from their professional training. DI is the qualifier that explains *how* this PBL is implemented. Leading with "Differentiated Arduino Workshop" makes the program sound like an instructional-design intervention with projects attached; reversing the order aligns with how educators mentally categorize this work and signals the program's pedagogical center of gravity correctly.

**Scope:** Titles and first-mention framing in all audience-facing documents (overview, master-doc abstract, executive summary, any funder-facing material). The reverse framing ("differentiated Arduino workshop") is fine in implementation-detail contexts where the student-work-tier aspect is the foreground.

**Examples (from session 2026-04-12 Hebrew overview edit by Yon):**
- **Before:** `תוכנית סדנת ארדואינו דיפרנציאלית לתלמידים עם קשיים רגשיים-התנהגותיים` (title of Hebrew overview)
- **After:** `תוכנית ללמידה מבוססת פרויקטים בסגנון הוראה דיפרנציאלי לתלמידים עם קשיים רגשיים-התנהגותיים`
- English equivalent for future documents: `A Project-Based Learning Program in a Differentiated-Instruction Style for Students with Emotional and Behavioural Challenges`

---

## Pattern 12 — Prefer "navigation card" over "task card" in audience-facing framing AND in Hebrew student-facing materials

**Rule:** Use `כרטיסיית ניווט` (navigation card), not `כרטיסיית משימה` (task card), in Hebrew student-facing materials and in all audience-facing framing (Hebrew and English). Yon's decision as of 2026-04-12 was to propagate the "navigation card" terminology to ALL student-facing Hebrew materials, not to keep two registers. English audience-facing documents should use "navigation card" in parallel; English student-facing materials (once the retroactive English pass runs) should be updated to match.

**Why:** "Navigation" emphasizes student agency — the student navigates through the project — and reframes the card as a map the student uses to find their way. "Task" frames the card as an externally-imposed obligation and echoes the "task-to-complete" register that many EBD students have negative associations with. The shift in terminology is small but the framing change is meaningful for a population whose school history is largely one of imposed tasks they did not choose.

**Scope:** All Hebrew student-facing materials (task cards, reference cards, tutorial, Channel B scaffold) — updated across 18 files on 2026-04-12. All audience-facing documents in both languages. English student-facing materials to be updated in the retroactive English pass.

**Examples (from session 2026-04-12):**
- **Before:** `כרטיסיית משימה` / "task card" / `כרטיסיות המשימה`
- **After:** `כרטיסיית ניווט` / "navigation card" / `כרטיסיות הניווט`
- **Hebrew file titles updated:** all 14 task cards' `<title>` tags changed from `כרטיסיית משימה פרויקט 1` to `כרטיסיית ניווט פרויקט 1`.

---

## Pattern 13 — When describing origin/personal experience, use present tense and stay in-role

**Rule:** In first-person narrative sections describing the teacher's motivation or origin of the program, prefer present-tense framing that positions the writer as currently in the role, not past-tense framing that positions the experience as historical. Hebrew: `אני מתמודד` not `נתקלתי בהן`. English: "I cope with" not "I ran into."

**Why:** The program is a living document — Yonatan is still the workshop teacher, still dealing with these problems, still refining. Past-tense framing ("I ran into two problems") creates retrospective distance and reads as if the problems are solved. Present-tense framing ("I cope with two difficulties") positions the writer as an active practitioner whose authority comes from ongoing engagement, not from past experience. For a Ministry reader or colleague, present-tense signals that the program is being lived, not reported.

**Scope:** All first-person narrative sections — overview's "Why this program exists" section, master doc's §1.3 "Where this program came from" subsection, and any future teacher-voice writing.

**Examples (from session 2026-04-12 Hebrew overview edit):**
- **Before:** `התוכנית נולדה משתי בעיות שנתקלתי בהן כמורה בסדנה.`
- **After:** `התוכנית הזו נולדה בעקבות שני קשיים איתם אני מתמודד כמורה בסדנת התכנות והרובוטיקה בבית הספר עגורים.`
- The past-tense "was born" of the program is preserved (the origin is a historical fact); the problems themselves are in the present (they are ongoing).

---

## Pattern 14 — Add "and more" / `ועוד` to diagnostic and similar lists; never claim exhaustiveness

**Rule:** When listing student diagnoses, hardware, or any other category that is inherently non-exhaustive, always end the list with "and more" / `ועוד` / "among others." Never present such a list as closed.

**Why:** The program explicitly describes a heterogeneous population. A closed list ("ADHD, ODD, anxiety, depression, OCD, post-trauma") reads as "these are the students we serve" when the real message is "these are examples of the range." The added "ועוד" / "among others" signals openness and preempts the reader's question "what about students with X?" The same principle applies to hardware lists in workshop descriptions — the specific items shown are examples of what the workshop contains, not an exhaustive inventory.

**Scope:** Every diagnostic list, hardware list, and other inherently non-exhaustive list in every document. Both Hebrew and English.

**Examples (from session 2026-04-12 Hebrew overview edit):**
- **Before:** `(הפרעת קשב וריכוז, הפרעת התנגדות מתריסה, חרדה, דיכאון, הפרעה טורדנית-כפייתית, פוסט-טראומה)`
- **After:** `(הפרעת קשב וריכוז, הפרעת התנגדות מתריסה, חרדה, דיכאון, הפרעה טורדנית-כפייתית, פוסט-טראומה ועוד)`

---

## Pattern 15 — School name Hebrew spelling is עגורים (with ayin), not אגורים (with aleph)

**Rule:** The school's name in Hebrew is **עגורים** (with ayin, meaning "cranes"), not **אגורים** (with aleph). Apply this spelling consistently across every Hebrew document.

**Why:** Factual accuracy. The aleph spelling was a transliteration artifact from the English "Agourim" — the correct Hebrew spelling uses ayin because the school is named after cranes (the birds). Misspelling the name is a credibility-damaging factual error in a Ministry-facing document.

**Scope:** Every Hebrew file in the project. Propagated across all 21 Hebrew files on 2026-04-12 (Hebrew overview + 14 task cards + 5 reference cards + Hebrew tutorial + Channel B scaffold). Any future Hebrew document must use the ayin spelling.

**Examples (from session 2026-04-12):**
- **Before:** `בית ספר אגורים`
- **After:** `בית ספר עגורים`

---

*Last updated: 2026-04-12. Patterns 11–15 added after Yon revised the Hebrew executive overview in DOCX: Pattern 11 (PBL-first framing) from title change; Pattern 12 (navigation card) from a systematic terminology preference; Pattern 13 (present-tense origin voice) from "נתקלתי בהן"→"מתמודד"; Pattern 14 ("ועוד" on diagnostic lists) from explicit addition; Pattern 15 (school name spelling) from the אגורים→עגורים correction. Earlier entry: Pattern 9 added after Yon caught an overreaching novelty claim in §1. Pattern 10 added after Yon caught two misattributions of research stance in Principle 5 (Barker 2022 and Morsink 2022, both misread as opposing token economies when they actually do not).*
