<h1 class="libTop">daemon-spec</h1>

This is a brief description of a Python 3 wrapper for modules that
allows them to be run as a proper daemon.  Initially at least this
capability will be confined to Linux systms and possibly only to
Debian and Ubuntu distributions.

Tenatively this behavior will be built on top of `python-daemon` and
its `DaemonContext`.

For the purposes of this document we will assume that the daemon
package is called `zDaemon` and that there is a companiion locking
facility `zLocks` which is expected to be a separate module.

## Daemonization Candidates

We assume that any program to be daemonized using this module will

* accept options through `sys.argv`
* expect to store and retrieve files through paths relative to its
    current directory

## Expected Implementation Style

Call the program to be daemonized `Candidate`.  Typically this will
be packaged as a separate module, perhaps `candidate.py`.  This should
have a conventional Python entry point `main()`, so that the last two
lines of `candidate.py` are

    if _name__ == '__main__':
        main()

Then the program can be run as a standalone script using

    PATH_TO_SCRIPT/candidate/main() ARGV

where ARGV represents the usual sequence of arguments passed through
`sys.argv`.

`zDaemon` is invoked similarl

    zDaemon ARGV

with the understanding that `zDaemon` will consume at least some of the
leading arguments, stripping them off before passing the remaining
arguments to the candidate.

This allows the candidate program to be thoroughly tested independently
of `zDaemon`.
