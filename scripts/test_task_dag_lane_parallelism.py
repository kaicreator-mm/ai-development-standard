from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    template = read("templates/task-dag.md")
    l2_prompt = read("prompts/L2_ARCHITECTURE_EVIDENCE.md")
    workflow = read("standards/DEVELOPMENT_WORKFLOW.md")

    required_template = (
        "## Lane-Oriented Decomposition Prompt",
        "maximum safe parallelism",
        "| Task | Issue | Lane | Depends On | Parallel |",
        "## Lane Summary",
        "explicit convergence/integration Task",
        "Do not declare parallel lanes to bypass a real Issue Dependency",
        "Lane                  = planning hint for safe concurrency/ownership, not authority",
    )
    for token in required_template:
        assert token in template, f"task-dag template missing lane guidance: {token}"

    required_l2 = (
        "ownership/write-set boundaries",
        "maximum safe parallelism",
        "Task DAG Lane Hints",
        "Lane-Oriented Decomposition Prompt",
    )
    for token in required_l2:
        assert token in l2_prompt, f"L2 prompt missing lane handoff: {token}"

    assert "- parallelism；" in workflow, "Development Workflow no longer requires Task DAG parallelism"
    assert "GitHub Issue Dependencies = canonical live execution DAG" in workflow, (
        "lane planning must not replace canonical Issue Dependency authority"
    )

    forbidden = (
        "Lane = canonical live execution DAG",
        "Lane replaces Issue Dependency",
        "Parallel=YES means dependency-free",
    )
    for token in forbidden:
        assert token not in template, f"unsafe lane authority wording detected: {token}"

    print("Task DAG lane parallelism guidance: PASS")


if __name__ == "__main__":
    main()
