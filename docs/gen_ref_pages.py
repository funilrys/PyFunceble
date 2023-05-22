"""
Generate the code reference pages.
"""

from pathlib import Path

import mkdocs_gen_files

CODE_PATHS = ["PyFunceble"]
DOCPATH = "develop/api-references"

nav = mkdocs_gen_files.Nav()

for code_path in CODE_PATHS:
    for path in sorted(Path(code_path).rglob("*.py")):
        module_path = path.with_suffix("")
        doc_path = path.relative_to(code_path).with_suffix(".md")
        full_doc_path = Path(DOCPATH, doc_path)

        parts = list(module_path.parts)

        if parts[-1] == "__init__":
            parts: list[str] = parts[:-1]
            doc_path = doc_path.with_name("index.md")
            full_doc_path = full_doc_path.with_name("index.md")
        elif parts[-1] == "__main__":
            continue

        nav[parts] = doc_path.as_posix()

        with mkdocs_gen_files.open(full_doc_path, "w") as file_stream:
            identifier = ".".join(parts)
            print("::: " + identifier, file=file_stream)

        mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open(Path(DOCPATH, "SUMMARY.md"), "w") as nav_file_stream:
    nav_file_stream.writelines(nav.build_literate_nav())
