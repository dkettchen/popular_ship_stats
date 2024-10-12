import plotly.graph_objects as go
from visualisation.vis_utils.diagram_utils.make_subplots_by_year import make_subplots_by_year
from visualisation.vis_utils.diagram_utils.make_max_count import make_max_count

#
def visualise_rpf_vs_fic(input_dict:dict):
    """
    visualise the femslash output from rpf_vs_fic as pie charts
    """
    num_of_years = len(input_dict.keys)
    fig = make_subplots_by_year(num_of_years)
    max_count = make_max_count(num_of_years)

    row_count = 1
    col_count = 1

    for year in input_dict:
        year_df = input_dict[year].copy()

        colours = ["deeppink", "darkred"]

        fig.add_trace(go.Pie(
            labels=["RPF", "fictional"], 
            values=[year_df.loc["RPF"]["no_of_ships"], year_df.loc["fictional"]["no_of_ships"]], 
            hole=0.3, # determines hole size
            title=year, # text that goes in the middle of the hole
            sort=False, # if you want to keep it in its original order rather than sorting by size
            titlefont_size=10, # to format title text
            marker_colors=colours,
            automargin=False,
            textposition="inside"
        ), row_count, col_count)

        if col_count == max_count:
            col_count = 1
            row_count += 1
        else:
            col_count += 1

    fig.update_traces(
        textinfo='percent',
    )
    fig.update_layout(
        title="Real Person Fic vs fictional ships by year (AO3 femslash ranking 2014-2023)", 
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        #showlegend=False,
    )

    return fig
