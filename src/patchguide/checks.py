"""Compare PHP versions to fixed releases."""
from patchguide.versions import compare_versions, parse_version
def evaluate_advisories(version,advisories):
    parsed=parse_version(version or ""); findings=[]
    for item in advisories:
        fixed=None
        if parsed is None: status,message="unknown","PHP version not detected; verify serving runtime."
        else:
            series="{}.{}".format(parsed[0],parsed[1]); fixed=item.get("fixed_by",{}).get(series)
            if not fixed: status,message="unknown","No fixed-version rule for PHP {}.".format(series)
            elif compare_versions(version,fixed)==-1: status,message="affected","Update to {} or later, or verify vendor backports.".format(fixed)
            else: status,message="fixed","Version is at or above recorded fix {}.".format(fixed)
        findings.append({"id":item.get("id"),"title":item.get("title"),"severity":item.get("severity","unknown"),"status":status,"current_version":version,"fixed_version":fixed,"message":message,"url":item.get("url")})
    return findings
