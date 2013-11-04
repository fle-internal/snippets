git log --oneline --shortstat -C $1 | \
    grep -E 'file[s]? changed' | \
    perl -lan -e  'BEGIN{ $added=0; $subbed=0 } $added+=$F[3]; $subbed+=$F[5];  END{ $total=$added - $subbed; print "added: $added, subbed: $subbed, total=$total"}'
