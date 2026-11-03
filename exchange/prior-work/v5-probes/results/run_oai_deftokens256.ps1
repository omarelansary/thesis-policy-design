# NOTE: local paths are replaced by placeholders in this published copy; the version that ran had the real paths (hash in RESULTS-R1.md).
$ErrorActionPreference='Stop'
$envf='<adapter service .env>'
function Get-DotEnv($path,$name){ $line=Get-Content $path | Where-Object { $_ -match "^\s*$name\s*=" } | Select-Object -First 1; if(-not $line){return $null}; return (($line -split '=',2)[1]).Trim().Trim('"').Trim("'") }
$k=Get-DotEnv $envf 'OPEN_AI_API_KEY'; if(-not $k){throw 'no key'}; $env:OPENAI_API_KEY=$k
$sp='<scratch>'
$raw='<exchange>/prior-work\v5-probes\results\raw'
python "$sp\p2_tool_choice_probe_oai256.py" --base https://api.openai.com/v1 --key-env OPENAI_API_KEY --model gpt-5-mini --deftokens <local>/appworld-local\appworld_fc_tools.json --sizes 0 10 50 100 200 457 --pause 2 --out "$raw\r3-deftokens-gpt-5-mini-completion256-2026-11-01.json"
Write-Host ("key in output: " + [bool](Select-String -Path "$raw\*.json" -SimpleMatch $env:OPENAI_API_KEY -Quiet))
Remove-Item Env:OPENAI_API_KEY
