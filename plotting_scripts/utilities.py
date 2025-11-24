import July_2025_TID_utils as julyUtils


marker_cycle = ['v','^','<','>', 'x', '+']

def plot_TID_end(ax, cobs, plot50mA=False):
    _xlim = ax.get_xlim()
    _ylim = ax.get_ylim()
    for i, _COB_ in enumerate(cobs):
        if plot50mA:
            _xray_50 = julyUtils.getTID(julyUtils._xray_times[_COB_]['Xray 50'],_COB_)
            ax.vlines(_xray_50, _ylim[0]+i*0.1, _ylim[1],linestyles='dotted',color=julyUtils.color_cycle[i],linewidth=2,)
    
        _xray_Off = julyUtils.getTID(julyUtils._xray_times[_COB_]['Xray Off'], _COB_)
        ax.vlines(_xray_Off, _ylim[0]+i*0.05, _ylim[1],linestyles='dashed',color=julyUtils.color_cycle[i],linewidth=2,)