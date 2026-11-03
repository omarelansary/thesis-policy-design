# NOTE: local paths are replaced by placeholders in this published copy; the version that ran had the real paths (hash in RESULTS-R2.md).
# Runs Part A1 of exchange/prior-work/v5-probes/REQUEST-R2.md with p2_tool_choice_probe_v2.py (unmodified).
# The keys are read inside this script from the adapter service's .env and are never printed or written.
# One output file per model (so a crash loses at most one model); merge_r2_a1.py joins them into the files named in the request.
param([switch]$SkipScads, [switch]$SkipOpenAI)
$ErrorActionPreference = 'Stop'
$date   = '2026-11-02'
$probe  = '<exchange>/prior-work\v5-probes\p2_tool_choice_probe_v2.py'
$res    = '<exchange>/prior-work\v5-probes\results\R2'
$raw    = Join-Path $res 'raw'
$envf   = '<adapter service .env>'
New-Item -ItemType Directory -Force $raw | Out-Null
$env:PYTHONUTF8 = '1'

function Get-DotEnv($path, $name) {
    $line = Get-Content $path | Where-Object { $_ -match "^\s*$name\s*=" } | Select-Object -First 1
    if (-not $line) { return $null }
    return (($line -split '=', 2)[1]).Trim().Trim('"').Trim("'")
}

$k = Get-DotEnv $envf 'LLM_API_KEY'
if (-not $k) { $k = Get-DotEnv $envf 'EVAL_LLM_API_KEY' }
if (-not $k) { throw 'No LLM_API_KEY or EVAL_LLM_API_KEY in the service .env' }
$env:SCADS_API_KEY = $k
$o = Get-DotEnv $envf 'OPENAI_API_KEY'
if (-not $o) { $o = Get-DotEnv $envf 'OPEN_AI_API_KEY' }
if ($o) { $env:OPENAI_API_KEY = $o }

$code = (curl.exe -s -o NUL -m 20 -w '%{http_code}' -H "Authorization: Bearer $env:SCADS_API_KEY" https://llm.scads.ai/v1/models)
Write-Host "ScaDS /v1/models auth check: HTTP $code"
if ($code -ne '200') { throw 'ScaDS key not accepted; stopping before any probe' }
$haveOpenAI = [bool]$env:OPENAI_API_KEY
if ($haveOpenAI) {
    $code2 = (curl.exe -s -o NUL -m 20 -w '%{http_code}' -H "Authorization: Bearer $env:OPENAI_API_KEY" https://api.openai.com/v1/models)
    Write-Host "OpenAI /v1/models auth check: HTTP $code2"
    if ($code2 -ne '200') { $haveOpenAI = $false; Write-Host 'OpenAI key not accepted; OpenAI runs skipped' }
} else { Write-Host 'No OpenAI key found; OpenAI runs skipped' }

$scads = @('deepseek-ai/DeepSeek-V4.1-Flash', 'google/gemma-4-26B-A4B-it', 'meta-llama/Llama-3.3-70B-Instruct',
           'MiniMaxAI/MiniMax-M3', 'MiniMaxAI/MiniMax-M3.1-Flash', 'openai/gpt-oss-120b', 'Qwen/Qwen3.8-27B',
           'zai-org/GLM-5.3', 'zai-org/GLM-5.3-Flash')

if ($haveOpenAI -and -not $SkipOpenAI) {
    python $probe --base https://api.openai.com/v1 --key-env OPENAI_API_KEY --model gpt-4.1-mini --cells C2 C4 C6 C8 C9 --repeat 5 --max-tokens 1024 --pause 2 --out (Join-Path $raw "r2-openai-gpt-4.1-mini-$date.json")
    python $probe --base https://api.openai.com/v1 --key-env OPENAI_API_KEY --model gpt-5-mini --token-param max_completion_tokens --cells C2 C4 C6 C8 C9 --repeat 5 --max-tokens 1024 --pause 2 --out (Join-Path $raw "r2-openai-gpt-5-mini-$date.json")
}
if (-not $SkipScads) { foreach ($m in $scads) {
    $slug = $m -replace '[\\/]', '__'
    python $probe --base https://llm.scads.ai/v1 --key-env SCADS_API_KEY --model $m --cells C2 C4 C6 C8 C9 --repeat 5 --max-tokens 1024 --pause 15 --out (Join-Path $raw "r2-scads-$slug-$date.json")
} }

$leakS = Select-String -Path (Join-Path $raw '*.json') -SimpleMatch $env:SCADS_API_KEY -Quiet
Write-Host "ScaDS key string present in any output file: $([bool]$leakS)"
if ($env:OPENAI_API_KEY) {
    $leakO = Select-String -Path (Join-Path $raw '*.json') -SimpleMatch $env:OPENAI_API_KEY -Quiet
    Write-Host "OpenAI key string present in any output file: $([bool]$leakO)"
}
Remove-Item Env:SCADS_API_KEY -ErrorAction SilentlyContinue
Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue
Write-Host "Done. Outputs in $raw"
