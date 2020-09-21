#!/usr/bin/env python

from hAMRonization.hAMRonizedResult import hAMRonizedResult

from hAMRonization import AbricateIO
from hAMRonization import AmrFinderPlusIO
#from hAMRonization import AribaIO
#from hAMRonization import RgiIO
#from hAMRonization import ResFinderIO
#from hAMRonization import SraxIO
#from hAMRonization import DeepArgIO
#from hAMRonization import KmerResistanceIO
#from hAMRonization import Srst2IO
#from hAMRonization import GrootIO
#from hAMRonization import StarAmrIO
#from hAMRonization import CSStarIO
#from hAMRonization import AmrPlusPlusIO
#from hAMRonization import ResFamsIO


_FormatToIterator = {
    "abricate": AbricateIO.AbricateIterator,
    "amrfinderplus": AmrFinderPlusIO.AmrFinderPlusIterator,
    #"ariba": AribaIO.AribaIterator,
    #"rgi": RgiIO.RgiIterator,
    #"resfinder": ResFinderIO.ResFinderIterator,
    #"srax": SraxIO.SraxIterator,
    #"deeparg": DeepArgIO.DeepArgIterator,
    #"kmerresistance": KmerResistanceIO.KmerResistanceIterator,
    #"srst2": Srst2IO.Srst2Iterator,
    #"groot": GrootIO.GrootIterator,
    #"staramr": StarAmrIO.StarAmrIterator,
    #"csstar": CSStarIO.CSStarIterator,
    #"amrplusplus": AmrPlusPlusIO.AmrPlusPlusIterator,
    #"resfams": ResFamsIO.ResFamsIterator
    }

_RequiredToolMetadata = {
    "abricate": AbricateIO.required_metadata,
    "amrfinderplus": AmrFinderPlusIO.required_metadata,
}

def parse(handle, metadata, tool):
    r"""Turn a sequence file into an iterator returning SeqRecords.
    Arguments:
     - handle   - handle to the file, or the filename as a string
     - tool - lower case string describing the file format.
     - required_arguments - dictionary containing the required arguments for tool
    Typical usage, opening a file to read in, and looping over the record(s):
    >>> import hAMRonization
    >>> filename = "abricate_report.tsv"
    >>> metadata = {"analysis_software_version": "1.0.1", "reference_database_version": "2019-Jul-28"}
    >>> for result in hAMRonization.parse(filename, required_arguments, "abricate"):
    ...    print(record)

    """
    if not isinstance(tool, str):
        raise TypeError("Need a string for the file format (lower case)")
    if not isinstance(metadata, dict):
        raise TypeError("Metadata must be provided as a dictionary")
    if not tool:
        raise ValueError("Tool required (lower case string)")
    if not tool.islower():
        raise ValueError(f"Tool string '{tool}' should be lower case")

    # check all required metadata has been provided
    try:
        tool_required_metadata = _RequiredToolMetadata[tool]
    except KeyError:
        raise ValueError(f"Unknown tool: {tool}\nMust be in {_RequiredToolMetadata.keys()}")
    missing_data = []
    for required in tool_required_metadata:
        if required not in metadata:
            missing_data.append(required)
    if missing_data:
        raise ValueError(f"{tool} requires {missing_data} supplied in metadata dictionary")

    iterator_generator = _FormatToIterator.get(tool)
    if iterator_generator:
        return iterator_generator(handle, metadata)
    raise ValueError(f"Unknown tool: {tool}\nMust be in {_FormatToIterator.keys()}")