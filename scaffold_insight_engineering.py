# scaffold_insight_engineering.py
# يَبنـي هيكل مشروع: "هندسة البصيرة – Insight Engineering"
# الاستخدام:
#   python scaffold_insight_engineering.py
#   python scaffold_insight_engineering.py --dest "D:/Work" --overwrite

from pathlib import Path
import argparse
import textwrap

APP_NAME_AR = "هندسة البصيرة"
APP_NAME_EN = "Insight Engineering"
PROJECT_ROOT = "insight_engineering"

DIRS = [
    "apps",
    "apps/desktop",
    "apps/desktop/ui",
    "apps/desktop/ui/icons",
    "apps/desktop/ui/styles",
    "apps/desktop/resources",
    "apps/desktop/resources/qrc",
    "core",
    "core/features",
    "core/graph",
    "core/dynamics",
    "core/scoring",
    "core/explain",
    "core/guidance",
    "core/storage",
    "core/utils",
    "api",
    "configs",
    "data",
    "data/samples",
    "data/dictionaries",
    "assets",
    "assets/logos",
    "assets/fonts",
    "assets/figures",
    "notebooks",
    "scripts",
    "tests",
]

FILES = {
    # جذور المشروع
    "README.md": f"# {APP_NAME_AR} – {APP_NAME_EN}\n\nمشروع هيكل أولي (Skeleton) للتطبيق.\n",
    "LICENSE": "MIT License\n\nCopyright (c) ",
    ".gitignore": textwrap.dedent("""
        __pycache__/
        *.pyc
        *.pyo
        .Python
        .env
        .venv
        venv/
        env/
        .idea/
        .vscode/
        *.sqlite3
        .DS_Store
        .pytest_cache/
        .mypy_cache/
        .coverage
        dist/
        build/
        *.egg-info/
    """).strip()+"\n",
    ".env.example": "APP_ENV=dev\nSECRET_KEY=change_me\n",
    "pyproject.toml": textwrap.dedent(f"""
        [project]
        name = "insight-engineering"
        version = "0.1.0"
        description = "{APP_NAME_AR} – {APP_NAME_EN}"
        authors = [{{name = "Dr. Taha Abdelaal"}}]
        readme = "README.md"
        requires-python = ">=3.9"

        [tool.setuptools.packages.find]
        where = ["."]
    """).strip()+"\n",
    "requirements.txt": textwrap.dedent("""
        streamlit
        pydantic
        fastapi
        uvicorn
        numpy
        scipy
        matplotlib
        networkx
        sqlite-utils
    """).strip()+"\n",
    "setup.cfg": textwrap.dedent("""
        [flake8]
        max-line-length = 100
        extend-ignore = E203,W503

        [tool:pytest]
        addopts = -q
    """).strip()+"\n",
    "Makefile": textwrap.dedent("""
        .PHONY: run-web run-api test

        run-web:
\t\tstreamlit run apps/streamlit_app.py

        run-api:
\t\tuvicorn api.server:app --reload

        test:
\t\tpytest -q
    """).replace("        ", "").strip()+"\n",

    # apps
    "apps/streamlit_app.py": textwrap.dedent(f"""
        # Placeholder entry for Streamlit UI
        import streamlit as st

        st.set_page_config(page_title="{APP_NAME_AR} – {APP_NAME_EN}", layout="centered")
        st.title("{APP_NAME_AR} – {APP_NAME_EN}")
        st.write("هيكل أولي جاهز. أضف المنطق من مجلد core/ لاحقًا.")
    """).strip()+"\n",

    "apps/desktop/main.py": textwrap.dedent(f"""
        # Placeholder entry for PyQt6 desktop app (لا يعتمد عليه البناء)
        # عند التفعيل: pip install PyQt6
        try:
            from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
            import sys
            def main():
                app = QApplication(sys.argv)
                w = QMainWindow()
                w.setWindowTitle("{APP_NAME_AR} – {APP_NAME_EN}")
                lbl = QLabel("{APP_NAME_AR} – {APP_NAME_EN}")
                w.setCentralWidget(lbl)
                w.resize(640, 400)
                w.show()
                sys.exit(app.exec())
            if __name__ == "__main__":
                main()
        except Exception:
            # ملف واجهة تجريبي فقط
            pass
    """).strip()+"\n",

    "apps/desktop/ui/main_window.ui": "<ui><!-- Qt Designer placeholder --></ui>\n",

    # core
    "core/__init__.py": "",
    "core/config.py": textwrap.dedent("""
        # حمل الإعدادات العامة لاحقًا (YAML/ENV)
        APP_TITLE_AR = "هندسة البصيرة"
        APP_TITLE_EN = "Insight Engineering"
    """).strip()+"\n",
    "core/data_models.py": textwrap.dedent("""
        # ضع نماذج البيانات (Pydantic/Dataclasses) هنا لاحقًا
        # from pydantic import BaseModel
        # class Session(BaseModel): ...
        pass
    """).strip()+"\n",
    "core/questionnaire.py": "pass\n",

    "core/features/__init__.py": "",
    "core/features/text_features.py": "pass\n",
    "core/features/audio_features.py": "pass\n",
    "core/features/signal_features.py": "pass\n",

    "core/graph/__init__.py": "",
    "core/graph/builder.py": "pass\n",
    "core/graph/laplacian.py": "pass\n",
    "core/graph/metrics.py": "pass\n",

    "core/dynamics/__init__.py": "",
    "core/dynamics/ode_models.py": "pass\n",
    "core/dynamics/simulators.py": "pass\n",

    "core/scoring/__init__.py": "",
    "core/scoring/indices.py": "pass\n",
    "core/scoring/aggregators.py": "pass\n",

    "core/explain/__init__.py": "",
    "core/explain/attribution.py": "pass\n",

    "core/guidance/__init__.py": "",
    "core/guidance/rules.py": "pass\n",
    "core/guidance/planner.py": "pass\n",

    "core/storage/__init__.py": "",
    "core/storage/db.py": "pass\n",
    "core/storage/repository.py": "pass\n",

    "core/utils/__init__.py": "",
    "core/utils/io.py": "pass\n",
    "core/utils/plotting.py": "pass\n",
    "core/utils/validators.py": "pass\n",

    # api
    "api/__init__.py": "",
    "api/schemas.py": "pass\n",
    "api/server.py": textwrap.dedent("""
        # FastAPI placeholder (اختياري)
        try:
            from fastapi import FastAPI
            app = FastAPI(title="Insight Engineering API")
            @app.get("/")
            def root():
                return {"status": "ok"}
        except Exception:
            app = None
    """).strip()+"\n",

    # configs
    "configs/app.yaml": textwrap.dedent("""
        title_ar: "هندسة البصيرة"
        title_en: "Insight Engineering"
        env: dev
    """).strip()+"\n",
    "configs/questionnaire.yaml": textwrap.dedent("""
        facets: ["Mind","Heart","Body","Spirit","Relations","Work"]
        default_score: 70
    """).strip()+"\n",
    "configs/graph.yaml": textwrap.dedent("""
        nodes: ["Mind","Heart","Body","Spirit","Relations","Work"]
        edges:
          - ["Mind","Spirit", 0.5]
          - ["Heart","Relations", 0.6]
    """).strip()+"\n",
    "configs/guidance.yaml": textwrap.dedent("""
        rules:
          - facet: "Mind"
            tip: "5 دقائق تنفس واعٍ + تدوين سريع."
    """).strip()+"\n",

    # data
    "data/samples/demo_sessions.csv": "session_id,user_id,avg_score\n1,100,72\n",
    "data/samples/demo_texts.txt": "Sample notes...\n",
    "data/dictionaries/stopwords.txt": "the\na\nof\n",
    "data/dictionaries/lexicons.json": "{\n  \"calm\": 1,\n  \"stress\": -1\n}\n",

    # assets
    "assets/logos/arabic_logo.svg": "<svg><!-- Arabic logo placeholder --></svg>\n",
    "assets/logos/bilingual_lockup.svg": "<svg><!-- Bilingual lockup placeholder --></svg>\n",

    # notebooks
    "notebooks/exploration.ipynb": "",
    "notebooks/dynamics_experiments.ipynb": "",

    # scripts
    "scripts/init_db.py": "print('init db placeholder')\n",
    "scripts/export_report.py": "print('export report placeholder')\n",
    "scripts/ingest_demo.py": "print('ingest demo placeholder')\n",

    # tests
    "tests/__init__.py": "",
    "tests/test_scoring.py": "def test_ok(): assert True\n",
    "tests/test_graph.py": "def test_ok(): assert True\n",
    "tests/test_dynamics.py": "def test_ok(): assert True\n",
    "tests/test_guidance.py": "def test_ok(): assert True\n",
    "tests/test_storage.py": "def test_ok(): assert True\n",
}

def write_file(base: Path, rel_path: str, content: str, overwrite: bool = False):
    path = base / rel_path
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        return
    path.write_text(content, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Scaffold Insight Engineering project.")
    parser.add_argument("--dest", type=str, default=".", help="Destination directory")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    dest_root = Path(args.dest).resolve() / PROJECT_ROOT
    dest_root.mkdir(parents=True, exist_ok=True)

    # إنشاء المجلدات
    for d in DIRS:
        (dest_root / d).mkdir(parents=True, exist_ok=True)

    # إنشاء الملفات
    for rel, content in FILES.items():
        write_file(dest_root, rel, content, overwrite=args.overwrite)

    print(f"✅ تم إنشاء الهيكل في: {dest_root}")

if __name__ == "__main__":
    main()
