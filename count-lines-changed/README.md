Count Lines Changed
===

Will count the total lines added into the repository in the given commit range
(as specified by Git). If no range is given, then count for all commits
in the current branch.


Example usage
====

	count-lines-changed.sh HEAD~1..HEAD
	  => added: 19, subbed: 2, total: 17

	count-lines-changed.sh master..develop
	  => added: 19, subbed: 2, total: 17
