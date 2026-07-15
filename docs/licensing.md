# Licensing boundaries

The 0BSD license covers original LFSWeaver code and documentation authored for
this repository. It does not relicense third-party material.

## Upstream books and generated instructions

Linux From Scratch book prose is published under its own documentation license,
while computer instructions have a separate MIT grant. Providers must preserve
the notices that apply to extracted or generated instructions. The project
should prefer fetching pinned upstream sources at build time instead of
vendoring entire books.

## Packages, patches, and artifacts

Every downloaded package and patch retains its own license. A final system image
is an aggregation of many licenses; “the repository is 0BSD” does not mean “the
whole generated Linux system is 0BSD.” Release artifacts must ship a source and
license inventory and satisfy any corresponding-source obligations.

## Reference repositories

Architecture ideas may be reimplemented independently. GPL code must not be
copied into the 0BSD controller. Repositories without an explicit license are
all-rights-reserved by default and likewise must not be copied without
permission.
