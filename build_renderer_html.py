import re

with open("docs/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Replace the dynamic init/manifest fetch with SPEC = __SPEC__
renderer_content = re.sub(
    r"let currentSpec = null;.*?init\(\);",
    r"""const SPEC = __SPEC__;
currentSpec = SPEC;
window.addEventListener("DOMContentLoaded", () => {
    setSpec(SPEC);
});""",
    content,
    flags=re.DOTALL
)

# Remove the upload modal and tunnel modal buttons from the renderer for self-contained output
with open("renderer.html", "w", encoding="utf-8") as f:
    f.write(renderer_content)

print("renderer.html updated with elite design system and __SPEC__ injection point!")
