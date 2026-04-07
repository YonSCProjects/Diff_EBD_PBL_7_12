Do the following three steps in order:

## Step 1: Save to Memory
Review the current conversation for any information worth persisting to memory. This includes:
- User preferences, feedback, or corrections (feedback memories)
- Project context, decisions, or goals (project memories)
- Details about the user's role, expertise, or working style (user memories)
- Pointers to external resources mentioned (reference memories)

If there is relevant information, write or update the appropriate memory files in the memory directory. If nothing new is worth saving, skip this step and say so briefly.

## Step 2: Commit
Look at all changed and untracked files (git status + git diff). If there are changes:
- Stage all relevant files (exclude .env, credentials, secrets)
- Write a concise commit message summarizing the changes
- Create the commit

If there are no changes, say "Nothing to commit" and skip to the end.

## Step 3: Push
Push the current branch to the remote origin.

Report what was saved to memory, what was committed, and confirm the push.
