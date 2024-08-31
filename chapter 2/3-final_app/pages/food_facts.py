import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb


def on_navigate(state):
    print("ho")


###########################
## Initial values        ##
###########################
fao_csv_file = "./data/faostat_data.csv"


def create_df_faostat(file_path=fao_csv_file):
    df_faostat = pd.read_csv(file_path)
    df_faostat.drop(
        columns=["Domain Code", "Year Code", "Months Code", "Flag", "Element"],
        inplace=True,
    )
    df_faostat = df_faostat.reset_index(drop=True)
    return df_faostat


df_faostat = create_df_faostat()

lov_year = list(df_faostat["Year"].astype(str).unique())
lov_year.append("All")
selected_year = "All"

keep_estimated_values = True

selected_statistic = "Consumer Prices, Food Indices (2015 = 100)"
lov_statistics = list(df_faostat["Item"].unique())
df_faostat = df_faostat[
    df_faostat["Item"] == "Consumer Prices, Food Indices (2015 = 100)"
].reset_index(drop=True)

lov_months = list(df_faostat["Months"].unique())
months = lov_months


def create_fig_countries(df_faostat):
    fig_countries = px.choropleth(
        df_faostat,
        locations="Area Code (ISO3)",
        color="Value",
        title="Values per country",
        scope="europe",
    )
    return fig_countries


fig_countries = create_fig_countries(df_faostat)


###########################
## Callbacks             ##
###########################
def edit_note(state, var_name, payload):
    if payload["col"] == "Note":
        df_faostat_new = state.df_faostat.copy()
        df_faostat_new.loc[payload["index"], payload["col"]] = payload["value"]
        state.df_faostat = df_faostat_new
    else:
        None


def add_row(state, var_name, payload):
    empty_row = pd.DataFrame(
        [[None for _ in state.df_faostat.columns]], columns=state.df_faostat.columns
    )
    empty_row["Domain"] = "New Index"
    state.df_faostat = pd.concat(
        [empty_row, state.df_faostat], axis=0, ignore_index=True
    )


def delete_row(state, var_name, payload):
    index = payload["index"]
    state.df_faostat = state.df_faostat.drop(index=index)


def filter_dataframe(state, var_name, payload):
    state.df_faostat = create_df_faostat()

    df_faostat_copy = state.df_faostat.copy().reset_index(drop=True)

    filter_condition = pd.Series([True] * len(df_faostat_copy))

    filter_condition &= df_faostat_copy["Item"] == state.selected_statistic

    if state.selected_year != "All":
        filter_condition &= df_faostat_copy["Year"] == int(state.selected_year)
    if not state.keep_estimated_values:
        filter_condition &= df_faostat_copy["Flag Description"] != "Estimated value"

    filter_condition &= df_faostat_copy["Months"].isin(state.months)

    df_faostat_copy = df_faostat_copy.loc[filter_condition]

    state.df_faostat = df_faostat_copy
    state.fig_countries = create_fig_countries(state.df_faostat)


def change_chart(state, var_name, payload):
    print(var_name)
    print(payload)


###########################
## Page             ##
###########################
with tgb.Page() as food_fact_page:
    tgb.text("# Food facts 📊", mode="md", class_name="color-secondary header")

    with tgb.layout("1 1 1 1 1"):

        tgb.selector(
            value="{selected_statistic}",
            lov="{lov_statistics}",
            mode="radio",
            on_change=filter_dataframe,
        )
        tgb.toggle(
            value="{keep_estimated_values}",
            label="Keep estimated values",
            on_change=filter_dataframe,
        )
        tgb.toggle(
            value="{selected_year}",
            lov="{lov_year}",
            on_change=filter_dataframe,
            label="select year",
        )

        tgb.selector(
            value="{months}",
            lov="{lov_months}",
            label="Choose month",
            multiple=True,
            on_change=filter_dataframe,
            dropdown=True,
        )

        tgb.file_download(
            content="{fao_csv_file}",
            label="download dataset",
            name="fao_dataset_eu_2019-2024.csv",
        )

    with tgb.layout("1 1 1"):
        tgb.chart(
            data="{df_faostat}",
            type="bar",
            x="Year",
            y="Value",
            title="Value per year",
            class_name="p0 m0",
        )
        tgb.chart(
            data="{df_faostat}",
            type="heatmap",
            x="Year",
            y="Months",
            z="Value",
            title="Value per year and month",
            class_name="p0 m0",
        )
        tgb.chart(
            figure="{fig_countries}",
            class_name="p0 m0",
        )

    with tgb.part():
        tgb.table(
            data="{df_faostat}",
            height="60vh",
            filter=True,
            hover_text="Fao Data",
            nan_value=0,
            on_edit=edit_note,
            on_add=add_row,
            on_delete=delete_row,
            class_name="p0 m0",
        )
