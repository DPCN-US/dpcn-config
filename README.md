# DPCN System Configuration Repo

![Python application](https://github.com/DPCN-US/dpcn-config/workflows/Python%20application/badge.svg)

DPCN system configurations are stored in the [systems](systems) folder.

To generate a list of system radio IDs, talkgroup IDs, and channel codes, run the `gen-codes.py` command.

ℹ️️ System administrators: Save the output to a text file when you apply the configuration.
That way in the future you will be able to run a `diff` against a previous configuration and save yourself the headache 
of a lengthy and painful "stare and compare."

```bash
python gen-config.py > `date +%Y-%m-%d_dpcn-config.txt`
```