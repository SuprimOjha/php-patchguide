"""Text and JSON reports."""
import json
def build_report(project,findings):
    states=[f["status"] for f in findings]
    return {"tool":"PHP PatchGuide","schema_version":"1.0","project":project,"summary":{"advisory_count":len(findings),"affected":states.count("affected"),"fixed":states.count("fixed"),"unknown":states.count("unknown")},"findings":findings,"limitations":["CLI version may differ from serving runtime.","Version checks cannot reliably detect vendor backports.","Local advisory data is not exhaustive."]}
def format_json(report): return json.dumps(report,indent=2,sort_keys=True)
def format_text(report):
    p=report["project"]; version=p.get("cli_runtime",{}).get("version") or "not detected"
    lines=["PHP PatchGuide","Project: "+p.get("path","?"),"PHP project detected: "+("yes" if p.get("is_php_project") else "not confirmed"),"PHP CLI version: "+version,"Advisory findings: "+str(report["summary"]["advisory_count"]),""] 
    if not report["findings"]: lines.append("No local advisory records were loaded.")
    for f in report["findings"]:
        lines.append("{} {} [{}] {}".format(f["severity"].upper(),f["id"],f["status"],f["message"]))
        if f.get("url"): lines.append("         Source: "+f["url"])
    lines += ["","Runtime note: "+p.get("runtime_warning",""),"Verify official vendor guidance before upgrading."]
    return "\n".join(lines)
