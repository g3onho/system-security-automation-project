"""진단영역별 Ansible 실행 위치와 파일 이름을 한 곳에서 관리한다."""
from dataclasses import dataclass
from pathlib import Path

# dashboard/backend/runtime.py → 저장소 루트
PROJECT_ROOT = Path(__file__).resolve().parents[2]
# 진단영역별 Ansible 프로젝트(unix/, web/, dbms/)와 통합 인벤토리가 있는 위치
ANSIBLE_ROOT = PROJECT_ROOT / "ansible"
UNIFIED_INVENTORY = ANSIBLE_ROOT / "inventory" / "hosts.ini"

@dataclass(frozen=True)
class DomainRuntime:
    name: str
    root: Path
    inventory: Path
    deploy_playbook: str | None
    check_playbook: str
    audit_playbook: str
    remediate_playbook: str
    check_report_suffix: str
    audit_report_suffix: str

    @property
    def reports_dir(self) -> Path:
        return self.root / "reports"

RUNTIMES = {
    "UNIX": DomainRuntime(
        "UNIX",
        ANSIBLE_ROOT / "unix",
        ANSIBLE_ROOT / "unix" / "inventory" / "hosts.ini",
        "playbooks/deploy.yml",
        "playbooks/check.yml",
        "playbooks/audit.yml",
        "playbooks/remediate_approved.yml",
        "_check.json",
        "_audit.json",
    ),
    "WEB": DomainRuntime(
        "WEB",
        ANSIBLE_ROOT / "web",
        ANSIBLE_ROOT / "web" / "inventory" / "hosts.ini",
        "playbooks/deploy.yml",
        "playbooks/check.yml",
        "playbooks/audit.yml",
        "playbooks/remediate_approved.yml",
        "_check.json",
        "_audit.json",
    ),
    "DBMS": DomainRuntime(
        "DBMS",
        ANSIBLE_ROOT / "dbms",
        ANSIBLE_ROOT / "dbms" / "inventory" / "hosts.ini",
        "playbooks/deploy.yml",
        "playbooks/check.yml",
        "playbooks/audit.yml",
        "playbooks/remediate_approved.yml",
        "_mysql_dbms_check.json",
        "_remediate.json",
    ),
}

def domain_for_code(code: str) -> str:
    normalized = code.strip().upper()
    if normalized.startswith("WEB-"):
        return "WEB"
    if normalized.startswith("D-"):
        return "DBMS"
    if normalized.startswith("U-"):
        return "UNIX"
    raise ValueError(f"지원하지 않는 점검 코드입니다: {code}")
