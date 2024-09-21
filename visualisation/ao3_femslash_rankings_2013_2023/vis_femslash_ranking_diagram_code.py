from visualisation.vis_utils.remove_translation import remove_translation
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def visualise_market_share_and_popularity(input_dict, colour_lookup):
    """
    visualise the femslash output from fandom_market_share_by_year 
    or fandoms_popularity_by_year as pie charts
    """
    year_donuts_fig = make_subplots(rows=2, cols=5, specs=[[
        {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}
    ], [
        {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}
    ]],)

    row_count = 1
    col_count = 2

    if "no_of_ships" in input_dict[2023].columns:
        femslash_title = "Fandoms (> 1 ship) by market share by year (AO3 femslash ranking 2013-2023)"
        column_name = "no_of_ships"
    elif "rank_sum" in input_dict[2023].columns:
        femslash_title = "Top 15 fandoms by popularity by year (AO3 femslash ranking 2013-2023)"
        column_name = "rank_sum"

    for year in input_dict:
        year_df = input_dict[year]
        fandoms = []
        for fandom in year_df.index:
            if " | " in fandom:
                new_fandom = remove_translation(fandom) 
                if "Madoka" in new_fandom:
                    new_fandom = "Madoka"
                elif new_fandom == "My Hero Academia":
                    new_fandom = "MHA"
            elif "Universe" in fandom and fandom != "Steven Universe":
                new_fandom = fandom[:-9]
                if "Avatar" in new_fandom:
                    new_fandom = "ATLA"
                elif "Game of Thrones" in new_fandom:
                    new_fandom = "GoT"
            elif "She-Ra" in fandom:
                new_fandom = "She-Ra"
            else: new_fandom = fandom
            fandoms.append(new_fandom)

        ships_no = year_df[column_name]

        colours = list(year_df.reset_index()["fandom"].apply(lambda x: colour_lookup[x]))

        year_donuts_fig.add_trace(go.Pie(
            labels=fandoms, 
            values=ships_no, 
            hole=0.3, # determines hole size
            title=year, # text that goes in the middle of the hole
            sort=False, # if you want to keep it in its original order rather than sorting by size
            titlefont_size=25, # to format title text
            marker_colors=colours,
            automargin=False,
            textposition="inside"
        ), row_count, col_count)

        if col_count == 5:
            col_count = 1
            row_count += 1
        else:
            col_count += 1

    year_donuts_fig.update_traces(
        textinfo='label',
        # marker=dict(
        #     #colors=px.colors.qualitative.Bold + px.colors.qualitative.Bold, # to use colours
        #     line=dict(color='#000000', width=2) # to add outline
        # )
    )
    year_donuts_fig.update_layout(
        title=femslash_title, 
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        showlegend=False,
        # colorway=list(colour_lookup.values())
        # px.colors.qualitative.Bold + \
        #     px.colors.qualitative.Pastel + \
        #     px.colors.qualitative.Prism + \
        #     px.colors.qualitative.Vivid
    )

    return year_donuts_fig

def visualise_top_5_fandoms(input_dict):
    pass


