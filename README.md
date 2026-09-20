# vibe-kit

Personal toolkit for vibe coding: AI skills, agents, loops, prompts and snippets.

I use this repo to sync my setup between laptops. Private by default.

## Layout

- `skills/` — reusable skills, each in its own folder with a `SKILL.md`
- `agents/` — custom agents (Markdown definitions)
- `loops/` — repeatable workflows / loops (plan → build → review, etc.)
- `snippets/` — small copy-paste prompts and code pieces

## Use on a new laptop

```bash
git clone git@github.com:<you>/vibe-kit.git ~/vibe-kit
cd ~/vibe-kit
./install.sh
```

`install.sh` symlinks everything into the standard local skill/agent paths,
so you edit in `~/vibe-kit` and all tools pick it up.

## Daily workflow

```bash
cd ~/vibe-kit
# edit / add files, then:
git status
git add -A
git commit -m "update skills"
git push
# on the other laptop:
git pull
```

## Add a new skill

```bash
mkdir -p skills/my-skill
# create skills/my-skill/SKILL.md (see skills/example-skill/SKILL.md)
./install.sh
git add -A && git commit -m "add my-skill" && git push
```

## Add a new agent or loop

- Copy `agents/example-agent.md` → `agents/<name>.md` and edit.
- Copy `loops/example-loop.md` → `loops/<name>.md` and edit.

## Make the GitHub repo

1. Go to github.com → New repository → name `vibe-kit` → Private.
2. Then:

```bash
cd ~/vibe-kit
git init -b main
git add -A && git commit -m "init vibe-kit"
git remote add origin git@github.com:<you>/vibe-kit.git
git push -u origin main
```
