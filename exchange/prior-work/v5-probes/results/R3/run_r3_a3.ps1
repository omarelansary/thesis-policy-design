# NOTE: local paths replaced by placeholders in this published copy. The key is read inside this script from the adapter service .env and never printed or written.
$ErrorActionPreference = 'Stop'
$probe = '<exchange>\prior-work\v5-probes\p2_tool_choice_probe_v3.py'
$res   = '<exchange>\prior-work\v5-probes\results\R3'
$envf  = '<adapter service .env>'
New-Item -ItemType Directory -Force $res | Out-Null
$env:PYTHONUTF8 = '1'
$line = Get-Content -LiteralPath $envf | Where-Object { $_ -match '^\s*OPENROUTER_API_KEY\s*=' } | Select-Object -First 1
if (-not $line) { throw 'No OPENROUTER_API_KEY in the .env file' }
$env:OPENROUTER_API_KEY = $line.Split('=', 2)[1].Trim().Trim('"', "'").Trim()
$code = (curl.exe -s -o NUL -m 20 -w '%{http_code}' -H "Authorization: Bearer $env:OPENROUTER_API_KEY" https://openrouter.ai/api/v1/auth/key)
Write-Host "OpenRouter key check: HTTP $code"
if ($code -ne '200') { throw 'key not accepted; stopping before any probe' }
Write-Host ('start UTC ' + [DateTime]::UtcNow.ToString('s'))
$eb = '{\"provider\":{\"order\":[\"gmicloud/fp8\"],\"allow_fallbacks\":false}}'
python $probe --base https://openrouter.ai/api/v1 --key-env OPENROUTER_API_KEY --model minimax/minimax-m3 --repeat 3 --max-tokens 1024 --pause 2 --extra-body $eb --out (Join-Path $res 'r3-openrouter-gmicloud-2026-11-02.json')
Write-Host ('exit ' + $LASTEXITCODE + ' end UTC ' + [DateTime]::UtcNow.ToString('s'))
Remove-Item Env:OPENROUTER_API_KEY -ErrorAction SilentlyContinue
