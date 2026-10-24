# FAQ

**Does PatchGuide upgrade PHP?** No, it is read-only.

**Does it replace Composer audit?** No; its initial dataset focuses on PHP runtime advisories.

**Why unknown?** The version is unavailable or the database has no rule for that series. Unknown does not mean safe.

**Why a warning after a vendor update?** A vendor may backport a fix without changing the upstream-looking version. Review the vendor notice.

**Does monitoring update records automatically?** No.
