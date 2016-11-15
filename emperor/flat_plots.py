import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_3x3(ordination, offset, mapping, field, colors, null_kw=None,
             focus_kw=None):
    """Construct a 3 x 3 plot of PC combinations

    Where X is a PCn / PCm plot, _ is a blank spot, and L is the legend.

    Offset defines the starting offset for the rows. If zero, the layout
    is:

    PC1v2 PC1v3 PC1v4 BLANK
    PC2v3 PC2v4 PC2v5 Legend
    PC3v4 PC3v5 PC3v6 BLANK

    Notes
    -----
    This is ridged and defined layout intended to faciliate examining a large
    number of PCs over different metadata categories. Specifically, the layout
    constraints force the location of the plots and points within each plot 
    to be consistent thereby making viewing of different metadata fields
    easy as your perspective remains fixed. 

    Parameters
    ----------
    ordination : OrdinationResults
        An OrdinationResults object
    offset : int
        The starting ordination axis (e.g., 0 in the above example as 0 maps
        to PC1).
    mapping : DataFrame
        DataFrame object with the metadata associated to the samples in the
        ``ordination`` object, should have an index set and it should match the
        identifiers in the ``ordination`` object.
    field : str
        The field within the mapping file to use for coloring.
    colors : dict or str
        If a dict, it is expected to provide a mapping of category value to
        a color; entries not in the mapping will be considered "null". If a
        str, the value is interpreted as the name of a color map and assumes
        a gradient is to be painted.
    null_kw : dict, optional
        Parameters to use for plotting and painting null or unknown values.
    focus_kw : dict, optional
        Parameters to use for plotting and painting values which are not
        null and in the field of interest.
    """
    # setup defaults if not provided
    if null_kw is None:
        null_kw = {}
    if focus_kw is None:
        focus_kw = {}

    # resolve if this is discrete or continous
    if isinstance(colors, str):
        plot = two_dimensional_gradient
        legend = legend_gradient
    else:
        plot = two_dimensional_discrete
        legend = legend_discrete

    # full page, with square plots
    fig, grid = plt.subplots(3, 4, sharex=False, sharey=False,
                             figsize=(24, 16))
    grid[0, 3].grid(False)
    grid[0, 3].set_axis_off()
    grid[2, 3].grid(False)
    grid[2, 3].set_axis_off()

    for row in range(3):
        # y_pc is the axis in the ordination to put on the y-axis
        y_pc = row + offset

        # the y-axis is consistent across a row so only label the
        # first column
        row_ax = grid[row, 0]
        row_ax.set_ylabel(_pcoa_label(y_pc, ordination), fontsize=14)

        for col in range(3):
            # x_pc is the axis in the ordination to put on the x-axis
            x_pc = row + col + offset + 1

            # fetch the specific subplot, and plot
            ax = grid[row, col]
            ax.set_xlabel(_pcoa_label(x_pc, ordination), fontsize=14)
            plot(ax, field, mapping, ordination, x_pc, y_pc, colors, null_kw,
                 focus_kw)

    # establish the legend on the right side
    legend(grid[1, 3], field, mapping, ordination, colors, null_kw)

    return (fig, grid)


def _pcoa_label(dim, ordination):
    """Helper method to make a PCoA label"""
    fmt = 'PC%d (%0.2f%%)'
    return fmt % (dim + 1, ordination.proportion_explained[dim] * 100)


def two_dimensional_gradient(ax, field, mapping, ordination, xaxis, yaxis,
                             colormap, null_kw, focus_kw):
    """Plot two axes

    Parameters
    ----------
    ax : AxesSubplot
        A subplot to plot into
    field : str
        A metadata field in the mapping to plot.
    mapping : pd.DataFrame
        The metadata about the samples.
    ordination : skbio.OrdinationResults
        The ordination object.
    xaxis : integer
        An axis to plot from the ordination.
    yaxis : integer
        An axis to plot from the ordination.
    colormap : str
        The colormap to use.
    null_kw : dict
        Additional arguments to the scatter plot for the samples in the
        background.
    focus_kw : dict
        Additional arguments to the scatter plot for the samples in focus.
    """
    gap_to_frame = 0.01

    mapping = mapping.loc[ordination.samples.index]
    field_values = mapping[~mapping[field].isnull()][field]

    nonfield_samples = set(mapping.index) - set(field_values.index)

    # discretize our color gradient, and determine which bin (i.e., color)
    # a given value is associated with
    bins = np.arange(field_values.min(),
                     field_values.max(),
                     (field_values.max() - field_values.min()) / 256.0)

    order = np.digitize(field_values, bins=bins, right=True)
    colors = np.array(sns.color_palette(colormap, n_colors=len(bins) + 1))

    # obtain the full vector of positions for each axis
    x_full = ordination.samples[xaxis]
    y_full = ordination.samples[yaxis]

    # plot nulls
    x = x_full.loc[nonfield_samples]
    y = y_full.loc[nonfield_samples]
    ax.scatter(x, y, **null_kw)

    # plot samples of interest
    x = x_full.loc[field_values.index].values
    y = y_full.loc[field_values.index].values
    ax.scatter(x, y, color=colors[order], **focus_kw)

    # finalize
    ax.set_xlim(x_full.min() - gap_to_frame, x_full.max() + gap_to_frame)
    ax.set_ylim(y_full.min() - gap_to_frame, y_full.max() + gap_to_frame)
    ax.grid(False)
    ax.set_yticklabels([])
    ax.set_xticklabels([])


