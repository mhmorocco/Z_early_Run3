from ntuple_processor.utils import Selection


def channel_selection(channel, era):
    if "mm" in channel:
        cuts = [("pt_1>30 && pt_2>20", "trg_selection")]
        return Selection(name="mm", cuts=cuts)
