# NOTE: local paths are replaced by placeholders in this published copy; the version that ran had the real paths (hash in RESULTS-R1.md).
# Runs Part 1 and Part 3 of exchange/prior-work/v5-probes/REQUEST-R1.md.
# Run it yourself in a PowerShell window:  powershell -File <this file>
# The keys are read inside this script from the adapter service's .env and are never printed or written.
# Outputs hold only status codes, scrubbed errors, token counts and tool names. A leak check at the end prints True/False only.
param([string[]]$Parts = @('1', '3'), [switch]$SkipScads)
$ErrorActionPreference = 'Stop'
$date   = '2026-11-01'
$probe  = '<exchange>/prior-work\v5-probes\p2_tool_choice_probe.py'
$probeO = '<scratch>\p2_tool_choice_probe_oai.py'
$res    = '<exchange>/prior-work\v5-probes\results'
$raw    = Join-Path $res 'raw'
$defs   = '<local>/appworld-local\appworld_fc_tools.json'
$envf   = '<adapter service .env>'
New-Item -ItemType Directory -Force $raw | Out-Null

function Get-DotEnv($path, $name) {
    $line = Get-Content $path | Where-Object { $_ -match "^\s*$name\s*=" } | Select-Object -First 1
    if (-not $line) { return $null }
    return (($line -split '=', 2)[1]).Trim().Trim('"').Trim("'")
}

# ScaDS key: first LLM_API_KEY, then EVAL_LLM_API_KEY
$k = Get-DotEnv $envf 'LLM_API_KEY'
if (-not $k) { $k = Get-DotEnv $envf 'EVAL_LLM_API_KEY' }
if (-not $k) { throw 'No LLM_API_KEY or EVAL_LLM_API_KEY in the service .env' }
$env:SCADS_API_KEY = $k
# OpenAI key: an existing environment variable, else OPENAI_API_KEY in the same .env, else the OpenAI runs are skipped
if (-not $env:OPENAI_API_KEY) {
    $o = Get-DotEnv $envf 'OPENAI_API_KEY'
    if (-not $o) { $o = Get-DotEnv $envf 'OPEN_AI_API_KEY' }
    if ($o) { $env:OPENAI_API_KEY = $o }
}

# Auth check: status codes only
$code = (curl.exe -s -o NUL -w '%{http_code}' -H "Authorization: Bearer $env:SCADS_API_KEY" https://llm.scads.ai/v1/models)
Write-Host "ScaDS /v1/models auth check: HTTP $code"
if ($code -ne '200') { throw 'ScaDS key not accepted; stopping before any probe' }
$haveOpenAI = [bool]$env:OPENAI_API_KEY
if ($haveOpenAI) {
    $code2 = (curl.exe -s -o NUL -w '%{http_code}' -H "Authorization: Bearer $env:OPENAI_API_KEY" https://api.openai.com/v1/models)
    Write-Host "OpenAI /v1/models auth check: HTTP $code2"
    if ($code2 -ne '200') { $haveOpenAI = $false; Write-Host 'OpenAI key not accepted; OpenAI runs skipped' }
} else { Write-Host 'No OpenAI key found; OpenAI runs skipped' }

$scads = @('deepseek-ai/DeepSeek-V4.1-Flash', 'google/gemma-4-26B-A4B-it', 'meta-llama/Llama-3.3-70B-Instruct',
           'MiniMaxAI/MiniMax-M3', 'MiniMaxAI/MiniMax-M3.1-Flash', 'openai/gpt-oss-120b', 'Qwen/Qwen3.8-27B',
           'zai-org/GLM-5.3', 'zai-org/GLM-5.3-Flash', 'alias-code')

if ($Parts -contains '1') {
    if (-not $SkipScads) { foreach ($m in $scads) {
        $slug = $m -replace '[\\/]', '__'
        python $probe --base https://llm.scads.ai/v1 --key-env SCADS_API_KEY --model $m --max-tokens 1024 --pause 15 --out (Join-Path $raw "r1-scads-$slug-$date.json")
    } }
    if ($haveOpenAI) {
        # gpt-4.1-mini accepts max_tokens: unmodified script. gpt-5-mini needs max_completion_tokens: separate copy.
        python $probe  --base https://api.openai.com/v1 --key-env OPENAI_API_KEY --model gpt-4.1-mini --max-tokens 1024 --pause 2 --out (Join-Path $raw "r1-openai-gpt-4.1-mini-$date.json")
        python $probeO --base https://api.openai.com/v1 --key-env OPENAI_API_KEY --model gpt-5-mini  --max-tokens 1024 --pause 2 --out (Join-Path $raw "r1-openai-gpt-5-mini-$date.json")
    }
}
if ($Parts -contains '3') {
    $non = $scads | Where-Object { $_ -ne 'alias-code' }
    if (-not $SkipScads) { foreach ($m in $non) {
        $slug = $m -replace '[\\/]', '__'
        python $probe --base https://llm.scads.ai/v1 --key-env SCADS_API_KEY --model $m --deftokens $defs --sizes 0 10 50 100 200 457 --pause 15 --out (Join-Path $raw "r3-deftokens-$slug-$date.json")
    } }
    if ($haveOpenAI) {
        python $probe  --base https://api.openai.com/v1 --key-env OPENAI_API_KEY --model gpt-4.1-mini --deftokens $defs --sizes 0 10 50 100 200 457 --pause 2 --out (Join-Path $raw "r3-deftokens-gpt-4.1-mini-$date.json")
        python $probeO --base https://api.openai.com/v1 --key-env OPENAI_API_KEY --model gpt-5-mini  --deftokens $defs --sizes 0 10 50 100 200 457 --pause 2 --out (Join-Path $raw "r3-deftokens-gpt-5-mini-$date.json")
    }
}

# Leak check: prints only True/False
$leakS = Select-String -Path (Join-Path $raw '*.json') -SimpleMatch $env:SCADS_API_KEY -Quiet
Write-Host "ScaDS key string present in any output file: $([bool]$leakS)"
if ($env:OPENAI_API_KEY) {
    $leakO = Select-String -Path (Join-Path $raw '*.json') -SimpleMatch $env:OPENAI_API_KEY -Quiet
    Write-Host "OpenAI key string present in any output file: $([bool]$leakO)"
}
Remove-Item Env:SCADS_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue
Write-Host "Done. Outputs in $raw"