def two_dimensional_discrete(ax, field, mapping, ordination, xaxis, yaxis,
                             colors, null_kw, focus_kw):
    """Plot two axes

    Parameters
    ----------
    ax : AxesSubplot
        A subplot to plot into
    field : str
        A metadata field in the mapping to plot.
    mapping : pd.DataFrame
        The metadata about the samples.
    ordination : skbio.OrdinationResults
        The ordination object.
    xaxis : integer
        An axis to plot from the ordination.
    yaxis : integer
        An axis to plot from the ordination.
    colors : dict
        A mapping of a metadata value to a color. A category not present
        in the mapping is assumed to be "null."
    null_kw : dict
        Additional arguments to the scatter plot for the samples in the
        background.
    focus_kw : dict
        Additional arguments to the scatter plot for the samples in focus.
    """
    gap_to_frame = 0.01

    mapping = mapping.loc[ordination.samples.index]
    field_values = mapping[mapping[field].isin(set(colors))][field]

    nonfield_samples = set(mapping.index) - set(field_values.index)

    # obtain the full vector of positions for each axis
    x_full = ordination.samples[xaxis]
    y_full = ordination.samples[yaxis]

    # plot nulls
    x = x_full.loc[nonfield_samples]
    y = y_full.loc[nonfield_samples]
    ax.scatter(x, y, **null_kw)

    # plot samples of interest
    for value in field_values.unique():
        value_index = field_values[field_values == value].index

        x = x_full.loc[value_index].values
        y = y_full.loc[value_index].values
        ax.scatter(x, y, color=colors.get(value), **focus_kw)

    # finalize
    ax.set_xlim(x_full.min() - gap_to_frame, x_full.max() + gap_to_frame)
    ax.set_ylim(y_full.min() - gap_to_frame, y_full.max() + gap_to_frame)
    ax.grid(False)
    ax.set_yticklabels([])
    ax.set_xticklabels([])


def legend_gradient(ax, field, mapping, ordination, colormap, null_kw):
    """Create a gradient legend

    Parameters
    ----------
    ax : AxesSubplot
        A subplot for the legend
    field : str
        A metadata field in the mapping to plot.
    mapping : pd.DataFrame
        The metadata about the samples.
    ordination : skbio.OrdinationResults
        The ordination object.
    colormap : str
        The colormap to use.
    null_kw : dict
        Additional arguments to the scatter plot for the samples in the
        background.
    """
    mapping = mapping.loc[ordination.samples.index]
    field_values = mapping[~mapping[field].isnull()][field]

    # get a gradient
    gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))

    # use the Freedman-Diaconis rule to determine number of bins
    counts, bins = np.histogram(field_values, bins='fd')

    # offset the histogram by a little bit so we can place the gradient below
    shift = 0.12 * counts.max()
    counts, bins, patches = ax.hist(field_values, bins=bins, color='k',
                                    bottom=shift)

    # move the ticks to the right side. generally the legend is on the
    # the right so this removes some clutter with the actual plot of interest
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")

    # deal with the yticks. notably, we need to account for our histogram shift
    # while still allowing for space to show the gradient
    ax.set_yticks([0 + shift,
                   counts.max() / 2.0 + shift,
                   counts.max() + shift])
    ax.set_yticklabels([0, int(counts.max() / 2.0), int(counts.max())],
                       fontsize=12, rotation=45)
    ax.set_ylim(0, counts.max() + shift)
    ax.set_xlim(bins[0], bins[-1])

    # plot the gradient in the space below the histogram
    ax.imshow(gradient, aspect='auto', cmap=colormap,
              extent=[bins[0], bins[-1], 0.0, shift - (shift * 0.2)])

    # put on the x and y labels
    ax.set_xlabel(field, fontsize=14)
    ax.set_ylabel('Counts', fontsize=14, rotation=270, labelpad=15)

    # the grid looks bad here...
    ax.grid(False)

    # if we have samples which do not have a value for this category, provide
    # include them in the legend and note their count
    if mapping[field].isnull().sum():
        base_y = counts.max()
        n_bins = len(bins)
        n_bins_40p = int(n_bins * 0.4)

        # if the histogram is heavily weighted on the left side, target the
        # rightside
        if counts[:n_bins_40p].sum() > counts[-n_bins_40p:].sum():
            dot = bins[-1] - bins[-1] * 0.25
            text = dot + dot * 0.02
        else:
            dot = bins[1]
            text = bins[2]

        n = mapping[field].isnull().sum()
        ax.scatter([dot], [base_y + shift * 0.75], color='k')
        ax.text(text, base_y + shift * 0.55, "N/A (%d)" % n, fontsize=12)

    # turn off the frame
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)


def legend_discrete(ax, field, mapping, ordination, colors, null_kw):
    """Create a discrete legend

    Parameters
    ----------
    ax : AxesSubplot
        A subplot for the gradient histogram
    field : str
        A metadata field in the mapping to plot.
    mapping : pd.DataFrame
        The metadata about the samples.
    ordination : skbio.OrdinationResults
        The ordination object.
    colors : dict
        A mapping of a metadata value to a color.
    null_kw : dict
        Additional arguments to the scatter plot for the samples in the
        background.
    """
    unique_cats = [cat for cat in mapping[field].unique()
                   if cat in colors]
    nonunique_cats = [cat for cat in mapping[field].unique()
                      if cat not in colors]

    legend_names = []
    for cat in unique_cats:
        color = colors.get(cat)
        ax.scatter(-1, -1, color=color, s=100)
        legend_names.append(cat)

    if nonunique_cats:
        ax.scatter(-1, -1, color=null_kw.get('color'), s=100)
        legend_names.append("Unknown")

    ax.set_xlim(0, 1)
    ax.grid(False)
    ax.set_axis_off()

    ax.legend(legend_names, loc='center', prop={'size': 20})
