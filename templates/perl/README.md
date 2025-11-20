Hauke's Perl Snippets
=====================

Note on One-Liners
------------------

I generally use `perl -wM5.014` because:
- It's low enough to be available everywhere ([released 2011](https://perldoc.perl.org/perlhist#THE-RECORDS))
- That's when [JSON::PP](https://perldoc.perl.org/5.14.0/JSON::PP),
  [HTTP::Tiny](https://perldoc.perl.org/5.14.0/HTTP::Tiny),
  and `s///r` were [added](https://perldoc.perl.org/perl5140delta)
- [`use 5.014`](https://perldoc.perl.org/functions/use#use-VERSION) also turns on `strict`
  and [enables](https://perldoc.perl.org/feature#FEATURE-BUNDLES) `say`
