$ErrorActionPreference = 'Stop'
Write-Host 'Step 1: Sign in to your NORMAL Claude profile. Enter any authorization code only in this terminal.'
& 'C:/Users/mathi/.local/bin/claude.exe' auth login --claudeai
if ($LASTEXITCODE -ne 0) { throw 'Claude login did not complete. Stop here and report the displayed error.' }
Write-Host ''
Write-Host 'Step 2: Codex opens next. Enter /hooks and review the verity-plane@se-harness SessionStart hook.'
Write-Host 'Trust only this hook: python .../verity-plane/0.2.0/scripts/inject_instructions.py --host codex'
Write-Host 'Expected current hook hash: sha256:f297274c31689e31abb00ae43e22a718a8e6242311442e65d5007f4d618839ff'
Write-Host 'It reads and delivers the selected repository instructions. It makes no repository or lifecycle changes.'
Write-Host 'After trusting it, exit Codex with /quit and reply Setup complete in this chat.'
& 'C:/Users/mathi/AppData/Local/OpenAI/Codex/bin/faa963e871dd422c/codex.exe' --enable hooks --no-alt-screen --cd 'C:/Users/mathi/Documents/Codex/2026-09-20/verity-plane-plugin-verity-plane-se/work/se_harness'
Write-Host 'Return to the original chat and reply Setup complete. The agent will verify the actual host state.'
