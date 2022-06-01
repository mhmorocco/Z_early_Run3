from ntuple_processor.utils import Selection


def channel_selection(channel, era):
    if "mm" in channel:
        cuts = [
            ("(pt_1>25. && pt_2>25.)", "acceptance"),
            ("(q_1*q_2 < 0)", "opposite_charge"),
            ("(m_vis > 60. &&  m_vis < 120.)", "Z_mass_window"),
            ("(trg_single_mu24_1 || trg_single_mu24_2)", "trg_matching"),
        ]
        return Selection(name="mm", cuts=cuts)
