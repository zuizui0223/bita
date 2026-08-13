"""Synchronize the saturated Pattern package and one-sided selectivity story."""

from sync_expanded_submission_narrative_base import main as sync_base
from sync_selectivity_readme import main as sync_readme
from sync_selectivity_manuscript_part1 import main as sync_part1
from sync_selectivity_manuscript_part2 import main as sync_part2
from sync_selectivity_manuscript_65 import main as sync_65
from sync_selectivity_manuscript_66 import main as sync_66
from sync_selectivity_manuscript_final_b import main as sync_conclusion
from sync_selectivity_tables import main as sync_tables


def main() -> None:
    sync_base()
    sync_readme()
    sync_part1()
    sync_part2()
    sync_65()
    sync_66()
    sync_conclusion()
    sync_tables()
    print("synchronized saturated Pattern plus one-sided selectivity story")


if __name__ == "__main__":
    main()
