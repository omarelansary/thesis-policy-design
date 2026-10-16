import json,subprocess,sys
ws=r"C:\Users\omr\Documents\thesis-policy-design"
cases=[("lead ws-abs ok",{"tool_name":"Write","tool_input":{"file_path":ws+r"\findings\x.md"}},0),
("lead outside abs",{"tool_name":"Write","tool_input":{"file_path":r"C:\Users\omr\Documents\other\x.md"}},2),
("lead ../ escape",{"tool_name":"Write","tool_input":{"file_path":"../x.md"},"cwd":ws},2),
("lead rel ok",{"tool_name":"Write","tool_input":{"file_path":"findings/x.md"},"cwd":ws},0),
("steward traversal to tools",{"tool_name":"Write","tool_input":{"file_path":"findings/../tools/guard.py"},"agent_type":"evidence-steward","cwd":ws},2),
("steward abs traversal to config",{"tool_name":"Edit","tool_input":{"file_path":ws+r"\findings\..\config\ownership.json"},"agent_type":"evidence-steward"},2),
("steward own area",{"tool_name":"Write","tool_input":{"file_path":ws+r"\findings\FND-1.md"},"agent_type":"evidence-steward"},0),
("proposer into steward area",{"tool_name":"Write","tool_input":{"file_path":ws+r"\findings\FND-1.md"},"agent_type":"design-proposer"},2),
("immutable via traversal",{"tool_name":"Write","tool_input":{"file_path":"design/../evidence/governing/INDEX.json"},"cwd":ws},2),
("lead immutable",{"tool_name":"Edit","tool_input":{"file_path":ws+r"\evidence\sources.json"}},2),
("origin write",{"tool_name":"Write","tool_input":{"file_path":r"C:\Users\omr\Documents\research-cleanroom\a.md"}},2),
("bash origin",{"tool_name":"Bash","tool_input":{"command":"cat ../research-cleanroom/CLAUDE.md"}},2),
("bash sanctioned",{"tool_name":"Bash","tool_input":{"command":"python tools/origin_extract.py --list-sources"}},0),
("unknown agent",{"tool_name":"Write","tool_input":{"file_path":"findings/a.md"},"agent_type":"Explore"},2),
("msg to agentId",{"tool_name":"SendMessage","tool_input":{"to":"a18792284f77dc047"}},0),
("msg to main",{"tool_name":"SendMessage","tool_input":{"to":"main"},"agent_type":"design-proposer"},0),
("msg to peer session name",{"tool_name":"SendMessage","tool_input":{"to":"research-cleanroom-21"}},2),
("msg to peer session ref",{"tool_name":"SendMessage","tool_input":{"to":"3ee433"}},2),
("msg to arbitrary name",{"tool_name":"SendMessage","tool_input":{"to":"ping"}},2),
]
bad=0
for n,d,exp in cases:
    r=subprocess.run([sys.executable,"tools/guard.py"],input=json.dumps(d),capture_output=True,text=True,cwd=ws)
    ok=r.returncode==exp; bad+=not ok
    print("PASS" if ok else "FAIL",n,"exit",r.returncode,"expected",exp)
print("failures",bad)
