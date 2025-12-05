# Overview

These are the basics of using Claude code.

# Initial setup

Get an account and install it. Duh!
See https://code.claude.com/docs/en/overview

## IDE Integration

You run it in a terminal, which can also be embedded in your IDE. See:
https://code.claude.com/docs/en/jetbrains
https://code.claude.com/docs/en/vs-code

## Permissions

Claude will ask you constantly for permissions. You can be as permissive or restrictive as you like.

I go with full permissions, YMMV.

```
cl='claude --dangerously-skip-permissions'
```

# Using Claude code

## Resuming previous sessions

Claude keeps track of previous sessions. You can resume the very last session with:

```
cl --continue
```

This is my primary resume mode. If you want to resume another previous session you can type:

```
cl --resume
```

You can also type the `/resume` slash command in Claude code.

In both cases you will get a list of previous sessions to choose from.

## Slash commands

Claude code has many slash commands. Just type `/` and you'll see a list of commands.

See [Slash Commands](slash-commands.md) for details.

## Running shaell commands

You can quickly run shell commands with the `!` modifier. For example, `! pwd` will run the `pwd` command and insert the output into the conversation.


# The CLAUDE.md file

This is where you give Claude code instructions for your project. You can have multiple CLAUDE.md files in a project. You can have a CLAUDE.md file in the root of your project, in subdirectories and in your home directory as `~/.cloud/CLAUDE.md` . If you have a personal CLAUDE.md file for a project that you don't want to commit to the repository, you can name it `CLAUDE.local.md` and ignored it in your .gitignore. Claude code will pick up both `CLAUDE.md` and `CLAUDE.local.md` files automatically at any level. You can also have a general CLAUDE.md file in your home directory that applies to all projects.

Claude code combines all CLAUDE.md files in its current directory and parent directories up to the home directory and adds them automatically to the prompt. `CLOUDE.md` files in sub-directories are pulled into the contet when working with files in these subdirectories.

## Command-line tools

Claude code has access to the shell environment that launched it. This means it can run any command-line tool you have
installed. It will be familiar with standard tools like `git`, `curl`, `ls`, etc. If you have custom tools installed,
you may want to provide some documentation for them in the CLAUDE.md file.
 
## Fine-tuning your CLAUDE.md files

It is a good idea to periodically review and refine your CLAUDE.md files to ensure they accurately reflect your current workflow and preferences. You can add new instructions on the fly with the inline `#` directive ro directly edit the CLAUDE.md files. 

Since they become part of the prompt, you want to keep them concise and relevant. Avoid adding too much detail that may overwhelm the model.







